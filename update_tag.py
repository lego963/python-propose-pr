import argparse
import os
import sys

import yaml
from git import Repo


def main():
    parser = argparse.ArgumentParser(prog="update-tag", description="Simple script for updating a tag in YAML")
    parser.add_argument("--path", type=str, help="Path to yaml file", required=True)
    parser.add_argument("--key", type=str, help="Which key should be updated", required=True)
    parser.add_argument("--value", type=str, help="New tag value", required=True)
    parser.add_argument("--token", type=str, help="Auth token")
    args = parser.parse_args()

    with open(args.path) as f:
        yaml_data = yaml.safe_load(f)

    update_yaml_value(yaml_data, args.key, args.value)

    with open(args.path, "w") as f:
        yaml.safe_dump(yaml_data, f)

    if args.token != "":
        proposal_branch = get_proposal_branch_name(args.key, args.value)
        checkout_proposal_branch(proposal_branch, args.path)


def get_proposal_branch_name(key: str, value: str):
    return f"{key.split('.')[-1]}-{value}"


def update_yaml_value(yaml_data, key: str, tag_value: str):
    keys = key.split(".")
    accessible = yaml_data
    for k in keys[:-1]:
        accessible = accessible[k]
    url_tag = accessible[keys[-1]].split(":")
    accessible[keys[-1]] = "{url}:{tag}".format(url=url_tag[0], tag=tag_value)


def checkout_proposal_branch(branch_name: str, changed_file_path: str):
    repo = Repo(os.getcwd())
    repo.git.checkout("-b", branch_name)
    repo.index.add([changed_file_path])
    repo.index.commit(f"Update image version of `{changed_file_path}`")


if __name__ == "__main__":
    sys.exit(main())
