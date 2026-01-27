import json

#with open('credentials.json') as f:
    #test_data = json.load(f)
    #print(test_data["user_crendentials"]["userName"])

with open(f"data/carddetails.json")as f:
    card_details = json.load(f)
    print(card_details["card_details"]["cardNumber"])


        #page.get_by_placeholder("Enter card number").fill(card_details["cardNumber"])
        #page.get_by_placeholder("MM/YY").fill(card_details["expiry"])
        #page.locator('input[name="cvv"]').fill(card_details["cvv"])
        #time.sleep(5)
