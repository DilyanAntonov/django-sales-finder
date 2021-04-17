from django import forms
from .models import ClothesSearch, ShoesSearch

class ClothesSearchForm(forms.ModelForm):
    class Meta:
        model = ClothesSearch
        fields = ('size', 'sex', 'brand', 'clothes_type')

        widgets = {
            'size': forms.Select(attrs={'class':'form-control'}),
            'sex': forms.Select(attrs={'class':'form-control'}),
            'brand': forms.Select(attrs={'class':'form-control'}),
            'clothes_type': forms.Select(attrs={'class':'form-control'})
        }

class ShoesSearchForm(forms.ModelForm):
    class Meta:
        model = ShoesSearch
        fields = ('size', 'sex', 'brand')

        widgets = {
            'size': forms.Select(attrs={'class':'form-control'}),
            'sex': forms.Select(attrs={'class':'form-control'}),
            'brand': forms.Select(attrs={'class':'form-control'}),
        }