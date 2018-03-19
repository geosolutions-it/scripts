from __future__ import division

from gwcinstance import GWC_TASK_STATUS

def tasks_to_str(pending_array):
    """ Pretty print GWC instances pending tasks array """
    s = 'Total Tasks running: {}\n'.format(len(pending_array))
    for task in pending_array:
        processed, total, remaining, task_id, task_status = task
        progress = (processed/total) * 100 if total > 0 else -1
        s += "Task ID: {} Status: {} Total: {} Processed: {} Remaining: {} Progress: {}% \n".format(
            task_id,
            GWC_TASK_STATUS[task_status],
            total,
            processed,
            remaining,
            round(progress,2)
        )
    return s
