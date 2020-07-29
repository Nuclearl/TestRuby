from django import forms

class RecordForm(forms.Form):
    post = forms.CharField()