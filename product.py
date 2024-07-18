import random
import requests
from faker import Faker

for x in range(50):
    faker = Faker()

    random_title = faker.text(max_nb_chars=20)
    random_body_html = f"<strong>{faker.catch_phrase()}!</strong>"
    random_vendor = faker.company()
    random_product_type = random.choice(["Electronics", "Snowboard", "Furniture", "Clothing"])
    random_status = "draft"

    data = {
        "title": random_title,
        "body_html": random_body_html,
        "vendor": random_vendor,
        "product_type": random_product_type,
        "status": random_status
    }

    url = "http://localhost:8002/admin/api/2024-06/products.json"
    response = requests.post(url, json=data)

    print(response.status_code)
    print(response.json())
