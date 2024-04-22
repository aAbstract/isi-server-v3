from models.runtime import Result
from database.tinydb_driver import get_database


def get_rooms() -> Result:
    rooms_db = get_database().table('rooms')
    return Result(success=rooms_db.all())
