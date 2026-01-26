import json
import time
import pytest

from playwright.sync_api import Page, expect


def test_homepage(page:Page):
    page.goto("http://127.0.0.1:5001/")

    expect(page.locator(".lead")).to_be_visible()



def test_loginButton_present(page:Page):
    page.goto("http://127.0.0.1:5001/")
    expect(page.get_by_role("link",name="Login")).to_be_visible()
    time.sleep(5)

def test_resgisterButton_present(page:Page):
    page.goto("http://127.0.0.1:5001/")
    expect(page.get_by_role("link",name="Register")).to_be_visible()
    time.sleep(5)

@pytest.mark.order(1)
@pytest.mark.dependency(name="register")
def test_registration_Positive(page:Page):
    page.goto("http://127.0.0.1:5001/")
    with open('data/credentials.json') as f:
        test_data = json.load(f)
    #timestamp = int(time.time())
    #username = f"register_user_{timestamp}"
    page.get_by_role("link",name="Register").click()
    expect(page.get_by_role("heading",name="Register")).to_be_visible()
    page.locator('input[name="username"]').fill(test_data["user_crendentials"]["userName"])
    page.locator('input[name="password"]').fill(test_data["user_crendentials"].get("userPassword"))
    page.locator('input[name="confirm_password"]').fill(test_data["user_crendentials"].get("userPassword"))
    page.get_by_role("button",name="Register").click()
    time.sleep(5)

@pytest.mark.order(2)
@pytest.mark.dependency(depends=["register"])
def test_login_Page(page: Page):
    # Setup: Ensure the user exists for this specific test
    with open("data/credentials.json") as f:
        test_data=json.load(f)

    userName=test_data["user_crendentials"]["userName"]
    userPassword=test_data["user_crendentials"]["userPassword"]



    page.goto("http://127.0.0.1:5001/")


    time.sleep(4)
    # Action: Perform Login
    page.goto("http://127.0.0.1:5001/")
    page.get_by_role("link", name="Login").click()
    expect(page.get_by_role("heading", name="Login")).to_be_visible()
    page.locator('input[name="username"]').fill(userName)
    page.locator('input[name="password"]').fill(userPassword)
    page.get_by_role("button", name="Login").click()
    page.wait_for_load_state("networkidle")
    # Assert
    expect(page.get_by_text("Beverage Catalogue", exact=True)).to_be_visible()








