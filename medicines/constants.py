MAX_LENGTH_NAME = 30
MAX_LENGTH_SLUG = 30

from django.db import models


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
