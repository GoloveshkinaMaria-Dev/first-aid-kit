from django.db import models
from users.models import User

from .constants import MAX_LENGTH_NAME, MAX_LENGTH_SLUG, Frequency, Status


class Medicine(models.Model):
    name = models.CharField(
        max_length=MAX_LENGTH_NAME,
        unique=False,
        verbose_name="Название тега",
    )
    slug = models.SlugField(
        max_length=MAX_LENGTH_SLUG,
        unique=False,
        verbose_name="Слаг",
    )
    dosage = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        verbose_name="Дозировка (mg)",
    )
    purchase_date = models.DateField(
        unique=False,
        verbose_name="Дата покупки",
    )
    shelf_life_days = models.PositiveIntegerField(
        verbose_name="Срок годности (дней)",
    )
    reorder_days = models.IntegerField(
        verbose_name="За сколько напоминать о повторной покупке",
    )
    quantity = models.IntegerField(
        verbose_name="Количество в упаковке",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="medicicnes",
        verbose_name="Пользователь",
    )

    class Meta:
        verbose_name = "Лекарство"
        verbose_name_plural = "Лекарства"

    def __str__(self):
        return self.name

    @property
    def expiry_date(self):
        """Дата истечения срока годности."""
        from datetime import timedelta

        return self.purchase_date + timedelta(days=self.shelf_life_days)


class Schedule(models.Model):
    medicine = models.ForeignKey(
        Medicine,
        related_name="schedules",
        verbose_name="Лекарство",
    )
    time_of_day = models.DateTimeField(verbose_name="Время приема")
    frequency = models.CharField(
        choices=Frequency.choices, verbose_name="Периодичность"
    )
    start_date = models.DateField(verbose_name="Дата начала приема")
    end_date = models.DateField(
        null=True, blank=True, verbose_name="Дата оконяания приема"
    )

    class Meta:
        verbose_name = "График приёма"
        verbose_name_plural = "Графики приёма"

    def __str__(self):
        return f"{self.medicine.name} — {self.get_frequency_display()} в {self.time_of_day}"


class IntakeLog(models.Model):
    schedule = models.ForeignKey(
        Schedule,
        on_delete=models.CASCADE,
        verbose_name="График",
        related_name="logs",
    )
    scheduled_at = models.DateTimeField(verbose_name="Запланированное время")
    taken_at = models.DateTimeField(
        null=True, blank=True, verbose_name="Фактическое время приема"
    )
    status = models.CharField(choices=Status.choices, verbose_name="Статус")

    class Meta:
        verbose_name = "Запись о приёме"
        verbose_name_plural = "Записи о приёме"
        ordering = ["-scheduled_at"]

    def __str__(self):
        return f"{self.schedule.medicine.name} @ {self.scheduled_at:%d.%m.%Y %H:%M} — {self.get_status_display()}"
