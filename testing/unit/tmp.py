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
    # send_register_customer()
    send_register_courier()
    access_token = send_login_courier()
    send_delete_courier_no_header(access_token)
    send_delete_courier(access_token)


def send_register_customer():
    payload = {
        "forename": "Jim",
        "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE + '/register_customer',
        data=payload
    )

    print(response)
    print(response.text)
    # print(response.json())


def send_register_courier():
    payload = {
        "forename": "Jim",
        "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE + '/register_courier',
        data=payload
    )

    print(response)
    print(response.text)
    # print(response.json())


def send_login_courier():
    payload = {
        # "forename": "Jim",
        # "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE + '/login',
        data=payload
    )

    print(response)
    print(response.text)
    # print(response.json())

    return response.json()["accessToken"]


def send_delete_courier_no_header(access_token):
    payload = {
        # "forename": "Jim",
        # "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE + '/delete',
        data=payload
    )

    print(response)
    print(response.text)
    # print(response.json())


def send_delete_courier(access_token):
    print(f'Trying access token: {access_token}')
    payload = {
        # "forename": "Jim",
        # "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    headers = {
        # 'accept': 'application/json',
        # 'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(
        url=BASE + '/delete',
        data=payload,
        headers=headers
    )

    print(response)
    print(response.text)
    # print(response.json())



if __name__ == "__main__":
    main()
