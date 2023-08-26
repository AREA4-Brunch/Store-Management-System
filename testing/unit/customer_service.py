import requests
import os


BASE_AUTH = "http://127.0.0.1:5000"
BASE_CUSTOMERS = "http://127.0.0.1:5002"



def main():
    test1()

    return



def test1():
    access_token = send_login_customer()
    print(f'Access token for customer: {access_token}')

    search(access_token, 'am', 'cat')
    search(access_token, '', 'cat')
    search(access_token, '', '2')
    search(access_token, '', '1')
    search(access_token, '2', '2')

    return


def send_login_customer():
    """
        email="onlymoney@gmail.com",
        forename='Scrooge',
        surname='McDuck',
        password='evenmoremoney'
    """
    payload = {
        # "forename": "Customer1",
        # "surname": "Morrison",
        "email": "god@27.com",
        "password": "heaven12"
    }

    print('Logging in as customer:')
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


def search(access_token, product_name, category_name):
    # products_to_add = [
    #     'cat1|cat2,Product Name3,2500',
    #     'cat2,Product Name2,1000',
    # ]

    payload = {
        
    }

    files = {
    }

    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    search_str = f'/search?name={product_name}&category={category_name}'
    print(f'\n\nSearching: {search_str}')

    response = requests.post(
        url=BASE_CUSTOMERS + search_str,
        data=payload,
        headers=headers,
        files=files
    )

    print(response)
    print(response.text)
    # print(response.json())

    return





if __name__ == '__main__':
    main()
