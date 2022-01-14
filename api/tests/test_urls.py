from django.test import SimpleTestCase
from django.urls import reverse, resolve
from api.views import index, ProductsView, RegisterView

"""
    Perform Tests on url conf to see if they resolve to the expected view method 
"""
class TestUrls(SimpleTestCase):

    def test_index_resolve(self):
        url = reverse('index')
        self.assertEqual(resolve(url).func, index)

    def test_products_resolve(self):
        url = reverse('products')
        self.assertEqual(resolve(url).func.view_class, ProductsView)

    def test_register_resolve(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func.view_class, RegisterView)