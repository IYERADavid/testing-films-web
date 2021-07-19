from os import environ

def get_env(name):
    env_value = environ.get(name)
    return env_value
