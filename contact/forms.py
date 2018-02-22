from django import forms
from .models import Contact, ContactInfo


class ContactFormGr(forms.ModelForm):
    #date = forms.DateTimeField(widget=forms.HiddenInput())
    class Meta:
        model = Contact
        fields = '__all__'
        exclude =['date', 'is_readed']



class ContactFormEng(forms.ModelForm):
    #date = forms.DateTimeField(widget=forms.HiddenInput())
    class Meta:
        model = Contact
        fields = '__all__'
        exclude =['date', 'is_readed']


class ContactInfoForm(forms.ModelForm):

    class Meta:
        model = ContactInfo
        fields ='__all__'
        exclude = ['date']