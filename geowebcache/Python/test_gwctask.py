from __future__ import print_function

import unittest
from gwctask import GWCTask

class TestGWCTask(unittest.TestCase):
    def test_seed_task(self):
        """ Test Simple seed instantiation """
        gwc_task = GWCTask(
            name = "topp:states",
            bounds = None,
            srs = 4326,
            zoomStart = 1,
            zoomStop = 6,
            format = "image/png8",
            type = "seed",
            parameters = None,
            threadCount = 1
        )

    def test_truncate_task(self):
        """ Test Simple truncate instantiation """
        gwc_task = GWCTask(
            name = "topp:states",
            bounds = None,
            srs = 4326,
            zoomStart = 1,
            zoomStop = 6,
            format = "image/png8",
            type = "truncate",
            parameters = None,
            threadCount = 1
        )

    def test_seed_name_missing(self):
        """ 'name' is mandatory for 'seed' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name=None,
                bounds=None,
                srs=4326,
                zoomStart=1,
                zoomStop=6,
                format="image/png8",
                type="seed",
                parameters=None,
                threadCount=1
            )

    def test_seed_srs_missing(self):
        """ 'srs' is mandatory for 'seed' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=None,
                zoomStart=1,
                zoomStop=6,
                format="image/png8",
                type="seed",
                parameters=None,
                threadCount=1
            )

    def test_seed_zoomStart_missing(self):
        """ 'zoomStart' is mandatory for 'seed' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=4326,
                zoomStart=None,
                zoomStop=6,
                format="image/png8",
                type="seed",
                parameters=None,
                threadCount=1
            )

    def test_seed_zoomStop_missing(self):
        """ 'zoomStop' is mandatory for 'seed' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=4326,
                zoomStart=None,
                zoomStop=6,
                format="image/png8",
                type="seed",
                parameters=None,
                threadCount=1
            )

    def test_seed_format_missing(self):
        """ 'format' is mandatory for 'seed' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=4326,
                zoomStart=None,
                zoomStop=6,
                format="image/png8",
                type="seed",
                parameters=None,
                threadCount=1
            )

    def test_truncate_name_missing(self):
        """ 'name' is mandatory for 'truncate' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name=None,
                bounds=None,
                srs=4326,
                zoomStart=1,
                zoomStop=6,
                format="image/png8",
                type="truncate",
                parameters=None,
                threadCount=1
            )

    def test_truncate_srs_missing(self):
        """ 'srs' is mandatory for 'truncate' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=None,
                zoomStart=1,
                zoomStop=6,
                format="image/png8",
                type="truncate",
                parameters=None,
                threadCount=1
            )

    def test_seed_zoomStart_missing(self):
        """ 'zoomStart' is mandatory for 'seed' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=4326,
                zoomStart=None,
                zoomStop=6,
                format="image/png8",
                type="seed",
                parameters=None,
                threadCount=1
            )

    def test_truncate_zoomStop_missing(self):
        """ 'zoomStop' is mandatory for 'truncate' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=4326,
                zoomStart=None,
                zoomStop=6,
                format="image/png8",
                type="truncate",
                parameters=None,
                threadCount=1
            )

    def test_truncate_format_missing(self):
        """ 'format' is mandatory for 'truncate' task """
        with self.assertRaises(ValueError):
            GWCTask(
                name="topp:states",
                bounds=None,
                srs=4326,
                zoomStart=None,
                zoomStop=6,
                format="image/png8",
                type="truncate",
                parameters=None,
                threadCount=1
            )

if __name__ == "__main__":
    unittest.main()
