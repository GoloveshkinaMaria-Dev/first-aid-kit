from rest_framework import serializers


from .models import (Medicine, Schedule, IntakeLog, ScheduleSlot)
from users.serializers import UserSerializer


class MedicineSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Medicine
        fields = ("id", "name", "dosage",
                  'purchase_date',
                  'shelf_life_days',
                  'reorder_days',
                  'quantity',
                  'user')
        read_only_fields = ('id',)

class ScheduleSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSlot
        fields = ("id", "time")

class SchedulerSerializer(serializers.ModelSerializer):
    slots = ScheduleSlotSerializer(many=True, write_only=True)
    medicine = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all())
    days_of_week = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=7),
        required=False,
        default=[]
    )
    class Meta:
        model = Schedule
        fields = (
            'time_of_day',
            'days_of_week',
            'start_date',
            'end_date',
            'medicines',
            'slots',
        )
        read_only_fields = ('id',)

    def validate_medicine(self, medicine):
        request = self.context.get("request")
        if request and medicine.user != request.user:
            raise serializers.ValidationError(
                "Нельзя создать график для чужого лекарства."
            )
        return medicine

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        if start and end and end < start:
            raise serializers.ValidationError(
                {"end_date": "Дата окончания не может быть раньше даты начала."}
            )
        
        if not attrs.get("slots"):
            raise serializers.ValidationError(
                {"slots": "Добавьте хотя бы одно время приема."}
                )

        return attrs

    def create(self, validated_data) -> Schedule:
        slots_data = validated_data.pop("slots")
        medicines = validated_data.pop("medicines")
        schedule = Schedule.objects.create(**validated_data)
        
        schedule.medicines.set(medicines)
        
        for slot in slots_data:
            ScheduleSlot.objects.create(schedule=schedule, time=slot["time"])
            
        return schedule

class IntakeLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = IntakeLog
        fields = ("id", "schedule", "scheduled_at", "taken_at", "status", 'user',)
        read_only_fields = ("id",)