from datetime import date

import pytest
from flask_sqlalchemy.session import Session

from app import app
from app import User, Credit, Creditor, StatusField

user_info = {
    "first_name": "play",
    "last_name": "boy",
    "password": "karl220",
    "email": "playboy@gmail.com",
    "phone": "+380930232722",
    "status": 'paid'
}

user_info1 = {
    "first_name": "play",
    "last_name": "boy",
    "password": "karl220",
    "email": "playbasdoy@gmail.com",
    "phone": "+380930232722",
    "status": 'paid'
}

credit_info = {
    "sum_of_credit": 10000,
    "percent_of_credit": 0.05,
    "user_id": 12,
    "creditor_id": 12,
    "status": "paid"
}

credit_info1 = {
    "sum_of_credit": 10000,
    "percent_of_credit": 0.05,
    "user_id": 12,
    "creditor_id": 12,
    "status": "paid"
}


creditor_info = {
    "name": "Rodriguez",
    "budget": 12000,
    "phone": "12325"
}

creditor_info1 = {
    "name": "boy",
    "phone": "+380930232722",
    "budget": 10000
}


class TestUser:

    def test_user_update_by_id(self):
        response = app.test_client().post('/api/v1/user', json=user_info)

        user_id = response.json['user_id']
        response = app.test_client().put(f'/api/v1/user/{user_id}', json={"first_name": "new8"})

        assert response.status_code == 200

    def test_user_create(self):
        response = app.test_client().post('/api/v1/user', json=user_info)
        assert response.status_code == 200

    def test_get_users(self):
        response = app.test_client().get('/api/v1/users')
        assert response.status_code == 200

    def test_user_delete_by_id(self):
        response = app.test_client().post('/api/v1/user', json=user_info)
        user_id = response.json['user_id']

        response = app.test_client().delete(f'/api/v1/user/{user_id}')

        assert response.status_code == 200
        assert response.data == b"User deleted"

    def test_user_get_by_id(self):
        response = app.test_client().post('/api/v1/user', json=user_info1)
        user_id = response.json['user_id']
        response = app.test_client().get(f'/api/v1/user/{user_id}')

        assert response.status_code == 200


class TestCredit:

    def test_credit_update_by_id(self):
        response = app.test_client().post('/api/v1/credit', json=credit_info)

        print(response.json)
        credit_id = response.json['credit_id']
        response = app.test_client().put(f'/api/v1/credit/{credit_id}', json={"first_name": "new8"})

        assert response.status_code == 200

    def test_credit_create(self):
        response = app.test_client().post('/api/v1/credit', json=credit_info)
        assert response.status_code == 200

    def test_get_credits(self):
        response = app.test_client().get('/api/v1/credits')
        assert response.status_code == 200

    def test_credit_delete_by_id(self):
        response = app.test_client().post('/api/v1/credit', json=credit_info)
        credit_id = response.json['credit_id']

        response = app.test_client().delete(f'/api/v1/credit/{credit_id}')

        assert response.status_code == 200
        assert response.data == b"Credit deleted"

    def test_credit_get_by_id(self):
        response = app.test_client().post('/api/v1/credit', json=credit_info1)
        credit_id = response.json['credit_id']
        response = app.test_client().get(f'/api/v1/credit/{credit_id}')

        assert response.status_code == 200


class TestCreditor:

    def test_creditor_update_by_id(self):
        response = app.test_client().post('/api/v1/creditor', json=creditor_info)

        creditor_id = response.json['creditor_id']
        response = app.test_client().put(f'/api/v1/creditor/{creditor_id}', json={"first_name": "new8"})

        assert response.status_code == 200

    def test_creditor_create(self):
        response = app.test_client().post('/api/v1/creditor', json=creditor_info)
        assert response.status_code == 200

    def test_get_creditors(self):
        response = app.test_client().get('/api/v1/credits')
        assert response.status_code == 200

    def test_creditor_delete_by_id(self):
        response = app.test_client().post('/api/v1/creditor', json=creditor_info)
        creditor_id = response.json['creditor_id']

        response = app.test_client().delete(f'/api/v1/creditor/{creditor_id}')

        assert response.status_code == 200
        assert response.data == b"Creditor deleted"

    def test_creditor_get_by_id(self):
        response = app.test_client().post('/api/v1/creditor', json=creditor_info1)
        creditor_id = response.json['creditor_id']
        response = app.test_client().get(f'/api/v1/creditor/{creditor_id}')

        assert response.status_code == 200


