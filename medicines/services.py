from datetime import timedelta, datetime
from .models import Schedule, Medicine, IntakeLog

def generate_schedule(schedule: Schedule, days_ahead: int = 30) -> None:
    if schedule.frequency == "daily":
        current_date = schedule.start_date
        end_date = (
            schedule.end_date
            or (current_date + timedelta(days=days_ahead))
        )

        logs = []
        while current_date <= end_date:
            if (not schedule.days_of_week
                or current_date.isoweekday() in schedule.days_of_week
            ):
                for slot in schedule.slots.all():
                    scheduled_dt = datetime.combine(current_date, slot.time) 
                for medicine in schedule.medicine.all():
                    logs.append(
                        IntakeLog(
                            schedule=schedule,
                            medicine=medicine,
                            scheduled_at=scheduled_dt,
                        )
                    )
                    current_date += timedelta(days=1)
        
    
        if logs:
            IntakeLog.objects.bulk_create(logs)

