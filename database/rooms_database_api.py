from tinydb import Query
from models.runtime import Result
from database.tinydb_driver import get_database


def get_rooms() -> Result:
    rooms_db = get_database().table('rooms')
    rooms = rooms_db.all()

    # get each room global sensor list
    for room in rooms:
        devices_db = get_database().table('devices')
        query = ((Query().device_type == 'TEMP') | (Query().device_type == 'HUMD')) & (Query().room_name == room['room_name'])
        device_names = [x['device_name'] for x in devices_db.search(query)]
        room['global_sensors_list'] = device_names

    return Result(success=rooms)
