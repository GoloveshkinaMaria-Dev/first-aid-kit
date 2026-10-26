from django.db import models

MAX_LENGTH_NAME = 30
MAX_LENGTH_SLUG = 30


class Frequency(models.TextChoices):
    ONCE_DAILY = "once_daily", "Раз в день"
    TWICE_DAILY = "twice_daily", "Два раза в день"
    THREE_TIMES_DAILY = "three_daily", "Три раза в день"
    WEEKLY = "weekly", "Раз в неделю"
    AS_NEEDED = "as_needed", "По необходимости"


class Status(models.TextChoices):
    SCHEDULED = "scheduled", "Запланировано"
    TAKEN = "taken", "Принято"
    MISSED = "missed", "Пропущено"
    SKIPPED = "skipped", "Отменено"


WRONG_USER_SCHEDULE = "Нельзя создать график для чужого лекарства."
INVALID_DATE = "Дата окончания не может быть раньше даты начала."
ADD_TIME = "Добавьте хотя бы одно время приема."
