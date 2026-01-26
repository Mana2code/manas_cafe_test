import json
import time
import pytest

from playwright.sync_api import Page, expect

def test_homepage(page:Page):
    page.goto("http://127.0.0.1:5001/")

    expect(page.locator(".lead")).to_be_visible()

def test_login_Page(page: Page):
    page.goto("http://127.0.0.1:5001/")
    with open("data/credentials.json") as f:
        test_data=json.load(f)
        page.get_by_role("link",name="Login").click()
        userName = test_data["user_crendentials"]["userName"]
        userPassword = test_data["user_crendentials"]["userPassword"]
        page.locator('input[name="username"]').fill(userName)
        page.locator('input[name="password"]').fill(userPassword)
        time.sleep(3)
        page.get_by_role("button",name="Login").click()
        #expect(page.get_by_text("Beverage Catalogue")).to_be_visible()
        time.sleep(2)



