import requests


BASE = "http://127.0.0.1:5000"

# payload = {
#     "first_name": "Jim",
#     "last_name": "Morrison",
#     "email": "god@27.com",
#     "gender": "male",
#     "language": "english",
#     "position": "weird?",
# }

def main():
    add_products()


def add_products():
    payload = {
        "forename": "Jim",
        "surname": "Morrison",
        "email": "god@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE + '/update',
        data=payload
    )

    print(response)
    print(response.text)
    # print(response.json())


if __name__ == '__main__':
    main()
