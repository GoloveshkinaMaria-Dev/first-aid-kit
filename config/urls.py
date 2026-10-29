from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from medicines.views import (
    medicine_create_html,
    medicine_edit_html,
    medicine_list_html,
    schedule_create_html,
    schedule_list_html,
    today_list_html,
)
from users.views import UserViewSet, profile_view, register_view

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path("api/", include("medicines.urls")),
    path("api/auth/", include("djoser.urls")),
    path("api/auth/", include("djoser.urls.authtoken")),
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
    path("profile/", profile_view, name="profile"),
    path("my-kit/", medicine_list_html, name="medicine-list-html"),
    path("my-kit/add/", medicine_create_html, name="medicine-add-html"),
    path("my-kit/<int:medicine_id>/edit/", medicine_edit_html, name="medicine-edit-html"),
    path("my-schedule/", schedule_list_html, name="schedule-list-html"),
    path("my-schedule/add/", schedule_create_html, name="schedule-add-html"),
    path("my-kit/today", today_list_html, name="today-list-html"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
