from django import forms

from .models import Medicine


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ["name", "dosage", "purchase_date", "shelf_life_days", "reorder_days", "quantity"]

        widgets = {
            "name": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Например: Аспирин"}
            ),
            "dosage": forms.NumberInput(attrs={"class": "form-control"}),
            "purchase_date": forms.DateInput(attrs={"class": "form-control", "type": "date"}),
            "shelf_life_days": forms.NumberInput(attrs={"class": "form-control"}),
            "reorder_days": forms.NumberInput(attrs={"class": "form-control"}),
            "quantity": forms.NumberInput(attrs={"class": "form-control"}),
        }
