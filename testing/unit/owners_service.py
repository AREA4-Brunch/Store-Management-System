import requests


BASE_AUTH = "http://127.0.0.1:5000"
BASE_OWNERS = "http://127.0.0.1:5001"



def main():
    test1()

    return



def test1():
    access_token = send_login_owner()
    print(f'Access token for owner: {access_token}')

    create_product(access_token)

    return


def send_login_owner():
    """
        email="onlymoney@gmail.com",
        forename='Scrooge',
        surname='McDuck',
        password='evenmoremoney'
    """
    payload = {
        # "forename": "Jim",
        # "surname": "Morrison",
        "email": "onlymoney@gmail.com",
        "password": "evenmoremoney"
    }

    print('Logging in as owner:')
    # headers = {'accept': 'application/json'}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(
        url=BASE_AUTH + '/login',
        json=payload,
    )

    print(response)
    print(response.text)
    # print(response.json())

    return response.json()["accessToken"]


def create_product(access_token):
    payload = {
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    print('\n\nSent create_product:')
    response = requests.post(
        url=BASE_OWNERS + '/update',
        data=payload,
        headers=headers
    )

    print(response)
    print(response.text)
    # print(response.json())

    return





if __name__ == '__main__':
    main()
