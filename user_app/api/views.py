from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
 

from user_app.api.serializers import RegisterSerializer
from user_app import models


@api_view(['POST'])
def logout_view(request):
    
    if request.method == 'POST':
        request.user.auth_token.delete()
        
        data = {}
        data['response'] = 'Logged out successfully'
        data['status'] = status.HTTP_200_OK
        return Response(data)


@api_view(['POST'])
def registration_view(request):
    
    if request.method == 'POST':
        serializer = RegisterSerializer(data=request.data)

        data = {}
        
        if serializer.is_valid():
            account = serializer.save()
            
            data['response'] = 'Account created successfully'
            data['username'] = account.username
            data['email'] = account.email
            data['token'] = account.auth_token.key
            data['status'] = status.HTTP_201_CREATED
            
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #                     'refresh': str(refresh),
            #                     'access': str(refresh.access_token),
            #                 }
        
        else:
            data['error'] = serializer.errors
            
        return Response(data)