from django.urls import path
from . import views
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
     path("", views.index, name="index"),
     path("api/products/", views.ProductsView.as_view(), name="products"),
     path("api/register", views.RegisterView.as_view(), name="register"),
     path("api/login", obtain_auth_token, name="login")
 ]