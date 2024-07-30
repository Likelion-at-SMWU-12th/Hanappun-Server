from django.urls import path, include
from django.contrib import admin
from users import views
# from rest_framework import routers

app_name='users'

# router = routers.DefaultRouter()
# router.register('', )

urlpatterns=[
    path('signup/', views.SignUpView.as_view(), name='sign_up_view'), # /users/signup/
    path('login/', views.LoginView.as_view(), name='login_view'), # /users/login/
    path('logout/', views.LogoutView.as_view(), name='logout_view'), # /users/logout/
    path('admin', admin.site.urls),
]