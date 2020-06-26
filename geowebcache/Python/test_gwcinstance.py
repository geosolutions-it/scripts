from __future__ import print_function

import unittest
import timeout_decorator
import time
from gwcinstance import GWCInstance
from gwctask import GWCTask
from utils import tasks_to_str
from pprint import pprint, pformat

GWC_REST_URL="http://localhost:8080/geoserver/gwc/rest"
USERNAME = "admin"
PASSWORD = "geoserver"

GLOBAL_TIMEOUT = 1800
LOCAL_TIMEOUT = 60

def setUpModule():
    print("setUpModule: " + __name__ + " set up")
    print

def tearDownModule():
    print("tearDownModule: " + __name__ + " tear down")
    print

class TestGWCInstance(unittest.TestCase):

    gwc = None

    @classmethod
    def setUpClass(cls):
        TestGWCInstance.gwc = GWCInstance(
            gwc_rest_url = GWC_REST_URL,
            username = USERNAME,
            password = PASSWORD
        )
        print("setUpClass: " + cls.__name__ + " set up")
        print

    @classmethod
    def tearDownClass(cls):
        """ Test GWCInstance instantiation """
        del TestGWCInstance.gwc
        print("tearDownClass: " + cls.__name__ + " tear down")
        print

    # GWC must not be busy to start with
    def setUp(self):
        print("setUp")
        assert not TestGWCInstance.gwc.is_busy()
        print

    def tearDown(self):
        print("tearDown")
        TestGWCInstance.gwc.kill_tasks()
        while TestGWCInstance.gwc.is_busy():
            time.sleep(1)
        print


    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_get_tasks(self):
        """ Test tasks retrieval """
        tasks = TestGWCInstance.gwc.get_tasks()
        assert isinstance(tasks, list)
        pprint(tasks)

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_submit_task_seed(self):
        """ Test simple seeding task submission """
        task = GWCTask(
            name="topp:states",
            srs=4326,
            zoomStart=1,
            zoomStop=8,
            format="image/png8",
            type="seed",
            threadCount=1
        )

        print( "Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        time.sleep(1)
        tasks = TestGWCInstance.gwc.get_tasks()
        assert len(tasks) == 1
        print( "Running Tasks: \n{}".format(tasks_to_str(tasks)) )


    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_submit_task_seed_with_parameters(self):
        """ Test seeding task with parameters """
        task = GWCTask(
            name="topp:states",
            srs=4326,
            parameters=[
                ('STYLES', "population"),
                ('CQL_FILTER', "STATE_NAME='Wyoming'")
            ],
            zoomStart=1,
            zoomStop=8,
            format="image/png8",
            type="seed",
            threadCount=1
        )
        print( "Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        time.sleep(1)
        tasks = TestGWCInstance.gwc.get_tasks()
        assert len(tasks) == 1
        print( "Running Tasks: \n{}".format(tasks_to_str(tasks)) )


    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_submit_task_seed_with_bounds(self):
        """ Test seeding task with bbox """
        task = GWCTask(
            name="topp:states",
            srs=4326,
            bounds=[-124.0,22.0,66.0,72.0],
            zoomStart=1,
            zoomStop=4,
            format="image/png8",
            type="seed",
            threadCount=1
        )
        print( "Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        time.sleep(1)
        tasks = TestGWCInstance.gwc.get_tasks()
        assert len(tasks) == 1
        print( "Running Tasks: \n{}".format(tasks_to_str(tasks)) )

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_submit_task_truncate(self):
        """ Test truncate task """
        task = GWCTask(
            name="topp:states",
            srs=4326,
            zoomStart=1,
            zoomStop=8,
            format="image/png8",
            type="truncate",
            threadCount=1
        )
        print("Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        tasks = TestGWCInstance.gwc.get_tasks()
        assert len(tasks) == 1
        print("Running Tasks: \n{}".format(tasks_to_str(tasks)))

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_submit_task_truncate_with_parameters(self):
        """ Test truncate task with parameters """
        task = GWCTask(
            name="topp:states",
            srs=4326,
            parameters=[
                ('STYLES', "population"),
                ('CQL_FILTER', "STATE_NAME='Wyoming'")
            ],
            zoomStart=1,
            zoomStop=8,
            format="image/png8",
            type="truncate",
            threadCount=1
        )
        print( "Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        tasks = TestGWCInstance.gwc.get_tasks()
        assert len(tasks) == 1
        print( "Running Tasks: \n{}".format(tasks_to_str(tasks)) )

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_submit_task_truncate_with_bounds(self):
        """ Test truncate task with bounds """
        task = GWCTask(
            name="topp:states",
            srs=4326,
            bounds=[-124.0, 22.0, 66.0, 72.0],
            zoomStart=1,
            zoomStop=8,
            format="image/png8",
            type="truncate",
            threadCount=1
        )
        print( "Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        tasks = TestGWCInstance.gwc.get_tasks()
        assert len(tasks) == 1
        print( "Running Tasks: \n{}".format(tasks_to_str(tasks)) )

    @timeout_decorator.timeout(LOCAL_TIMEOUT)
    def test_kill_tasks_layer(self):
        """ Test tasks killing on a specific Layer """
        task = GWCTask(
            name="topp:states",
            srs=4326,
            zoomStart=1,
            zoomStop=15,
            format="image/png8",
            type="seed",
            threadCount=1
        )
        print( "Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        task = GWCTask(
            name="topp:tasmania_roads",
            srs=4326,
            zoomStart=1,
            zoomStop=15,
            format="image/png8",
            type="seed",
            threadCount=1
        )
        print( "Submitting Task: \n" + str(task))
        assert TestGWCInstance.gwc.submit_task(task) is not False

        tasks = TestGWCInstance.gwc.get_tasks()
        assert len(tasks) == 2

        print( "Running Tasks BEFORE: \n{}".format(tasks_to_str(tasks)) )

        layer = 'topp:states'
        print( "Killing Tasks for layer: {}\n".format(layer))
        TestGWCInstance.gwc.kill_tasks(layer=layer)
        time.sleep(5)

        tasks = TestGWCInstance.gwc.get_tasks()
        print( "Running Tasks AFTER: \n{}".format(tasks_to_str(tasks)) )

        assert len(tasks) == 1

if __name__ == "__main__":
    timeout_decorator.timeout(GLOBAL_TIMEOUT)(unittest.main)()
