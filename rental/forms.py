from django import forms
from .models import Rental


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = ["rating", "review"]
        widgets = {
            "rating": forms.Select(choices=[(i, f"{i} stars") for i in range(1, 6)]),
            "review": forms.Textarea(
                attrs={"rows": 3, "placeholder": "Write your review here..."}
            ),
        }
