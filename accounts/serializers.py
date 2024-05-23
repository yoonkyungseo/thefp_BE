from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Deposit_Comment, User

class CustomRegisterSerializer(RegisterSerializer):
    birth = serializers.DateField(
        required=True
    )
    nickname = serializers.CharField(
        required = False,
        allow_blank = False,
        max_length = 20
    )
    def get_cleaned_data(self):
        return {
            'username':self.validated_data.get('username',''),
            'password1':self.validated_data.get('password1',''),
            'birth':self.validated_data.get('birth',''),
            'email':self.validated_data.get('email',''),
            'nickname':self.validated_data.get('nickname','')
        }

class DepositCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit_Comment
        fields = '__all__'
        read_only_fields = ['user','product','created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['product','annuity','creditloan']