"""工单实体（对应需求 FR-02 提交报修、FR-03 更新状态）。

工单只通过 transition_to() 修改状态，是否允许由 status_rule.can_transition()
统一判断，避免把状态规则散落在业务代码中。
"""

from dataclasses import dataclass, field
from datetime import datetime

from status_rule import (COMPLETED, PENDING, PROCESSING, can_transition,
                         status_label)


class InvalidTransitionError(Exception):
    """非法状态转换，例如跳级、回退或状态不变。"""

    def __init__(self, current, target):
        self.current = current
        self.target = target
        super().__init__(
            f"不允许的状态转换：{status_label(current)}({current}) -> "
            f"{status_label(target)}({target})"
        )


def _now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@dataclass
class WorkOrder:
    """一张报修工单。

    必需属性（实验要求）：
        order_id:    工单编号，例如 WO-20261110-001
        device_id:   关联设备编号，每张工单对应 1 台设备
        description: 故障描述，提交时必须非空
        status:      工单状态，新建为 PENDING

    追踪属性（便于演示和记录）：
        reporter:    报修人
        handler:     受理的维修人员
        created_at:  创建时间
        started_at:  开始维修时间
        completed_at:完成维修时间
    """

    order_id: str
    device_id: str
    description: str
    status: str = field(default=PENDING)
    reporter: str = "报修人"
    handler: str = ""
    created_at: str = field(default_factory=_now_text)
    started_at: str = ""
    completed_at: str = ""

    def transition_to(self, target, handler=""):
        """把工单状态改为 target，不允许时抛出 InvalidTransitionError。"""
        if not can_transition(self.status, target):
            raise InvalidTransitionError(self.status, target)
        self.status = target
        if target == PROCESSING:
            self.started_at = _now_text()
            if handler:
                self.handler = handler
        elif target == COMPLETED:
            self.completed_at = _now_text()
            if handler:
                self.handler = handler
        return self

    def describe(self):
        """返回用于界面展示的一行文字。"""
        return (f"{self.order_id}  {self.device_id}  "
                f"{status_label(self.status)}  故障：{self.description}")
