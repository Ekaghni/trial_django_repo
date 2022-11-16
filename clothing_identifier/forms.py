from django import forms
from .models import *

class TempVideoForm(forms.ModelForm) :
   class Meta :
      model = TempVideo
      fields = '__all__'