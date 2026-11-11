"""报修业务服务层：查看设备、提交报修、更新工单状态。

界面（cli.py）与数据层（device.py、work_order.py）之间的薄服务层，
集中实现 FR-01~FR-03 的业务校验：

* FR-01 查看设备：设备编号不存在时抛 DeviceNotFoundError；
* FR-02 提交报修：设备必须在清单内、故障描述必须非空，否则抛 ValidationError，
  且不创建工单；成功时生成状态为 PENDING 的工单；
* FR-03 更新状态：只允许 PENDING→PROCESSING、PROCESSING→COMPLETED，
  其余转换由 WorkOrder.transition_to 抛 InvalidTransitionError。
"""

import itertools
from datetime import date

from device import Device, load_devices
from status_rule import PENDING
from work_order import WorkOrder


class DeviceNotFoundError(LookupError):
    """设备编号不在清单内。"""


class WorkOrderNotFoundError(LookupError):
    """工单编号不存在。"""


class ValidationError(ValueError):
    """输入不完整或不合法。"""


class RepairService:
    """校园物联网设备报修的业务门面。"""

    def __init__(self, devices):
        """devices: {device_id: Device} 字典，通常由 load_devices() 生成。"""
        self._devices = dict(devices)
        self._orders = {}
        self._counter = itertools.count(1)
        self._day = date.today().strftime("%Y%m%d")

    @classmethod
    def from_csv(cls, path):
        """按设备清单 CSV 构造服务。"""
        return cls(load_devices(path))

    # ---------- FR-01 查看设备 ----------
    def list_devices(self):
        """返回设备清单（按编号排序）。"""
        return [self._devices[k] for k in sorted(self._devices)]

    def get_device(self, device_id):
        """按编号查询设备，不存在时给出明确提示。"""
        device_id = (device_id or "").strip()
        device = self._devices.get(device_id)
        if device is None:
            raise DeviceNotFoundError(f"设备编号不存在：{device_id or '（空）'}")
        return device

    # ---------- FR-02 提交报修 ----------
    def submit_repair(self, device_id, description, reporter="报修人"):
        """提交报修，返回新建工单（状态 PENDING）。

        设备不在清单内或故障描述为空/全空格时抛异常，不创建工单。
        """
        device = self.get_device(device_id)          # 设备校验
        text = (description or "").strip()
        if not text:
            raise ValidationError("故障描述不能为空")
        order = WorkOrder(
            order_id=self._next_order_id(),
            device_id=device.device_id,
            description=text,
            status=PENDING,
            reporter=(reporter or "报修人").strip() or "报修人",
        )
        self._orders[order.order_id] = order
        return order

    # ---------- FR-03 更新工单状态 ----------
    def start_repair(self, order_id, handler="维修人员"):
        """开始维修：PENDING -> PROCESSING。"""
        return self._get_order(order_id).transition_to("PROCESSING", handler)

    def complete_repair(self, order_id, handler="维修人员"):
        """完成维修：PROCESSING -> COMPLETED。"""
        return self._get_order(order_id).transition_to("COMPLETED", handler)

    def transition(self, order_id, target_status, handler="维修人员"):
        """通用状态更新，供界面选择目标状态时使用。"""
        return self._get_order(order_id).transition_to(target_status, handler)

    # ---------- 查询 ----------
    def list_orders(self, status=None):
        """返回工单列表，可按状态过滤。"""
        orders = [self._orders[k] for k in sorted(self._orders)]
        if status:
            orders = [o for o in orders if o.status == status]
        return orders

    def get_order(self, order_id):
        return self._get_order(order_id)

    def _get_order(self, order_id):
        order_id = (order_id or "").strip()
        order = self._orders.get(order_id)
        if order is None:
            raise WorkOrderNotFoundError(f"工单编号不存在：{order_id or '（空）'}")
        return order

    def _next_order_id(self):
        return f"WO-{self._day}-{next(self._counter):03d}"
