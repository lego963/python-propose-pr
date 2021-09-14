import argparse
import sys

import requests
import yaml


class GitProposePr:
    author = "lego963"
    repo = "python-propose-pr"
    api_repo_url = "https://api.github.com/repos"

    def __init__(self, path: str, key: str, value: str, token: str):
        self.path = path
        self.key = key.split("."),
        self.value = value
        self.token = token

    def update_yaml_file(self, yaml_data):
        accessible = yaml_data
        for k in self.key[:-1]:
            accessible = accessible[k]
        url_tag = accessible[self.key[-1][0]].split(":")
        accessible[self.key[-1][0]] = f"{url_tag[0]}:{self.value}"

    def open_yaml(self):
        with open(self.path) as f:
            return yaml.safe_load(f)

    def save_yaml(self, yaml_data):
        with open(self.path, "w") as f:
            return yaml.safe_dump(yaml_data, f)

    def create_gh_branch(self):
        get_refs_head = requests.request(
            method="GET",
            url="/".join((
                self.api_repo_url,
                self.author,
                self.repo,
                "git",
                "refs",
                "heads",
            ))
        )
        if get_refs_head.status_code not in [200]:
            return f"Cannot get refs of {self.author}/{self.repo}: {get_refs_head.status_code}"

        main_branch_sha = ""
        for branch in get_refs_head.json():
            if branch["ref"] == "refs/heads/main":
                main_branch_sha = branch["object"]["sha"]

        if main_branch_sha == "":
            return "SHA of `main` branch wasn't found"

        data = {
            "ref": f"refs/heads/{self.key[-1][0]}-{self.value}",
            "sha": main_branch_sha,
        }
        headers = {
            "Authorization": f"token {self.token}"
        }
        create_new_branch = requests.request(
            method="POST",
            url="/".join((
                self.api_repo_url,
                self.author,
                self.repo,
                "git",
                "refs"
            )),
            json=data,
            headers=headers,
        )
        if create_new_branch.status_code not in [201]:
            return f"Failed to create proposal branch: {create_new_branch.status_code}"


def main():
    parser = argparse.ArgumentParser(prog="update-tag", description="Simple script for updating a tag in YAML")
    parser.add_argument("--path", type=str, help="Path to yaml file", required=True)
    parser.add_argument("--key", type=str, help="Which key should be updated", required=True)
    parser.add_argument("--value", type=str, help="New tag value", required=True)
    parser.add_argument("--token", type=str, help="GitHub token")
    args = parser.parse_args()

    proposePr = GitProposePr(args.path, args.key, args.value, args.token)
    yaml_data = proposePr.open_yaml()
    proposePr.update_yaml_file(yaml_data)
    some_data = proposePr.save_yaml(yaml_data)

    proposePr.create_gh_branch()


if __name__ == "__main__":
    sys.exit(main())
