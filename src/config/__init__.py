import pathlib
import json

with open(pathlib.Path(__file__).parent / "env.json") as f:
    env = json.load(f)


def logging_config(log_file):
    logging_config = env["logging_config"]
    logging_config["handlers"]["file"]["filename"] = pathlib.Path(env["log_path"]) / log_file
    return logging_config
