import json

from playwright.sync_api import expect


def test_loginPage(page,login):
    expect(page.get_by_text("Beverage Catalogue")).to_be_visible()

def test_logoutPage(page,login):
    #expect(page.get_by_text("Beverage Catalogue")).to_be_visible()
    coffeeTest = page.locator(".card").filter(has_text="Coffee")
    coffeeTest.get_by_role("button", name="Add to Cart").click()
    latteTest = page.locator(".card").filter(has_text="Latte")
    latteTest.get_by_role("button", name="Add to Cart").click()
    page.get_by_role("link", name="Cart").click()
    page.get_by_role("link", name="Checkout").click()
    with open("data/carddetails.json") as f:
        cards = json.load(f)

    page.get_by_placeholder("Enter card number").fill(cards["card_details"]["cardNumber"])
    page.get_by_placeholder("MM/YY").fill(cards["card_details"]["expiry"])
    page.locator('input[name="cvv"]').fill(cards["card_details"]["cvv"])
    page.get_by_role("button", name="Checkout").click()
    expect(page.get_by_text("My Orders")).to_be_visible()
    page.get_by_role("link", name="Logout").click()
    expect(page.get_by_text("Welcome to Mana's Cafe ☕")).to_be_visible()





