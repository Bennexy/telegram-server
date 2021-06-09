from os import getenv as env
from dotenv import find_dotenv, load_dotenv

ENV_FILE = find_dotenv()

if ENV_FILE:
    load_dotenv(ENV_FILE)




ServerUrl = env("ServerUrl")


