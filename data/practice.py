import json

with open('credentials.json') as f:
    test_data = json.load(f)
    print(test_data["user_crendentials"]["userName"])