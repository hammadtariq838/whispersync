from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('profile/', views.userAccount, name="profile"),
    path('edit-profile/', views.editAccount, name="edit-profile"),


    path("password_change/", auth_views.PasswordChangeView.as_view(
        template_name='users/password_change.html'), name="password_change"),
    path('password_change/done/', views.password_change_done,
         name='password_change_done'),
]
