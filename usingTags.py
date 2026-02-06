from playwright.sync_api import expect


def test_loginPage(page,login):
    expect(page.get_by_text("Beverage Catalogue")).to_be_visible()




