from django.urls import path
from user import views

urlpatterns = [
    path('register/', views.RegisterGenericView.as_view(), name='register'),
    path('login/', views.LoginGenericView.as_view(), name='login')
]
