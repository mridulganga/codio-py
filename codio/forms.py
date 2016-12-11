from django import forms
from .models import code

class submit_form(forms.ModelForm):
    class Meta:
        model = code
        fields = ('title','usage','code_text','input_output','tags')
