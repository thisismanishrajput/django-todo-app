from rest_framework import serializers
from account.models import User

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type':'password'},write_only = True)
    class Meta:
        model = User
        fields = ['email', 'firstName', 'lastName','password', 'password2']
        extra_kwargs = {'write_only':True}


    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)




class UserLoginSerializer(serializers.ModelSerializer):
  email = serializers.EmailField(max_length=255)
  class Meta:
    model = User
    fields = ['id','email', 'password']



class UserProfileSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'email', 'firstName','lastName']
    depth = 1