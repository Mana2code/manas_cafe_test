import json

import pytest


@pytest.fixture
def login(page):
    page.goto("http://127.0.0.1:5001/")
    with open("data/credentials.json") as f:
        test_data = json.load(f)
        page.get_by_role("link", name="Login").click()
        page.locator('input[name="username"]').fill(test_data["user_crendentials"]["userName"])
        page.locator('input[name="password"]').fill(test_data["user_crendentials"]["userPassword"])
        page.get_by_role("button", name="Login").click()

        yield

