from django import forms

class SearchEngine(forms.Form):
    your_query = forms.CharField(label='', max_length=500)