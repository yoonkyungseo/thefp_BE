from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import Deposit_Comment

class CustomRegisterSerializer(RegisterSerializer):
    birth = serializers.CharField(
        required=True,
        max_length=100,
        allow_blank=True
    )
    def get_cleaned_data(self):
        return {
            'username':self.validated_data.get('username',''),
            'password1':self.validated_data.get('password1',''),
            'birth':self.validated_data.get('birth',''),
            # 'email':self.validated_data.get('email',''),
        }

class DepositCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit_Comment
        fields = '__all__'
        read_only_fields = ['user','product',]