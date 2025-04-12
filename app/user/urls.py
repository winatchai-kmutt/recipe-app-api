"""
URL mappings for the user API.
"""

from django.urls import path

from user import views

# so CREATE_USER_URL = reverse('user:create') come from this!!!
urlpatterns = [
    path('create', views.CreateUserView.as_view(), name='create')
]
