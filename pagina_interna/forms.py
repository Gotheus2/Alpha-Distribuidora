from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from .models import Vendedor


class FotoVendedorWidget(forms.ClearableFileInput):

    def render(self, name, value, attrs=None, renderer=None):
        
        file_attrs = {"class": "form-input", "id": f"id_{name}"}
        file_input = format_html(
            '<input type="file" name="{}" id="{}" class="form-input" accept="image/*">',
            name,
            f"id_{name}",
        )

        if not value or not getattr(value, "url", None):
            
            return file_input

        checkbox_name = self.clear_checkbox_name(name)
        checkbox_id   = self.clear_checkbox_id(checkbox_name)

        return format_html(
            '<div class="foto-preview-wrap">'
              '<img src="{url}" class="foto-preview-img" alt="Foto atual">'
              '<label class="foto-clear-row">'
                '<input type="checkbox" name="{cb_name}" id="{cb_id}">'
                '<span class="foto-clear-label">Remover foto</span>'
              '</label>'
              '<span class="form-label" style="display:block;margin-top:10px;">Alterar foto</span>'
              '{file_input}'
            '</div>',
            url=value.url,
            cb_name=checkbox_name,
            cb_id=checkbox_id,
            file_input=file_input,
        )


class VendedorForm(forms.ModelForm):
    ativo = forms.BooleanField(required=False)

    class Meta:
        model = Vendedor
        fields = ["nome", "cpf", "email", "telefone", "foto", "ativo"]
        widgets = {
            "nome":     forms.TextInput(attrs={"class": "form-input"}),
            "cpf":      forms.TextInput(attrs={"class": "form-input"}),
            "email":    forms.EmailInput(attrs={"class": "form-input"}),
            "telefone": forms.TextInput(attrs={"class": "form-input"}),
            "foto":     FotoVendedorWidget(attrs={"class": "form-input"}),
        }

    def clean_ativo(self):
        val = self.data.get("ativo", "false")
        return str(val).lower() in ("true", "on", "1")