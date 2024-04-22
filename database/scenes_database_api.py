from tinydb import Query
from models.runtime import Result
from database.tinydb_driver import get_database


def get_scenes_metadata() -> Result:
    scenes_db = get_database().table('scenes')
    scenes = scenes_db.all()
    for scene in scenes:
        del scene['actions']
    return Result(success=scenes)


def get_scene(scene_id: str) -> Result:
    scenes_db = get_database().table('scenes')
    scene = scenes_db.search(Query().id == scene_id)
    if not scene:
        return Result(status_code=404, error='Scene not Found')
    return Result(success=scene)
