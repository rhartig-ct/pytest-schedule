from typing import List

import pytest


def assign_xdist_workers(items: list[pytest.Item], split_data: List["Process"]) -> None:
    """Assign xdist groups to schedule jobs first using `loadgroup`
    distribution mode.
    """
    for i in items:
        for process in split_data:
            if i.nodeid in process.jobs:
                i.add_marker(pytest.mark.xdist_group(name=f"gw{process.id}"))
                break


class Process:
    def __init__(self, id=-1):
        self.jobs = []
        self.job_times = []
        self.job_time_sum = 0
        self.id = id

    def append(self, job: str, time: float):
        self.jobs.append(job)
        self.job_times.append(time)
        self.job_time_sum += time

    def __repr__(self):
        return f"""
            id: {self.id}
            jobs: {self.jobs}
            job_times: {self.job_times}
            job_time_sum: {self.job_time_sum}"""

    def __str__(self):
        return f"""
            id: {self.id}
            job_time_sum: {self.job_time_sum}"""

    def to_dict(self):
        return {
            "id": self.id,
            "jobs": self.jobs,
            "job_times": self.job_times,
            "job_time_sum": self.job_time_sum,
        }
