from django import test
from django.http import response
from rest_framework.test import APITestCase
from django.urls import reverse
from api.models import Products, User

class TestProducts(APITestCase):

    def create_test_products(self):
        self.dummy_user1 = User.objects.create(username='dummy1', email='dumm@mail.com', password="dummy")
        self.dummy_user1.set_password("dummypass1")
        self.test_product1 = Products.objects.create(seller=self.dummy_user1, product_name="test1", price=1)
        self.test_product2 = Products.objects.create(seller=self.dummy_user1, product_name="test2", price=10.5)
        self.dummy_user2 = User.objects.create(username='dummy2', email='dumm2@mail.com', password="dummy")
        self.dummy_user2.set_password("dummypass2")
        self.test_product1 = Products.objects.create(seller=self.dummy_user2, product_name="test3", price=12)
        self.test_product2 = Products.objects.create(seller=self.dummy_user2, product_name="test4", price=7.50)

    def authenticate(self):
        """
            Create and login a test user for authenticated tests
        """
        self.client.post(reverse('register'), {
            "email": "test@test.com",
            "username": "testuser1",
            "password": "TestPas1",
            "password2": "TestPas1"
        })

        response = self.client.post(reverse('login'), {
            "username": "testuser1",
            "password": "TestPas1"
        })

        token = f"Token {response.data['token']}"
        self.client.credentials(HTTP_AUTHORIZATION=token)

    def test_list_products_unauth(self):
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 401)

    def test_list_products_authed_empty(self):
        self.authenticate()
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_list_products_authed(self):
        self.authenticate()
        self.create_test_products()
        response = self.client.get(reverse('products'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 4)

    def test_list_products_filtering(self):
        self.authenticate()
        self.create_test_products()
        url = f"{reverse('products')}?username=dummy1"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['seller'], 'dummy1')
        self.assertEqual(response.data[1]['seller'], 'dummy1')
        
    def test_list_products_filtering_with_non_existing_username(self):
        self.authenticate()
        self.create_test_products()
        url = f"{reverse('products')}?username=nonexistinguser"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(str(response.data['detail']), "Not found.")

    def test_create_products_unauth(self):
        test_product = {"product_name": "test1", "price": 100}
        response = self.client.post(reverse('products'), test_product)
        self.assertEqual(response.status_code, 401)

    def test_create_products_authed(self):
        test_product = {"product_name": "test1", "price": 100}
        self.authenticate()
        response = self.client.post(reverse('products'), test_product)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['seller'], 'testuser1')
        self.assertEqual(response.data['product_name'], test_product['product_name'])
        self.assertEqual(response.data['price'], test_product['price'])