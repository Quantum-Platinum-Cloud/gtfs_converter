from rq_scheduler.scheduler import Scheduler
import rq
from redis import Redis
import os
import sys

import init_log
import logging


def _run_scheduler():
    with rq.Connection(Redis.from_url(os.environ.get("REDIS_URL") or "redis://")):
        q = rq.Queue()
        scheduler = Scheduler(queue=q)

        scheduler.cron(
            cron_string="0 7 * * 2",  # every tuesday at 7:00,
            func="merge_all_geojson.merge_geojson",
        )

        scheduler.run()


def _run_task(task):
    """debug task to manually trigger a geojson merge"""
    from datetime import timedelta

    with rq.Connection(Redis.from_url(os.environ.get("REDIS_URL") or "redis://")):
        q = rq.Queue()
        scheduler = Scheduler(queue=q)

        scheduler.enqueue_in(
            timedelta(seconds=1), func=task,
        )


if __name__ == "__main__":
    init_log.config_worker_log()

    if len(sys.argv) > 1:
        # run custom task for debug, like:
        # `python scheduler.py merge_all_geojson.merge_geojson`
        _run_task(sys.argv[1])
    else:
        _run_scheduler()
