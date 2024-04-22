# autopep8: off
import os
import sys
import jwt
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
# autopep8: on

isi_server_nodered_user = User(
    username='isi_server_nodered',
    disp_name='ISI Server NodeRED',
    user_role=UserRole.USER,
    pass_hash='',
    phone_number='+201012345678',
    email='isi_server_nodered@isi.dev',
)

print(jwt.encode({
    'username': isi_server_nodered_user.username,
    'display_name': isi_server_nodered_user.disp_name,
    'role': isi_server_nodered_user.user_role,
}, os.environ['JWT_KEY'], algorithm='HS512'))
