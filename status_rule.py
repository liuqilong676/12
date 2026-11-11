"""工单状态判断规则。

按《软件工程实验指导书——校园物联网设备报修》的统一约定：
新工单为 PENDING；只允许 PENDING→PROCESSING、PROCESSING→COMPLETED；
跳级、回退、状态不变以及其他非法输入一律返回 False。
"""

PENDING = "PENDING"
PROCESSING = "PROCESSING"
COMPLETED = "COMPLETED"

#: 唯一允许的两条业务转换，元素为（当前状态, 目标状态）
ALLOWED_TRANSITIONS = frozenset({
    (PENDING, PROCESSING),      # 开始维修
    (PROCESSING, COMPLETED),    # 完成维修
})

#: 状态的中文名称，用于界面提示
STATUS_LABELS = {
    PENDING: "待处理",
    PROCESSING: "处理中",
    COMPLETED: "已完成",
}


def can_transition(current, target):
    """判断工单能否从 current 转到 target。

    参数:
        current: 当前状态（str）
        target:  目标状态（str）

    返回:
        bool —— 只有两条允许的转换返回 True，其余（含状态不变、
        未知状态、None 等）返回 False。
    """
    return (current, target) in ALLOWED_TRANSITIONS


def status_label(status):
    """返回状态的中文名称，未知状态原样返回。"""
    return STATUS_LABELS.get(status, status)
