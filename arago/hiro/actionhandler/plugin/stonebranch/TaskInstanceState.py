from enum import Enum


# TODO
class TaskInstanceState(Enum):
    SUCCESS = 0
    LAUNCH_PENDING = 1
    LAUNCH_SUCCESS = 2
    LAUNCH_FAILED = 2
    SKIPPED = 2
    CANCELLED = 2
    FINISHED = 2
    FAILED = 5

    # 'FINISHED': TaskInstanceState.FINISHED,
    # 'CANCELLED': TaskInstanceState.CANCELLED,
    # 'FAILED': TaskInstanceState.FAILED,
    # 'SKIPPED': TaskInstanceState.SKIPPED,
    # 'START_FAILURE': TaskInstanceState.FAILED,
    # 'SUCCESS': TaskInstanceState.SUCCESS,
