from rest_framework import serializers

from api.models import UserProfile,AppsModel

from rest_framework.authtoken.views import ObtainAuthToken
from django.conf import settings
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User




class UserProfileSerializer(serializers.ModelSerializer):
	class Meta:
     
		model = UserProfile
		fields = ['email',  'password', 'date_of_birth','profile_image','username','id']
		extra_kwargs={'password':{'write_only':True}}
		
			
	def save(self):
		user = UserProfile(
			email = self.validated_data['email'],
			date_of_birth= self.validated_data['date_of_birth'],
			username = self.validated_data['username'],
           			 )
		password= self.validated_data['password']		
		user.set_password(password)
		user.save()
		return user
   
        
        
        

class AppSerializer(serializers.ModelSerializer):
 	
 owner = UserProfileSerializer(many=False,read_only=False)
 class Meta:
		model = AppsModel
		fields = ['name','owner']
  
  
        


