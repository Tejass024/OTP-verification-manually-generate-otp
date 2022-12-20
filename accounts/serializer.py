from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import User


user = get_user_model

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('phone', 'password')
        extra_kwargs = {'password':{'write_only':True},}
        
        
        def create(self, validated_data):
            user = User.objects.create(**validated_data)
            return user
        
