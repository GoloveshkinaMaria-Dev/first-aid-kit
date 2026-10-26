from django.contrib import admin
from django.urls import include, path

from medicines.views import medicine_list_html, schedule_list_html

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("medicines.urls")),
    path("my-kit/", medicine_list_html, name="medicine-list-html"),
    path('my-schedule/', schedule_list_html, name='schedule-list-html'),
]
