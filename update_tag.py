import argparse

import yaml

_parser = argparse.ArgumentParser(prog="propose-pr", description="Propose PR to a GitHub")
_parser.add_argument("--path", type=str, help="Vars file path", required=True)
_parser.add_argument("--key", type=str, help="Key to change", required=True)
_parser.add_argument("--value", type=str, help="New value of the key", required=True)


def main():
    args = _parser.parse_args()
    process_yaml(args.path, args.key, args.value)


def process_yaml(path: str, key: str, value: str):
    with open(path) as f:
        yaml_data = yaml.safe_load(f)

    update_yaml_value(yaml_data, key, value)

    with open(path, "w") as f:
        yaml.safe_dump(yaml_data, f)


def update_yaml_value(yaml_data, key: str, data: str):
    keys = key.split(".")
    accessible = yaml_data
    for k in keys[:-1]:
        accessible = accessible[k]
    url_tag = accessible[keys[-1]].split(":")
    accessible[keys[-1]] = "{url}:{tag}".format(url=url_tag[0], tag=data)


if __name__ == "__main__":
    main()
