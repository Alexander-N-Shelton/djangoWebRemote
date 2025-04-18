# remote/forms.py
from django import forms
from accounts.models import FavoriteButton

class FavoriteButtonForm(forms.Form):
    """Form for selecting multiple favorite buttons"""
    favorites = forms.ModelMultipleChoiceField(
        queryset=FavoriteButton.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
    )

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user")  # Extract the user from kwargs
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        favorites_selected = cleaned_data.get("favorites")

        if len(favorites_selected) > 12:
            raise forms.ValidationError("You can only have up to 12 favorites.")
