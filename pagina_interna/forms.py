from django import forms
from .models import Vendedor
from .models import Cliente


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

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "cpf_cnpj", "email", "telefone", "ativo"]
        widgets = {
            "nome": forms.TextInput(attrs={"class": "form-input", "placeholder": "Ex: João da Silva"}),
            "cpf_cnpj": forms.TextInput(attrs={"class": "form-input", "placeholder": "000.000.000-00", "id": "id_cpf_cnpj"}),
            "email": forms.EmailInput(attrs={"class": "form-input", "placeholder": "email@exemplo.com"}),
            "telefone": forms.TextInput(attrs={"class": "form-input", "placeholder": "(00) 00000-0000", "id": "id_telefone"}),
            "ativo": forms.CheckboxInput(attrs={"class": "form-switch-input", "id": "id_ativo"}),
        }
    
    def clean_cpf_cnpj(self):
        valor = self.cleaned_data.get("cpf_cnpj", "")
        apenas_digitos = "".join(filter(str.isdigit, valor))

        if len(apenas_digitos) not in (11, 14):
            raise forms.ValidationError("CPF deve ter 11 dígitos ou CNPJ deve ter 14 dígitos.")
        return apenas_digitos
    
    def clean_telefone(self):
        valor = self.cleaned_data.get("telefone", "")
        return ''.join(filter(str.isdigit, valor))