import random
import requests
from faker import Faker

for i in range(50):
    faker = Faker()

    random_note = faker.sentence(nb_words=6)
    random_initial_value = round(random.uniform(50, 500), 2)
    random_code = faker.bothify(text='???? ???? ???? ????', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    random_template_suffix = 'gift_cards.' + random.choice(['birthday', 'holiday', 'thankyou', 'special']) + '.liquid'

    data = {
        "note": random_note,
        "initial_value": f"{random_initial_value:.2f}",
        "code": random_code,
        "template_suffix": random_template_suffix
    }

    url = "http://localhost:8002/admin/api/2024-06/gift_cards.json"
    response = requests.post(url, json=data)

    print(response.status_code)
    print(response.json())
