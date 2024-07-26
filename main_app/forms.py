from django import forms
from .models import Feeding


class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ["date", "meal"]
        # update feeding form date input field
        widgets = {
            "date": forms.DateInput(
                format=("%Y-%m-%d"),
                attrs={"placeholder": "Select a date", "type": "date"},
            ),
        }


# Note that our custom form inherits from ModelForm.
# Many of the attributes in the Meta class are in common with CBVs because the CBV was using them behind the scenes to create a ModelForm as previously mentioned.
