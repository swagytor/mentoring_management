from django.urls import path
from rest_framework import routers

from users import views

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = [
    path("logout/", views.UserLogoutAPIView.as_view(), name="logout"),
] + router.urls
