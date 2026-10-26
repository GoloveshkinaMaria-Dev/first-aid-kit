from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Medicine, Schedule
from .serializers import MedicineSerializer, SchedulerSerializer


class MedicineView(viewsets.ModelViewSet):
    """POST/ GET / PUT / PATCH / DELETE"""

    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Medicine.objects.filter(user=self.request.user)


class ScheduleView(viewsets.ModelViewSet):
    serializer_class = SchedulerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(medicines__user=self.request.user)


@login_required
def medicine_list_html(request):
    """Отображение лекарств текущего пользователя на HTML-странице."""
    medicines = request.user.medicines.all()

    medicines = medicines.order_by("-purchase_date")

    return render(request, "medicines/list.html", {"medicines": medicines})


@login_required
def schedule_list_html(request):
    schedules = (
        Schedule.objects.filter(medicines__user=request.user)
        .distinct()
        .prefetch_related("medicines", "slots")
    )

    return render(request, "medicines/schedule_list.html", {"schedules": schedules})
