from django import forms
from .models import Feeding


class FeedingForm(forms.ModelForm):
    class Meta:
        model = Feeding
        fields = ["date", "meal"]

# Note that our custom form inherits from ModelForm.
# Many of the attributes in the Meta class are in common with CBVs because the CBV was using them behind the scenes to create a ModelForm as previously mentioned.
