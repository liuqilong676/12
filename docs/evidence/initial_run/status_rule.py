"""起始包中的未实现版本：保留常量，但 can_transition 对所有输入返回 False。"""

PENDING = "PENDING"
PROCESSING = "PROCESSING"
COMPLETED = "COMPLETED"


def can_transition(current: str, target: str) -> bool:
    return False


def status_label(status: str) -> str:
    return status
