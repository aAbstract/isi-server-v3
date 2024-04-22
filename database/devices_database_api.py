from tinydb import Query
from models.runtime import Result
from database.tinydb_driver import get_database


def get_room_devices(room_name: str) -> Result:
    devices_db = get_database().table('devices')
    room_devices = devices_db.search(Query().room_name == room_name)
    return Result(success=room_devices)


def get_device(device_name: str) -> Result:
    devices_db = get_database().table('devices')
    target_device = devices_db.search(Query().device_name == device_name)
    if not target_device:
        return Result(status_code=404, error='Device not Found')
    return Result(success=target_device)


def get_temp_humd_devices() -> Result:
    devices_db = get_database().table('devices')
    temp_humd_devices = devices_db.search((Query().device_type == 'TEMP') | (Query().device_type == 'HUMD'))
    return Result(success=temp_humd_devices)
