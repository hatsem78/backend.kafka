"""
Test main
"""
from fastapi.testclient import TestClient

import os

from . import settings
from app.main import app
settings.set_sys_path()


class TestItems:

    file = "test.tiff"
    client = TestClient(app)
    basedir = os.path.abspath(os.path.dirname(__file__))
    basedir_file = os.path.join(basedir, file)

    def test_hello(self) -> None:
        response = self.client.get("/items")

        assert response.json() == [{"name": "Item Foo"}, {"name": "item Bar"}]
        assert response.status_code == 200
