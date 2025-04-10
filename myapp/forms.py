from django import forms
from .models import GeneratedDocument, DocumentTemplate, UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['full_name', 'position', 'organization']


class DocumentForm(forms.Form):
    organization_name = forms.CharField(label='Название организации', max_length=255)
    inn = forms.CharField(label='ИНН', max_length=12)
    ogrn = forms.CharField(label='ОГРН', max_length=13)
    address = forms.CharField(label='Юридический адрес', max_length=255)
    responsible_person = forms.CharField(label='ФИО', max_length=255)
    position = forms.CharField(label='Должность', max_length=255)


class DocumentTemplateForm(forms.ModelForm):
    class Meta:
        model = DocumentTemplate
        fields = ['template_name', 'template_file']


def create_fill_template_form(tags):
    class FillTemplateForm(forms.Form):
        template_id = forms.IntegerField(widget=forms.HiddenInput())
        pass

    for tag in tags:
        FillTemplateForm.base_fields[tag] = forms.CharField(label=tag.replace('_', ' ').capitalize(), max_length=255)

    return FillTemplateForm
