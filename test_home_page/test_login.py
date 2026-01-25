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

def test_egistrationPositive(page:Page):
    page.goto("http://127.0.0.1:5001/")
    page.get_by_role("link",name="Register").click()
    expect(page.get_by_role("heading",name="Register")).to_be_visible()
    page.locator('input[name="username"]').fill("test")
    page.locator('input[name="password"]').fill("Testing@12")
    page.locator('input[name="confirm_password"]').fill("Testing@12")
    page.get_by_role("button",name="Register").click()
    time.sleep(5)

def test_login(page:Page):
    page.goto("http://127.0.0.1:5001/")
    page.get_by_role("link",name="Login").click()
    page.locator('input[name="username"]').fill("test")

    page.locator('input[name="password"]').fill("Testing@12")
    page.get_by_role("button",name="Login").click()
    expect(page.get_by_text("Beverage Catalogue",exact=True)).to_be_visible()
    time.sleep(5)








