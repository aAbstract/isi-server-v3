from tinydb import Query
from lib.crypto import hash_password, create_jwt_token
from models.runtime import Result
from database.tinydb_driver import get_database
from models.users import User


def login_user(username: str, password: str) -> Result:
    # check user in database
    users_db = get_database().table('users')
    user = users_db.search(Query().username == username)
    if not user:
        return Result(status_code=401, error='Login Failed, Invalid User Credentials')

    # check password hash
    user = User.model_validate(user[0])
    password_hash = hash_password(password)
    if password_hash != user.pass_hash:
        return Result(status_code=401, error='Login Failed, Invalid User Credentials')

    # create jwt token
    jwt_token = create_jwt_token({
        'username': user.username,
        'display_name': user.disp_name,
        'role': user.user_role,
    })
    return Result(success={'access_token': jwt_token})
