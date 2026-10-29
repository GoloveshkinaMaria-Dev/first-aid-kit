from rest_framework import serializers

from .constants import ADD_TIME, INVALID_DATE, WRONG_USER_SCHEDULE
from .models import IntakeLog, Medicine, Schedule, ScheduleSlot


class MedicineSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Medicine
        fields = (
            "id",
            "name",
            "dosage",
            "purchase_date",
            "shelf_life_days",
            "reorder_days",
            "quantity",
            "user",
        )
        read_only_fields = ("id",)


class ScheduleSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScheduleSlot
        fields = ("id", "time")


class SchedulerSerializer(serializers.ModelSerializer):
    slots = ScheduleSlotSerializer(many=True, write_only=True)
    medicines = serializers.PrimaryKeyRelatedField(queryset=Medicine.objects.all(), many=True)
    days_of_week = serializers.ListField(
        child=serializers.IntegerField(min_value=1, max_value=7), required=False, default=[]
    )

    class Meta:
        model = Schedule
        fields = (
            "days_of_week",
            "start_date",
            "end_date",
            "medicines",
            "slots",
        )
        read_only_fields = ("id",)

    def validate_medicine(self, medicine):
        request = self.context.get("request")
        if request and medicine.user != request.user:
            raise serializers.ValidationError(WRONG_USER_SCHEDULE)
        return medicine

    def validate(self, attrs):
        start = attrs.get("start_date")
        end = attrs.get("end_date")
        if start and end and end < start:
            raise serializers.ValidationError({"end_date": INVALID_DATE})

        if not attrs.get("slots"):
            raise serializers.ValidationError({"slots": ADD_TIME})

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
    medicine_name = serializers.CharField(source="medicine.name", read_only=True)

    class Meta:
        model = IntakeLog
        fields = (
            "id",
            "schedule",
            "medicine",
            "medicine_name",
            "scheduled_at",
            "taken_at",
            "status",
        )
        read_only_fields = ("id",)
