import requests
import random
from faker import Faker

faker = Faker()
for i in range(500):
    random_name = faker.company()
    random_price = int(round(random.uniform(10, 500), 2))
    random_return_url = faker.url().rstrip('/')
    data = {
        "application_charge": {
            "name": random_name,
            "price": random_price,
            "return_url": random_return_url,
            "test": True
        }
    }

    url = "http://localhost:8002/admin/api/2024-06/application_charges.json"
    response = requests.post(url, json=data)

    print(data)
    print(response.text)
    print(response.status_code)
    print(response.json())
