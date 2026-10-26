from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import MedicineView, ScheduleView

router = DefaultRouter()
router.register("medicines", MedicineView, basename="medicine")
router.register("schedules", ScheduleView, basename="schedule")

urlpatterns = [
    path("", include(router.urls)),
]
