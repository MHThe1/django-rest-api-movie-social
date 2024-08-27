from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}
        
    def save(self):
        password = self.validated_data.get('password')
        password2 = self.validated_data.get('password2')
        
        if password != password2:
            raise serializers.ValidationError({'error':'Passwords do not match'})
        
        if User.objects.filter(email=self.validated_data.get('email')).exists():
            raise serializers.ValidationError({'error':'Email already exists'})
        
        account = User(username=self.validated_data.get('username'), email=self.validated_data.get('email'))
        account.set_password(password)
        account.save()
        return account