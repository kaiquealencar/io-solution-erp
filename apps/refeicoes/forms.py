from django import forms
from .models import RefeicaoDia


class RefeicaoDiaForm(forms.ModelForm):
    class Meta:
        model = RefeicaoDia
        fields = "__all__"


    def clean_quantidade(self):
        quantidade = self.cleaned_data.get('quantidade')

        if quantidade is not None and quantidade <= 0:
            raise forms.ValidationError("A quantidade deve ser um número positivo.")
        
        return quantidade