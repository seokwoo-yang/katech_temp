import pathlib
import json
import os

FB_ENV = os.getenv("FB_ENV", "dev")

with open(pathlib.Path(__file__).parent / "env.json") as f:
    env = json.load(f)


def logging_config(log_file):
    logging_config = env["logging_config"]
    logging_config["handlers"]["file"]["filename"] = pathlib.Path(env[FB_ENV]["log_path"]) / log_file
    return logging_config
