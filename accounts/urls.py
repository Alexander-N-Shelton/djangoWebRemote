# accounts/urls.py

from django.urls import path, include 
from .views import login, logout, register, update_profile
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('settings/update/', update_profile, name='update_profile'),
    
    # Password Change (logged in users)
    path('password_change', auth_views.PasswordChangeView.as_view(
        template_name='accounts/password_change.html',
    ), name='password_change'),
    
    # Password Change Done (logged in users)
    path('password_change/done', auth_views.PasswordChangeDoneView.as_view(
        template_name='accounts/password_change_done.html',
    ), name='password_change_done'),

    # Password Reset 
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="accounts/password_reset_form.html",
    ), name='password_reset'),
    
    # Password Reset Done
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name="accounts/password_reset_done.html",
    ), name='password_reset_done'),
    
    # Password Reset Confirm
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="accounts/password_reset_confirm.html",
    ), name='password_reset_confirm'),
    
    # Password Reset Complete
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name="accounts/password_reset_complete.html",
    ), name='password_reset_complete')
]
