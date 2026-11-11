"""业务层补充测试（实验规定的 4 项见 test_status_rule.py）。

运行（在 src/python 目录下）：
    python -m unittest test_repair_service -v
"""

import unittest
from pathlib import Path

import status_rule
from device import Device, load_devices
from repair_service import (DeviceNotFoundError, RepairService, ValidationError,
                            WorkOrderNotFoundError)
from work_order import InvalidTransitionError

DEVICES = {
    "DEV-001": Device("DEV-001", "温湿度传感器", "A101教室"),
    "DEV-002": Device("DEV-002", "智能门锁", "B202实验室"),
}


def new_service():
    return RepairService(DEVICES)


class StatusRuleTest(unittest.TestCase):
    """规定的两条允许规则与全部拒绝分支。"""

    def test_two_allowed_transitions(self):
        self.assertTrue(status_rule.can_transition("PENDING", "PROCESSING"))
        self.assertTrue(status_rule.can_transition("PROCESSING", "COMPLETED"))

    def test_skip_and_rollback_rejected(self):
        self.assertFalse(status_rule.can_transition("PENDING", "COMPLETED"))
        self.assertFalse(status_rule.can_transition("COMPLETED", "PROCESSING"))
        self.assertFalse(status_rule.can_transition("COMPLETED", "PENDING"))

    def test_same_status_and_unknown_rejected(self):
        for status in ("PENDING", "PROCESSING", "COMPLETED"):
            self.assertFalse(status_rule.can_transition(status, status))
        self.assertFalse(status_rule.can_transition("PENDING", "UNKNOWN"))
        self.assertFalse(status_rule.can_transition(None, "PROCESSING"))
        self.assertFalse(status_rule.can_transition("pending", "processing"))


class ViewDeviceTest(unittest.TestCase):
    def test_list_devices_sorted(self):
        devices = new_service().list_devices()
        self.assertEqual([d.device_id for d in devices], ["DEV-001", "DEV-002"])

    def test_get_device(self):
        device = new_service().get_device(" DEV-002 ")
        self.assertEqual(device.name, "智能门锁")

    def test_missing_device_prompts(self):
        with self.assertRaises(DeviceNotFoundError) as ctx:
            new_service().get_device("DEV-999")
        self.assertIn("DEV-999", str(ctx.exception))


class SubmitRepairTest(unittest.TestCase):
    def test_new_order_is_pending(self):
        service = new_service()
        order = service.submit_repair("DEV-001", "读数一直为 0，疑似探头损坏")
        self.assertEqual(order.status, "PENDING")
        self.assertEqual(order.device_id, "DEV-001")
        self.assertEqual(len(service.list_orders()), 1)

    def test_blank_description_not_created(self):
        service = new_service()
        for text in ("", "   ", "\t\n"):
            with self.assertRaises(ValidationError):
                service.submit_repair("DEV-001", text)
        self.assertEqual(service.list_orders(), [])

    def test_unknown_device_not_created(self):
        service = new_service()
        with self.assertRaises(DeviceNotFoundError):
            service.submit_repair("DEV-404", "设备掉线")
        self.assertEqual(service.list_orders(), [])

    def test_description_is_trimmed(self):
        order = new_service().submit_repair("DEV-002", "  门锁无法刷开  ")
        self.assertEqual(order.description, "门锁无法刷开")


class UpdateStatusTest(unittest.TestCase):
    def setUp(self):
        self.service = new_service()
        self.order = self.service.submit_repair("DEV-001", "湿度数值异常")

    def test_normal_flow(self):
        order = self.service.start_repair(self.order.order_id, "李工")
        self.assertEqual(order.status, "PROCESSING")
        self.assertEqual(order.handler, "李工")
        order = self.service.complete_repair(self.order.order_id, "李工")
        self.assertEqual(order.status, "COMPLETED")
        self.assertTrue(order.started_at and order.completed_at)

    def test_skip_rejected(self):
        with self.assertRaises(InvalidTransitionError):
            self.service.complete_repair(self.order.order_id)
        self.assertEqual(self.service.get_order(self.order.order_id).status, "PENDING")

    def test_rollback_rejected(self):
        self.service.start_repair(self.order.order_id)
        self.service.complete_repair(self.order.order_id)
        with self.assertRaises(InvalidTransitionError):
            self.service.start_repair(self.order.order_id)
        self.assertEqual(self.service.get_order(self.order.order_id).status, "COMPLETED")

    def test_repeat_start_rejected(self):
        self.service.start_repair(self.order.order_id)
        with self.assertRaises(InvalidTransitionError):
            self.service.start_repair(self.order.order_id)

    def test_missing_order(self):
        with self.assertRaises(WorkOrderNotFoundError):
            self.service.start_repair("WO-1970-001")

    def test_orders_filtered_by_status(self):
        self.service.start_repair(self.order.order_id)
        self.assertEqual(len(self.service.list_orders("PROCESSING")), 1)
        self.assertEqual(len(self.service.list_orders("PENDING")), 0)


class DeviceCsvTest(unittest.TestCase):
    def test_load_starter_csv(self):
        path = Path(__file__).resolve().parents[2] / "data" / "devices.csv"
        if not path.exists():
            self.skipTest(f"未找到设备清单：{path}")
        devices = load_devices(path)
        self.assertIn("DEV-001", devices)
        self.assertEqual(devices["DEV-003"].location, "C楼走廊")


if __name__ == "__main__":
    unittest.main(verbosity=2)
