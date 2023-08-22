import requests


BASE_AUTH = "http://127.0.0.1:5000"

# payload = {
#     "first_name": "Courier1",
#     "last_name": "Morrison",
#     "email": "god@27.com",
#     "gender": "male",
#     "language": "english",
#     "position": "weird?",
# }

def main():
    send_register_customer()
    send_register_courier()
    access_token = send_login_courier()
    access_token = send_login_courier_again(access_token)
    send_delete_courier_no_header(access_token)
    send_delete_courier(access_token)


def send_register_customer():
    payload = {
        "forename": "Customer1",
        "surname": "Morrison",
        "email": "god@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE_AUTH + '/register_customer',
        json=payload
    )

    print(response)
    print(response.text)
    # print(response.json())


def send_register_courier():
    payload = {
        "forename": "Courier1",
        "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE_AUTH + '/register_courier',
        json=payload
    )

    print(response)
    print(response.text)
    # print(response.json())


def send_login_courier():
    payload = {
        # "forename": "Courier1",
        # "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE_AUTH + '/login',
        json=payload
    )

    print(response)
    print(response.text)
    # print(response.json())

    return response.json()["accessToken"]


def send_login_courier_again(access_token):
    payload = {
        # "forename": "Courier1",
        # "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    response = requests.post(
        url=BASE_AUTH + '/login',
        json=payload,
        headers=headers
    )

    print(response)
    print(response.text)
    # print(response.json())

    return response.json()["accessToken"]


def send_delete_courier_no_header(access_token):
    payload = {
        # "forename": "Courier1",
        # "surname": "Morrison",
        "email": "go2d@27.com",
        "password": "heaven12"
    }

    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE_AUTH + '/delete',
        json=payload
    )

    print(response)
    print(response.text)
    # print(response.json())


def send_delete_courier(access_token):
    print(f'Trying access token: {access_token}')
    payload = {
        # "forename": "Courier1",
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
        url=BASE_AUTH + '/delete',
        json=payload,
        headers=headers
    )

    print(response)
    print(response.text)
    # print(response.json())



if __name__ == "__main__":
    main()
