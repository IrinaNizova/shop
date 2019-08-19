import json
from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from .views import PersonLoad
from .models import Person
from .serializers import PersonSerializer

client = Client()
valid_set = [
    {
        "name": "Ivanov I I",
        "citizen_id": 1,
        "town": "Moscow",
        "street": "Iskri",
        "building": "15",
        "appartement": 3,
        "birth_date": "1990-11-11T00:00:00Z",
        "gender": "male",
        "relatives": [
            2,
            3
        ]
    },
    {
        "name": "Petrov I I",
        "citizen_id": 2,
        "town": "Moscow",
        "street": "Iskri",
        "building": "22",
        "appartement": 33,
        "birth_date": "1970-11-11T00:00:00Z",
        "gender": "male",
        "relatives": [
            1,
            3
        ]
    },
    {
        "name": "Smirnov I I",
        "citizen_id": 3,
        "town": "Moscow",
        "street": "Iskri",
        "building": "17",
        "appartement": 7,
        "birth_date": "1975-11-11T00:00:00Z",
        "gender": "male",
        "relatives": [
            1,
            2
        ]
    },
    {
        "name": "Kats I I",
        "citizen_id": 4,
        "town": "Moscow",
        "street": "Iskri",
        "building": "115",
        "appartement": 3,
        "birth_date": "1987-11-11T00:00:00Z",
        "gender": "male",
        "relatives": [
            2,
            3
        ]
    }
]

class CreateNewPersonsSetTest(TestCase):

    def setUp(self):
        self.valid_set = valid_set
        self.invalid_set = {
            'name': '',
            'age': 4,
            'breed': 'Pamerion',
            'color': 'White'
        }

    def test_create_valid_set(self):
        response = client.post(
            '/imports/',
            data=json.dumps(self.valid_set),
            content_type='application/json'
        )
        answer_text = {'data': {'import_id': 1}}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), answer_text)
        response = client.post(
            '/imports/',
            data=json.dumps(self.valid_set),
            content_type='application/json'
        )
        answer_text = {'data': {'import_id': 2}}
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), answer_text)

    def test_create_invalid_set(self):
        response = client.post(
            '/imports/',
            data=json.dumps(self.invalid_set),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreateGetPersonsSetTest(TestCase):

    def setUp(self):
        self.valid_set = valid_set
        response = client.post(
            '/imports/',
            data=json.dumps(self.valid_set),
            content_type='application/json'
        )

    def test_get_valid_set(self):
        response = client.get(
            '/imports/1/citizens'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_set(self):
        response = client.get(
            '/imports/11/citizens'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class CreatePatchPersonsTest(TestCase):

    def setUp(self):
        self.valid_set = valid_set
        response = client.post(
            '/imports/',
            data=json.dumps(self.valid_set),
            content_type='application/json'
        )

    def test_patch_valid_set(self):
        response = client.patch(
            '/imports/1/citizens/1',
            data=json.dumps({"appartement":33}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data = self.valid_set[0]
        data["appartement"] = 33
        self.assertEqual(response.json(), {'data': data})

    def test_patch_invalid_id_set(self):
        response = client.patch(
            '/imports/1/citizens/6',
            data=json.dumps({"appartement":33}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_patch_invalid_data_set(self):
        response = client.patch(
            '/imports/1/citizens/6',
            data=json.dumps({"appartement":None}),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)