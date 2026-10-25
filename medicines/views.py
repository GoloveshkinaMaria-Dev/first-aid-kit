from django.contrib.admin import action
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, mixins
from .models import Medicine, Schedule
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .serializers import MedicineSerializer, SchedulerSerializer



class MedicineView(
    viewsets.ModelViewSet):
    """POST/ GET / PUT / PATCH / DELETE"""
    serializer_class = MedicineSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Medicine.objects.filter(
            user=self.request.user)

class ScheduleView(
    viewsets.ModelViewSet
):
    serializer_class = SchedulerSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
            return Schedule.objects.filter(
                medicine__user=self.request.user
                )