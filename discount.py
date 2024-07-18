import requests
import random
import string
from faker import Faker
for i in range(50):
    faker = Faker()

    def random_price_rule_id(length=9):
        return ''.join(random.choices(string.digits, k=length))

    random_price_rule_id = random_price_rule_id()
    random_discount_code = faker.bothify(text='????SALE##OFF', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    data = {
        "discount_code": {
            "code": random_discount_code
        }
    }

    url = f"http://localhost:8002/admin/api/2024-06/price_rules/{random_price_rule_id}/discount_codes.json"
    response = requests.post(url, json=data)

    print(response.status_code)
    print(response.json())
