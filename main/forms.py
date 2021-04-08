from django import forms
from .models import Search

class SearchForm(forms.ModelForm):
    class Meta:
        model = Search
        fields = ('size', 'sex', 'brand', 'clothes_type')

        widgets = {
            # 'url': forms.TextInput(attrs={'class':'form-control'}),
            'size': forms.Select(attrs={'class':'form-control'}),
            'sex': forms.Select(attrs={'class':'form-control'}),
            'brand': forms.Select(attrs={'class':'form-control'}),
            'clothes_type': forms.Select(attrs={'class':'form-control'})
        }