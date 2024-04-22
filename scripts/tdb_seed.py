# autopep8: off
import os
import sys
from tinydb import TinyDB
from dotenv import load_dotenv
def load_root_path():
    file_dir = os.path.abspath(__file__)
    lv1_dir = os.path.dirname(file_dir)
    root_dir = os.path.dirname(lv1_dir)
    sys.path.append(root_dir)

load_root_path()
load_dotenv()
# routes
from models.users import *
from models.iot import *
from lib.crypto import *
# autopep8: on

if os.path.exists(os.environ['TDB_DEV_PATH']):
    os.remove(os.environ['TDB_DEV_PATH'])
tinydb = TinyDB(os.environ['TDB_DEV_PATH'])

seed_users = [
    User(
        username='test_admin',
        disp_name='Test Admin',
        user_role=UserRole.ADMIN,
        pass_hash=hash_password('TzQbMhHbZNXDJxpliqWNbtVAtc9r7Q33'),
        phone_number='+201012345678',
        email='test_admin@isi.dev',
    ),
    User(
        username='test_user',
        disp_name='Test User',
        user_role=UserRole.USER,
        pass_hash=hash_password('upass123'),
        phone_number='+201012345678',
        email='test_user@isi.dev',
    ),
]

seed_rooms = [
    Room(room_name='living_room_0'),
    Room(room_name='bedroom_0'),
    Room(room_name='children_room_0'),
    Room(room_name='dining_room_0'),
    Room(room_name='kichen_0'),
    Room(room_name='gym_0'),
    Room(room_name='garden_0'),
    Room(room_name='office_0'),
    Room(room_name='tv_room_0'),
]

seed_devices = [
    Device(
        device_name='main_switch_0',
        device_type=DeviceType.SWITCH,
        link_type=DeviceLinkType.LIVE,
    ),
    Device(
        device_name='main_switch_1',
        device_type=DeviceType.SWITCH,
        link_type=DeviceLinkType.LIVE,
    ),
    Device(
        device_name='main_humidity_sensor_0',
        device_type=DeviceType.HUMD,
        link_type=DeviceLinkType.LIVE,
    ),
    Device(
        device_name='main_temperature_sensor_0',
        device_type=DeviceType.TEMP,
        link_type=DeviceLinkType.LIVE,
    ),
    Device(
        device_name='main_plug_0',
        device_type=DeviceType.PLUG,
        link_type=DeviceLinkType.LIVE,
    ),
    Device(
        device_name='main_rgb_0',
        device_type=DeviceType.RGB,
        link_type=DeviceLinkType.LIVE,
    ),
    Device(
        device_name='security_lock_0',
        device_type=DeviceType.SEC_LOCK,
        link_type=DeviceLinkType.SUSPEND,
    ),
    Device(
        device_name='flood_sensor_0',
        device_type=DeviceType.FLOOD,
        link_type=DeviceLinkType.SUSPEND,
    ),
    Device(
        device_name='motion_sensor_0',
        device_type=DeviceType.MOTION,
        link_type=DeviceLinkType.LIVE,
        device_config=[
            DeviceConfig(config_name='light_mode', config_disp_name='Light Mode', config_val=True),
            DeviceConfig(config_name='sec_mode', config_disp_name='Security Mode', config_val=True),
        ],
    ),
    Device(
        device_name='main_dimmer_0',
        device_type=DeviceType.DIMMER,
        link_type=DeviceLinkType.LIVE,
    ),
    Device(
        device_name='bedroom_switch_0',
        device_type=DeviceType.SWITCH,
        link_type=DeviceLinkType.LIVE,
        room_name='bedroom_0',
    ),
]

seed_scenes = [
    Scene(
        scene_disp_name='Home Entrance',
        actions=[
            DeviceAction(
                device_name='main_switch_0',
                device_pref='power_0',
                payload='{"command":"TOGGLE"}',
            ),
            DeviceAction(
                device_name='main_dimmer_0',
                device_pref='dimmer_0',
                payload='{"command":"DIM_2"}',
            ),
        ],
    ),
    Scene(
        scene_disp_name='Bed Time',
        actions=[
            DeviceAction(
                device_name='main_switch_0',
                device_pref='power_0',
                payload='{"command":"TOGGLE"}',
            ),
            DeviceAction(
                device_name='main_switch_1',
                device_pref='power_0',
                payload='{"command":"TOGGLE"}',
            ),
            DeviceAction(
                device_name='main_dimmer_0',
                device_pref='dimmer_0',
                payload='{"command":"DIM_1"}',
            ),
        ],
    ),
]

if __name__ == '__main__':
    print('seeding users database...')
    users_db = tinydb.table('users')
    users_db.insert_multiple([x.model_dump() for x in seed_users])

    print('seeding iot system rooms...')
    rooms_db = tinydb.table('rooms')
    rooms_db.insert_multiple([x.model_dump() for x in seed_rooms])

    print('seeding iot system devices...')
    devices_db = tinydb.table('devices')
    devices_db.insert_multiple([x.model_dump() for x in seed_devices])

    print('seeding iot system scenes...')
    scenes_db = tinydb.table('scenes')
    scenes_db.insert_multiple([x.model_dump() for x in seed_scenes])
