from enum import Enum, auto, unique


# TODO
@unique
class TaskInstanceState(Enum):
    SUCCESS = auto()
    LAUNCH_PENDING = auto()
    LAUNCH_SUCCESS = auto()
    LAUNCH_FAILED = auto()
    SKIPPED = auto()
    CANCELLED = auto()
    FINISHED = auto()
    FAILED = auto()

    # 'FINISHED': TaskInstanceState.FINISHED,
    # 'CANCELLED': TaskInstanceState.CANCELLED,
    # 'FAILED': TaskInstanceState.FAILED,
    # 'SKIPPED': TaskInstanceState.SKIPPED,
    # 'START_FAILURE': TaskInstanceState.FAILED,
    # 'SUCCESS': TaskInstanceState.SUCCESS,
