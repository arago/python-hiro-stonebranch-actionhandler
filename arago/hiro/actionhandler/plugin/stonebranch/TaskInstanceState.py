from enum import Enum, unique


# TODO
@unique
class TaskInstanceState(Enum):
    SUCCESS = 0x01
    LAUNCH_PENDING = 0x02
    LAUNCH_SUCCESS = 0x03
    LAUNCH_FAILED = 0x04
    SKIPPED = 0x05
    CANCELLED = 0x06
    FINISHED = 0x07
    FAILED = 0x08

    # 'FINISHED': TaskInstanceState.FINISHED,
    # 'CANCELLED': TaskInstanceState.CANCELLED,
    # 'FAILED': TaskInstanceState.FAILED,
    # 'SKIPPED': TaskInstanceState.SKIPPED,
    # 'START_FAILURE': TaskInstanceState.FAILED,
    # 'SUCCESS': TaskInstanceState.SUCCESS,
