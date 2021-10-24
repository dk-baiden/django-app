from django.urls import path
from api.views import(
 UserList, 
 UserDetail,
AppList,
AppDetail
)
from rest_framework.authtoken.views import obtain_auth_token

app_name = 'api'

urlpatterns = [

 	
 	path('login/',  obtain_auth_token, name="login"),
    path('users/',UserList.as_view(),name="userlist"),
    path('users/<str:username>/',UserDetail.as_view(),name="userlist"),
    path('apps/',AppList.as_view(),name="apps"),
    path('apps/<str:name>/',AppDetail.as_view(),name="apps")
   
]