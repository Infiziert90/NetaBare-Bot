import os
import logging
import configparser


class AttrDict(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__dict__ = self

    def update(self, *d, **kwargs):
        for key, val in (d[0] if d else kwargs).items():
            setattr(self, key, val)

    def __getattr__(self, item):
        # expected behaviour:
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {item}")


config = AttrDict()
def load_config():
    ini_conf = configparser.ConfigParser()
    ini_conf.read(["bot.ini"])

    for key, val in ini_conf.items():
        if isinstance(val, (dict, configparser.SectionProxy)):
            val = AttrDict(val)
        config[key] = val

    debug = int(config.MAIN.get("debug", 0))
    if debug:
        os.environ["PYTHONASYNCIODEBUG"] = "1"

    if debug >= 3:
        log_level = logging.DEBUG
    elif debug >= 2:
        log_level = logging.INFO
    else:
        log_level = logging.WARNING

    logging.basicConfig(level=log_level)
    logging.getLogger('').addHandler(logging.FileHandler("output.log"))
    # suppress poll infos from asyncio
    logging.getLogger('asyncio').setLevel(logging.WARNING)


load_config()

__all__ = ['config']
