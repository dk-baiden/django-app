from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

def get_Image_File_Path(self,filename):
    return f'profile_images/{self.username}/{"profile_image.png"}'

def assignOwner(self):
    return self.pk



class MyUserManager(BaseUserManager):
    def create_user(self, email, date_of_birth,username, password=None):
        
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            date_of_birth=date_of_birth,
            username = username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,username, date_of_birth, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username = username,
            password=password,
            date_of_birth=date_of_birth,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    date_of_birth = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    is_admin = models.BooleanField(default=False)
    profile_image = models.FileField(upload_to=get_Image_File_Path,max_length=200,verbose_name='profile image',null=True,default='/default/some image.png')
    username = models.CharField(unique=True,max_length=200)
    objects = MyUserManager()



    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['date_of_birth','username']


    



    def __str__(self):
        return self.email


    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        
        return self.is_admin

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
        if created:
         Token.objects.create(user=instance)  
         

class AppsModel(models.Model):
    owner =  models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.PROTECT)
    name = models.CharField(max_length=200,verbose_name="app_name",unique=True) 
    
    
   
    
    
    def __str__(self):
        return self.name
    
    def verbose_name(self):
        return "Apps"          