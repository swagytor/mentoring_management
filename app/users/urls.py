from rest_framework import routers

from users import views

router = routers.SimpleRouter()
router.register(r"users", views.UserViewSet, basename="users")

urlpatterns = [] + router.urls
