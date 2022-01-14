from rest_framework import serializers
from .models import Products, User
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class ProductsSerializer(serializers.ModelSerializer):    
    
    seller = serializers.SerializerMethodField()

    # get the seller name from the user id
    def get_seller(self, obj):
        return obj.seller.username
       
    class Meta:
        model = Products
        fields = ['seller', 'product_name', 'price']


class UserCreationSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )

    # Use write_only to ensure that the password is not returned in the response
    password = serializers.CharField(
                write_only=True,
                required=True,
                validators=[validate_password]
                )
    
    password2 = serializers.CharField(
                write_only=True,
                required=True
                )

    class Meta:
        model = User
        fields = ['username', 'password', 'password2', 'email']

    def validate(self, attributes):
        
        if attributes['password'] != attributes['password2']:
            raise serializers.ValidationError({"password": "password and password2 mismatch"})
        return attributes

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        # Make sure password is stored as hashed value in DB
        user.set_password(validated_data['password'])
        user.save()

        return user