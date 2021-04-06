from django import forms
from .models import Search

class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ('url', 'size')

        widgets = {
            'url': forms.TextInput(attrs={'class':'form-control'}),
            'size': forms.Select(attrs={'class':'form-control'})
        }