from django.test import TestCase
from django.urls import reverse

import requests_mock

from .conf import HOST_URL_TRAIN
from .conf import HOST_URL_ORDER
from .conf import HOST_URL_BILLING

from .views import stopFlag

stopFlag.set()

@requests_mock.Mocker()
class TestAllViews(TestCase):

    def test_train_detail_get(self, m):
        train_id = 1
        free_places = 10
        train_mock = {
            "train_id": train_id,
            "ticket_count": 2,
            "from":"Пенза",
            "to": "Москва",
            "free_places": free_places
        }

        m.get(
            HOST_URL_TRAIN + 'trains/%s/' % train_id,
            headers = {"Content-Type":"application/json"},
            json = train_mock,
            status_code=200
        )

        response = self.client.get(reverse('servise:train-detail', kwargs={"train_id": train_id}))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 1)
        self.assertEqual(response.json(), train_mock)

    def test_trains_list_get(self, m):
        train_id = 1
        free_places = 10
        train_mock = [{
            "train_id": train_id,
            "ticket_count": 2,
            "from":"Пенза",
            "to": "Москва",
            "free_places": free_places
        }]

        m.get(
            HOST_URL_TRAIN + 'trains/',
            headers = {"Content-Type":"application/json"},
            json = train_mock,
            status_code=200
        )

        response = self.client.get(reverse('servise:trains-list'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 1)
        self.assertEqual(response.json(), train_mock)

    def test_user_detail_get(self, m):
        user_id = 1
        name = "Борис"
        user_mock = {
            "user_id": user_id,
            "name": name
        }

        m.get(
            HOST_URL_ORDER + 'users/%s/' % user_id,
            status_code=200,
            headers={"Content-Type": "application/json"},
            json = user_mock
        )

        response = self.client.get(reverse('servise:user-detail', kwargs={"user_id":user_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 1)
        self.assertEqual(response.json(), user_mock)

    def test_user_detail_patch(self, m):
        user_id = 1
        name = "Иван"
        user_mock = {
            "user_id": user_id,
            "name": name
        }

        m.patch(
            HOST_URL_ORDER + 'users/%s/' % user_id,
            status_code=200,
            headers={"Content-Type": "application/json"},
            json = user_mock
        )

        request_data = {
            "name" : name
        }

        response = self.client.patch(reverse('servise:user-detail', kwargs={"user_id":user_id}), data=request_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 1)
        self.assertEqual(response.json(), user_mock)

    def test_users_list_get(self, m):
        user_id = 1
        name = "Борис"
        user_mock = [{
            "user_id": user_id,
            "name": name
        }]

        m.get(
            HOST_URL_ORDER + 'users/',
            status_code=200,
            headers={"Content-Type": "application/json"},
            json=user_mock
        )

        response = self.client.get(reverse('servise:users-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 1)
        self.assertEqual(response.json(), user_mock)

    def test_order_detail_get(self, m):
        order_id = 1
        train_id = 1
        ticket_count = 2
        state = 0
        order_mock = {
            "oredr_id": order_id,
            "state": state,
            "train_id": train_id,
            "ticket_count": ticket_count
        }

        m.get(
            HOST_URL_ORDER + 'orders/%s/' % order_id,
            status_code=200,
            headers={"Content-Type": "application/json"},
            json=order_mock
        )

        train_id = 1
        free_places = 10
        train_mock = {
            "train_id": train_id,
            "ticket_count": 2,
            "from": "Пенза",
            "to": "Москва",
            "free_places": free_places
        }

        m.get(
            HOST_URL_TRAIN + 'trains/%s/' % train_id,
            headers={"Content-Type": "application/json"},
            json=train_mock,
            status_code=200
        )

        resp_data = order_mock.copy()
        resp_data.pop("train_id")
        resp_data["train"] = train_mock

        response = self.client.get(reverse('servise:order-detail', kwargs={"order_id" : order_id}))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 2)
        self.assertEqual(response.json(), resp_data)

    def test_orders_list_get(self, m):
        order_id = 1
        train_id = 1
        ticket_count = 2
        state = 0
        order_mock = [{
            "oredr_id": order_id,
            "state": state,
            "train_id": train_id,
            "ticket_count": ticket_count
        }]

        m.get(
            HOST_URL_ORDER + 'orders/',
            status_code=200,
            headers={"Content-Type": "application/json"},
            json=order_mock
        )

        response = self.client.get(reverse('servise:orders-list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 1)
        self.assertEqual(response.json(), order_mock)

    def test_order_detail_post(self, m):
        order_id = 1
        train_id = 1
        user_id = 1
        ticket_count = 2
        state = 0
        order_mock = {
            "oredr_id": order_id,
            "state": state,
            "train_id": train_id,
            "ticket_count": ticket_count
        }

        m.get(
            HOST_URL_TRAIN,
            status_code=200,
            headers={"Content-Type": "application/json"}
        )

        m.get(
            HOST_URL_ORDER,
            status_code=200,
            headers={"Content-Type": "application/json"}
        )

        train_id = 1
        free_places = 10
        train_get_mock = {
            "train_id": train_id,
            "ticket_count": 4,
            "from": "Пенза",
            "to": "Москва",
            "free_places": free_places
        }

        m.get(
            HOST_URL_TRAIN + 'trains/%s/' % train_id,
            headers={"Content-Type": "application/json"},
            status_code=200,
            json = train_get_mock
        )

        train_patch_mock = {
            "train_id": train_id,
            "ticket_count": 2,
            "from": "Пенза",
            "to": "Москва",
            "free_places": free_places
        }

        m.patch(
            HOST_URL_TRAIN + 'trains/%s/' % train_id,
            headers={"Content-Type": "application/json"},
            status_code=200,
            json = train_patch_mock
        )

        request_data = {
            "train_id": train_id,
            "ticket_count": ticket_count,
            "user_id": user_id
        }


        resp_data = {
            "train" : {
                "status_code" : 200,
                "content" : train_patch_mock
            },
            "order": {
                "status_code" : 201,
                "content" : order_mock
            }
        }

        response = self.client.post(
            reverse('servise:orders-list'),
            data=request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 3)
        self.assertEqual(response.json(), resp_data)

    def test_billing_create_post(self, m):
        order_id = 1
        train_id = 1
        user_id = 1
        ticket_count = 2
        state = 1
        order_mock = {
            "oredr_id": order_id,
            "state": state,
            "train_id": train_id,
            "ticket_count": ticket_count
        }

        m.patch(
            HOST_URL_ORDER + 'orders/%s/' %order_id,
            status_code=200,
            headers={"Content-Type": "application/json"},
            json=order_mock
        )

        billing_id = 1
        name = "Борис"
        card = 1234567890
        billing_mock = {
            "billing_id": billing_id,
            "order_id": order_id,
            "name": name,
            "card": card
        }

        m.post(
            HOST_URL_BILLING + 'billings/',
            headers={"Content-Type": "application/json"},
            status_code=201,
            json = billing_mock
        )

        resp_data = {
            "billing": {
                "status_code": 201,
                "content": billing_mock
            },
            "order": {
                "status_code": 200,
                "content": order_mock
            }
        }


        request_data = billing_mock.copy()

        response = self.client.post(
            reverse('servise:billing-create'),
            data=request_data,
            content_type='application/json'
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(m.called, True)
        self.assertEqual(m.call_count, 2)
        self.assertEqual(response.json(), resp_data)









