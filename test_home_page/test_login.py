import time

from playwright.sync_api import Page, expect


def test_homepage(page:Page):
    page.goto("http://127.0.0.1:5001/")
    time.sleep(2)
    expect(page.locator(".lead")).to_be_visible()
    time.sleep(2)

def test_loginButton_present(page:Page):
    page.goto("http://127.0.0.1:5001/")
    expect(page.get_by_role("link",name="Login")).to_be_visible()
    time.sleep(5)

def test_resgisterButton_present(page:Page):
    page.goto("http://127.0.0.1:5001/")
    expect(page.get_by_role("link",name="Register")).to_be_visible()
    time.sleep(5)

def test_registration_Positive(page:Page):
    page.goto("http://127.0.0.1:5001/")
    timestamp = int(time.time())
    username = f"register_user_{timestamp}"
    page.get_by_role("link",name="Register").click()
    expect(page.get_by_role("heading",name="Register")).to_be_visible()
    page.locator('input[name="username"]').fill(username)
    page.locator('input[name="password"]').fill("Testing@12")
    page.locator('input[name="confirm_password"]').fill("Testing@12")
    page.get_by_role("button",name="Register").click()
    time.sleep(5)


def test_login_Page(page: Page):
    # Setup: Ensure the user exists for this specific test
    timestamp = int(time.time())
    username = f"login_user_{timestamp}"
    page.goto("http://0.0.0.0")
    page.locator('input[name="username"]').fill(username)
    page.locator('input[name="password"]').fill("Testing@12")
    page.locator('input[name="confirm_password"]').fill("Testing@12")
    page.get_by_role("button", name="Register").click()

    # Action: Perform Login
    page.goto("http://0.0.0.0")
    page.locator('input[name="username"]').fill(username)
    page.locator('input[name="password"]').fill("Testing@12")
    page.get_by_role("button", name="Login").click()

    # Assert
    expect(page.get_by_text("Beverage Catalogue", exact=True)).to_be_visible()








