import requests
from faker import Faker
import random

for i in range(50):
    faker = Faker()

    random_title = faker.sentence(nb_words=3)
    random_price = round(random.uniform(20, 200), 2)
    random_grams = random.randint(500, 3000)
    random_quantity = random.randint(1, 10)
    random_tax_price = round(random_price * 0.06, 2)

    random_transaction_amount = round(random_price * random_quantity + random_tax_price, 2)

    data = {
        "order": {
            "line_items": [
                {
                    "title": random_title,
                    "price": random_price,
                    "grams": random_grams,
                    "quantity": random_quantity,
                    "tax_lines": [
                        {
                            "price": random_tax_price,
                            "rate": 0.06,
                            "title": "State tax"
                        }
                    ]
                }
            ],
            "transactions": [
                {
                    "kind": "sale",
                    "status": "success",
                    "amount": random_transaction_amount
                }
            ],
            "total_tax": random_tax_price,
            "currency": "EUR"
        }
    }

    url = "http://localhost:8002/admin/api/2024-06/orders.json"
    response = requests.post(url, json=data)

    print(response.text)
    print(response.status_code)
    print(response.json())
