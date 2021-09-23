import unittest

import yaml

import update_tag


class TestProposePr(unittest.TestCase):
    test_suite = [
        {
            "path": "yaml_tests/grafana.yaml",
            "key": "default.grafana_image",
            "value": "10.1.1",
        },
        {
            "path": "yaml_tests/carbonapi.yaml",
            "key": "carbonapi_image",
            "value": "1.1.1",
        },
        {
            "path": "yaml_tests/k8s-controller.yaml",
            "key": "document_hosting_instances.main.image",
            "value": "8.3.5",
        },
    ]

    def test_change_variable(self):
        for case in self.test_suite:
            with open(case["path"]) as f:
                yaml_data = yaml.safe_load(f)

            accessible = yaml_data
            keys = case["key"].split(".")
            for k in keys[:-1]:
                accessible = accessible[k]
            result_and_tag = accessible[keys[-1]].split(":")
            assert result_and_tag[1] != case["value"]

            update_tag.update_yaml_value(yaml_data, case["key"], case["value"])

            accessible = yaml_data
            keys = case["key"].split(".")
            for k in keys[:-1]:
                accessible = accessible[k]
            result_and_tag = accessible[keys[-1]].split(":")
            assert result_and_tag[1] == case["value"]
