import importlib


def get_config(env):
    mod_name = "src.config.{}".format(env)
    return importlib.import_module(mod_name)
