import json
import pytest

# Load test data once
with open("data/credentials.json") as f:
    test_data = json.load(f)
user_credentials = test_data["user_credentials"]

@pytest.fixture
def login(page):
    page.goto("http://127.0.0.1:5001/")
    page.get_by_role("link", name="Login").click()

    page.locator('input[name="username"]').fill(user_credentials["userName"])
    page.locator('input[name="password"]').fill(user_credentials["userPassword"])

    page.get_by_role("button", name="Login").click()

    yield
