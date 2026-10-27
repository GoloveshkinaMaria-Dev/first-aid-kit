from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import register_view

from .views import IntakeLogViewSet, MedicineView, ScheduleView

router = DefaultRouter()
router.register("medicines", MedicineView, basename="medicine")
router.register("schedules", ScheduleView, basename="schedule")
router.register("intakes", IntakeLogViewSet, basename="intake")

urlpatterns = [
    path("", include(router.urls)),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="registration/login.html"),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path("register/", register_view, name="register"),
]
