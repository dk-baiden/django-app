from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.models import User
from api.serializers import UserProfileSerializer,AppSerializer
from django.http import Http404
from django.shortcuts import get_object_or_404
from api.models import UserProfile,AppsModel
from django.core.paginator import Paginator
from rest_framework.authentication import  TokenAuthentication,SessionAuthentication
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.filters import SearchFilter,OrderingFilter
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authtoken.views import ObtainAuthToken
from api import permissions
from rest_framework.permissions import BasePermission,SAFE_METHODS


class isOwnerOrReadOnly(BasePermission):
    message = "editing is restricted to authors only."
    def has_object_permission(self, request, view,obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.owner == request.user
    
    

class IsUserOrAdmin(BasePermission):
    message = "editing is restricted to users only."
    def has_object_permission(self, request, view,obj):
        if request.method in SAFE_METHODS:
            return True
        return obj== request.user
    
        
            

class UserList(generics.ListAPIView):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    def post(self,request,format=None):
        data ={}
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            saved_user=serializer.save()
            data['email'] = saved_user.email
            data['username'] = saved_user.username
            data['date_of_birth'] = saved_user.date_of_birth
            token = Token.objects.get(user=saved_user).key
            data['token'] = token
            data['profile_image']=str(saved_user.profile_image)
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            data = serializer.errors
        return Response(data)    





class UserDetail(generics.RetrieveUpdateDestroyAPIView,IsAuthenticatedOrReadOnly,IsUserOrAdmin):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()
    lookup_field="username"
    permission_classes = [IsAuthenticatedOrReadOnly,IsUserOrAdmin]
    authentication_classes= [TokenAuthentication,SessionAuthentication]
    
    def update(self, request,*args,**kwargs):
        instance = self.get_object()
        user_id= instance.id
        user_password =instance.password
        instance.email = request.data.get("email")
        instance.username = request.data.get("username")
        instance.id = user_id
        instance.password=user_password
        instance.save()
        serializer = self.get_serializer(data=instance)
       
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"response":"update successfull"})
        else:
            return Response(serializer.errors)
    
    
    
            

class AppList(generics.ListCreateAPIView):
    serializer_class = AppSerializer
    queryset = AppsModel.objects.all()
    permission_classes=[IsAuthenticatedOrReadOnly]
    
      

class AppDetail(generics.RetrieveUpdateDestroyAPIView,isOwnerOrReadOnly,IsAuthenticated):
    serializer_class = AppSerializer
    lookup_field="name" 
    queryset = AppsModel.objects.all()
    permission_classes=[isOwnerOrReadOnly,IsAuthenticated]
    
    
    
    def update(self, request,*args,**kwargs):
        instance = self.get_object()
        app_id =instance.id
        
        instance.name = request.data.get("name")
        instance.id = app_id
        instance.save()
        serializer = self.get_serializer(data=instance)
       
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response({"response":"update successful"})
        else:
            return Response(serializer.errors)
    
        
    