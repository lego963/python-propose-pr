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

    proposal_branch_name = get_proposal_branch_name(args.key)

    checkout_proposal_branch(proposal_branch_name, args.path)


def get_proposal_branch_name(key: str):
    return key.split(".")[-1]


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
    commit = repo.index.commit(f"test commit in {branch_name}")


if __name__ == "__main__":
    sys.exit(main())
