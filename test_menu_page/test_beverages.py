import json
import time
import pytest

from playwright.sync_api import Page, expect

def test_homepage(page:Page):
    page.goto("http://127.0.0.1:5001/")

    expect(page.locator(".lead")).to_be_visible()