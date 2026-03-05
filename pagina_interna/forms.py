from django import forms
from .models import Vendedor


class VendedorForm(forms.ModelForm):
    class Meta:
        model = Vendedor
        
        fields = ["nome", "cpf", "email", "telefone", "foto", "ativo"]

        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-input"}),
            "cpf": forms.TextInput(attrs={"class": "form-input"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
            "telefone": forms.TextInput(attrs={"class": "form-input"}),

            "ativo": forms.CheckboxInput(attrs={"class": "form-checkbox"}),
            
            "foto": forms.ClearableFileInput(attrs={"class": "form-input"}),
        }