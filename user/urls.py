from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UserGenericView, basename='user')
router.register('forgot-password', views.ForgotGenericView, basename='forgot-password')

urlpatterns = [
    path('register/', views.RegisterGenericView.as_view(), name='register'),
    path('login/', views.LoginGenericView.as_view(), name='login'),
    path('refresh/', views.RefreshGenericView.as_view(), name='refresh'),
    path('logout/', views.LogoutGenericView.as_view(), name='logout'),
    path('reset-password/', views.ResetPasswordGenericView.as_view(), name='reset-password'),

    path('', include(router.urls))
]
