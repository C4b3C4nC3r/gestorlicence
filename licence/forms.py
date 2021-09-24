from django import forms
from .models import Client,CodeLicence


class ClientForm (forms.ModelForm):
    class Meta:
        model = Client
        fields =  ['name','last_name','number_phone','email','url_client','nci']


class CodeLicenceForm (forms.ModelForm):
    class Meta:
        model = CodeLicence
        fields = ['hash_licence','type_licence','create_at','date_rem']

