import requests as r


link = "http://localhost:8080/"


def add_account(request):
    request_data = request.data
    account_details = {
        "name": request_data['name'],
        "surname": request_data['surname'],
        "email": request_data['email'],
        "dob": request_data['dob']
    }
    response = r.post(link + "account/new", json=account_details)
    return response


def get_account_by_email(email):
    response = r.get(link+f"account?email={email}")
    return response


def get_all_accounts():
    response = r.get(link+"account/all")
    return response


def delete_account(id):
    response = r.delete(link+f"account/delete/{id}")
    return response
