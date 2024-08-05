from django.urls import path
from django.contrib import admin
from users import views

app_name='users'

urlpatterns=[
    path('signup/', views.SignUpView.as_view(), name='sign_up_view'), # /users/signup/
    path('login/', views.LoginView.as_view(), name='login_view'), # /users/login/
    path('logout/', views.LogoutView.as_view(), name='logout_view'), # /users/logout/
    path('quit/', views.QuitView.as_view(), name='quit_view'), # /users/quit/
    path('profile/', views.ProfileView.as_view(), name='profile_view'), # /users/profile/
    path('ourcare/', views.FriendsView.as_view(), name='ourcare_view'), # /users/ourcare/
    path('ourcare/profile/<str:username>/', views.FriendsProfileView.as_view(), name='friend_profile'),


    path('admin', admin.site.urls),
]