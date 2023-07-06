from django.urls import path
from . import views
from django.urls import path

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', views.login_view, name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),

    path('password_change/done/', views.password_change_done,
         name='password_change_done'),

    path('profile/', views.userAccount, name="profile"),
    path('edit-profile/', views.editAccount, name="edit-profile"),
]
