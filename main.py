# -*- coding: UTF-8 -*-

import logging
import os
import math
import time
import random
import threading
import multiprocessing

def load_cpu(deadline):
    start = time.time()
    
    while time.time() - start < deadline:
        math.pow(random.randint(0, 1), random.randint(0, 1))

def spawn_job(deadline):
    manager = multiprocessing.Manager()
    results = manager.dict()

    timeout = deadline + 0.100
    time_start = time.time()
    job = multiprocessing.Process(target=load_cpu, args=(deadline, ))
    job.start()
    job.join(timeout)
    elapsed = time.time()-time_start
    if elapsed < timeout and job.is_alive():
        print("job.join() returned too early")


def spawn_jobs(amount):
    jobs = []
    for i in range(amount):
        job = threading.Thread(target=spawn_job, args=(0.200, ))
        job.start()
        jobs.append(job)
    return jobs

def join_jobs(jobs):
    for job in jobs:
        job.join()

if __name__ == '__main__':
    logger = logging.getLogger('multiprocess') 
    loglevel = os.environ.get("LOGLEVEL", "INFO").upper()
    if loglevel == "": loglevel = os.environ.get("LOG_LEVEL", "INFO").upper()
    while True:
        jobs = spawn_jobs(8)
        join_jobs(jobs)