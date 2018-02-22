from django import forms
from .models import NewsLetter

my_default_errors = {
    'required': 'This field is required',
    'invalid': 'Enter a valid value',
    'unique': 'This email already exists!',
}


class NewsLetterForm(forms.ModelForm):
    email = forms.EmailField(error_messages=my_default_errors)
    class Meta:
        model = NewsLetter
        fields = ['email']



