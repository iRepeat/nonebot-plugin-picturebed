import uuid
from datetime import datetime


async def generate_file_name(extend, way="uuid"):
    """ 根据当前datetime或uuid生成文件名. """
    if way == "datetime":
        now = datetime.now()
        return datetime.strftime(now, "%Y%m%d%H%M%S") + "." + extend
    if way == "uuid":
        var = uuid.uuid4().hex
        return var + "." + extend

    return None
