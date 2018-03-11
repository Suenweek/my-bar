import os
import pytest


@pytest.mark.parametrize("resource_filename", [
    "ingredients.json",
    "recipes.json"
])
def test_resources_are_ascii(config, resource_filename):
    resource_path = os.path.join(config.RESOURCES_DIR, resource_filename)
    with open(resource_path) as f:
        assert is_ascii(f.read())


def is_ascii(string):
    return all(ord(char) < 128 for char in string)
