from uuid import uuid4
from enum import Enum
from pydantic import BaseModel, ConfigDict


class Room(BaseModel):
    id: str = None
    room_name: str
    room_icon: str = None
    room_disp_name: str = None

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid4())
        if not self.room_icon:
            self.room_icon = '_'.join(self.room_name.split('_')[:-1])
        if not self.room_disp_name:
            self.room_disp_name = ' '.join([word.capitalize() for word in self.room_name.split('_')[:-1]])


class DeviceType(Enum):
    SWITCH = 'SWITCH'
    HUMD = 'HUMD'
    TEMP = 'TEMP'
    PLUG = 'PLUG'
    RGB = 'RGB'
    SEC_LOCK = 'SEC_LOCK'
    FLOOD = 'FLOOD'
    MOTION = 'MOTION'
    DIMMER = 'DIMMER'


class DeviceLinkType(Enum):
    LIVE = 'LIVE'
    SUSPEND = 'SUSPEND'


class DeviceConfig(BaseModel):
    config_name: str
    config_disp_name: str
    config_val: bool = False


class Device(BaseModel):
    id: str = None
    device_name: str
    room_name: str = 'living_room_0'
    device_type: DeviceType
    link_type: DeviceLinkType = DeviceLinkType.LIVE
    device_config: list[DeviceConfig] = []
    is_online: bool = False

    model_config = ConfigDict(use_enum_values=True)

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid4())


class DeviceAction(BaseModel):
    device_name: str
    device_pref: str
    payload: str


class Scene(BaseModel):
    id: str = None
    scene_disp_name: str
    actions: list[DeviceAction] = []

    def __init__(self, **data):
        super().__init__(**data)
        self.id = str(uuid4())
