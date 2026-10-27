from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IntakeLogViewSet, MedicineView, ScheduleView

router = DefaultRouter()
router.register("medicines", MedicineView, basename="medicine")
router.register("schedules", ScheduleView, basename="schedule")
router.register("intakes", IntakeLogViewSet, basename="intake")

urlpatterns = [
    path("", include(router.urls)),
]
