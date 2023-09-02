from django.urls import path, include
from user import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('user', views.UserGenericView, basename='user')
router.register('refresh', views.RefreshGenericView, basename='refresh')
router.register('logout', views.LogoutGenericView, basename='logout')

urlpatterns = [
    path('register/', views.RegisterGenericView.as_view(), name='register'),
    path('login/', views.LoginGenericView.as_view(), name='login'),
    path('', include(router.urls))
]
