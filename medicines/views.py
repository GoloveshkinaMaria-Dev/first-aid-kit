from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .forms import MedicineForm
from .models import IntakeLog, Medicine, Schedule
from .serializers import IntakeLogSerializer, MedicineSerializer, SchedulerSerializer
from .services import generate_schedule


class MedicineView(viewsets.ModelViewSet):
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Medicine.objects.filter(user=self.request.user)


class ScheduleView(viewsets.ModelViewSet):
    serializer_class = SchedulerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(medicines__user=self.request.user)

    def perform_create(self, serializer):
        schedule = serializer.save()
        generate_schedule(schedule)


@login_required
def medicine_list_html(request):
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


def medicine_create_html(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.user = request.user
            # Slug генерю из названия
            medicine.slug = medicine.name.lower().replace(" ", "-")
            medicine.save()

            return redirect("medicine-list-html")
    else:
        form = MedicineForm()

    return render(request, "medicines/medicine_form.html", {"form": form})


@login_required
def schedule_create_html(request):
    medicines = Medicine.objects.filter(user=request.user)
    return render(request, "medicines/schedule_form.html", {"medicines": medicines})


def medicine_edit_html(request, medicine_id: int):
    medicine = get_object_or_404(Medicine, id=medicine_id, user=request.user)

    if request.method == "POST":
        form = MedicineForm(request.POST, instance=medicine)
        if form.is_valid():
            form.save()
            return redirect("medicine-list-html")
    else:
        form = MedicineForm(instance=medicine)

    return render(request, "medicines/medicine_form.html", {"form": form, "medicine": medicine})


class IntakeLogViewSet(viewsets.ModelViewSet):
    serializer_class = IntakeLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return IntakeLog.objects.filter(schedule__medicines__user=self.request.user).order_by(
            "-scheduled_at"
        )

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def mark_as_taken(self, request, pk=None):
        log = self.get_object()
        log.status = "taken"
        log.taken_at = timezone.now()
        log.save()
        serializer = self.get_serializer(log)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@login_required
def today_list_html(request):
    return render(request, "medicines/today.html")
