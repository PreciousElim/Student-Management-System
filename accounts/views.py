from django.shortcuts import render
from .models import User
from .serializers import AccountSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


class CreateAccount (generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]
    
    
    def create (self,request, *args, **kwargs):
        serializers = self.get_serializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        
        return Response ({
            'message': 'Account created successfully'},
            status = status.HTTP_201_CREATED
        )
    
class LogoutView(APIView):
    permissions_classes = permissions.IsAuthenticated 
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'message': 'Logged out Successfully'},
                status = status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({
                'error': 'Invalid Token'},
                status=status.HTTP_401_UNAUTHORIZED)
            
# Create your views here.