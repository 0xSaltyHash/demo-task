from rest_framework import generics
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from .serializers import ProductsSerializer, UserCreationSerializer
from .models import Products, User
from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes((permissions.AllowAny,))
def index(request):
     return Response({"response": "Hello, world!"})

class ProductsView(generics.ListCreateAPIView):
     permission_classes = (permissions.IsAuthenticated,)
     serializer_class = ProductsSerializer

     def get_queryset(self):
          queryset = Products.objects.all()
          username = self.request.query_params.get('username')
          if username is not None:
               user = get_object_or_404(User, username=username)
               queryset = queryset.filter(seller=user.id)
          return queryset

     def perform_create(self, serializer):
         serializer.save(seller=self.request.user)

class RegisterView(generics.CreateAPIView):
     queryset = User.objects.all()
     permission_classes = (permissions.AllowAny,)
     serializer_class = UserCreationSerializer