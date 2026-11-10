"""设备实体（对应需求 FR-01 查看设备）。"""

from dataclasses import dataclass


@dataclass
class Device:
    """一台校园物联网设备。

    属性:
        device_id: 设备编号，例如 DEV-001，全局唯一
        name:      设备名称，例如 温湿度传感器
        location:  安装位置，例如 A101教室
    """

    device_id: str
    name: str
    location: str

    def describe(self):
        """返回用于界面展示的一行文字。"""
        return f"{self.device_id}  {self.name}  {self.location}"


def load_devices(path):
    """从 CSV 清单读取设备，返回 {device_id: Device} 字典。

    CSV 首行为表头 deviceId,name,location；编码为 UTF-8。
    """
    import csv
    import os

    devices = {}
    with open(path, "r", encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            device = Device(
                device_id=row["deviceId"].strip(),
                name=row["name"].strip(),
                location=row["location"].strip(),
            )
            devices[device.device_id] = device
    if not devices:
        raise ValueError(f"设备清单为空：{os.fspath(path)}")
    return devices
