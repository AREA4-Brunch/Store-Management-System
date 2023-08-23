import requests
import os


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
    products_to_add = [
        'cat1|cat2,Product Name3,2500',
        'cat2,Product Name2,1000',
    ]

    path_tmp_file = 'tmp.csv'
    with open(path_tmp_file, 'w') as file:
        file.write('\n'.join(products_to_add))

    payload = {
        
    }

    files = {
        'file': open('tmp.csv', 'rb')
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    print('\n\nSent create_product:')

    response = requests.post(
        url=BASE_OWNERS + '/update',
        data=payload,
        headers=headers,
        files=files
    )

    print(response)
    print(response.text)
    # print(response.json())
    os.remove(path_tmp_file)

    return





if __name__ == '__main__':
    main()
