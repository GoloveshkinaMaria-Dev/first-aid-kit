from django.contrib import admin
from django.urls import include, path

from medicines.views import medicine_list_html, schedule_list_html, medicine_create_html, medicine_edit_html 

urlpatterns = [
    path("admin/", admin.site.urls),

    path("api/", include("medicines.urls")),
    path("my-kit/", medicine_list_html, name="medicine-list-html"),
    path('my-kit/add/', medicine_create_html, name='medicine-add-html'),
    path('my-kit/<int:medicine_id>/edit/', medicine_edit_html, name='medicine-edit-html'),
    path('my-schedule/', schedule_list_html, name='schedule-list-html'),
]
