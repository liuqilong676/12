"""校园物联网设备报修——命令行演示程序。

运行（在 src/python 目录下）：
    python cli.py
设备清单默认读取 ../../data/devices.csv，可用参数指定。
"""

import sys
from pathlib import Path

from repair_service import (DeviceNotFoundError, RepairService, ValidationError,
                            WorkOrderNotFoundError)
from status_rule import PROCESSING, COMPLETED, status_label
from work_order import InvalidTransitionError

MENU = """
================ 校园物联网设备报修 ================
 1  查看设备清单（FR-01）
 2  查看设备信息（FR-01）
 3  提交报修（FR-02）
 4  开始维修（FR-03）
 5  完成维修（FR-03）
 6  工单列表
 0  退出
====================================================
"""


def default_data_path():
    here = Path(__file__).resolve().parent
    return here.parents[1] / "data" / "devices.csv"


def show_devices(service):
    print("\n设备编号      名称              位置")
    print("-" * 48)
    for device in service.list_devices():
        print(f"{device.device_id:<12}{device.name:<16}{device.location}")


def show_device(service):
    device_id = input("请输入设备编号（如 DEV-001）：")
    try:
        device = service.get_device(device_id)
    except DeviceNotFoundError as exc:
        print(f"[提示] {exc}")
        return
    print(f"\n设备编号：{device.device_id}")
    print(f"设备名称：{device.name}")
    print(f"安装位置：{device.location}")


def submit_repair(service):
    device_id = input("请输入设备编号（如 DEV-001）：")
    description = input("请描述故障现象：")
    reporter = input("报修人（回车默认为“报修人”）：") or "报修人"
    try:
        order = service.submit_repair(device_id, description, reporter)
    except (DeviceNotFoundError, ValidationError) as exc:
        print(f"[失败] {exc}，未创建工单")
        return
    print(f"[成功] 已生成工单 {order.order_id}，当前状态 {status_label(order.status)}")


def change_status(service, action):
    order_id = input("请输入工单编号：")
    handler = input("维修人员（回车默认为“维修人员”）：") or "维修人员"
    try:
        if action == "start":
            order = service.start_repair(order_id, handler)
        else:
            order = service.complete_repair(order_id, handler)
    except WorkOrderNotFoundError as exc:
        print(f"[失败] {exc}")
    except InvalidTransitionError as exc:
        print(f"[失败] {exc}")
    else:
        print(f"[成功] 工单 {order.order_id} 状态已更新为 {status_label(order.status)}")


def show_orders(service):
    orders = service.list_orders()
    if not orders:
        print("\n暂无工单。")
        return
    print("\n工单编号              设备编号    状态    故障描述")
    print("-" * 72)
    for order in orders:
        print(f"{order.order_id:<22}{order.device_id:<12}"
              f"{status_label(order.status):<8}{order.description}")


def main(argv):
    path = Path(argv[1]) if len(argv) > 1 else default_data_path()
    try:
        service = RepairService.from_csv(path)
    except (OSError, ValueError) as exc:
        print(f"[错误] 无法读取设备清单 {path}：{exc}")
        return 2

    actions = {
        "1": show_devices,
        "2": show_device,
        "3": submit_repair,
        "6": show_orders,
    }
    while True:
        print(MENU)
        choice = input("请选择操作：").strip()
        if choice == "0":
            print("已退出。")
            return 0
        if choice in actions:
            actions[choice](service)
        elif choice == "4":
            change_status(service, "start")
        elif choice == "5":
            change_status(service, "complete")
        else:
            print("[提示] 无效选项，请重新输入。")


if __name__ == "__main__":
    sys.exit(main(sys.argv))
