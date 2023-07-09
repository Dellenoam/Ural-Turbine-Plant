from datetime import datetime
from django import forms
from django.forms import ModelForm, TextInput, DateInput, Textarea, FileInput, SelectMultiple, Select
from access_office.models import Document, Automobile, Driver, CrossingPoint, CustomStatus


class DocumentForm(ModelForm):
    class Meta:
        model = Document
        fields = ['status', 'custom_status', 'number_of_document', 'title', 'date_start', 'date_end',
                  'comment_for_access_office', 'comment_import', 'comment_export',
                  'crossing_point_name', 'document_file', 'auto']

        widgets = {
            'status': Select(attrs={
                'class': 'status_select',
            }),
            'custom_status': Select(attrs={
                'class': 'custom_status_select',
            }),
            'number_of_document': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Номер документа',
            }),
            'title': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Название документа',
            }),
            'date_start': DateInput(attrs={
                'class': 'form-control shadow-none',
                'id': 'date_start',
                'autocomplete': 'off',
                'placeholder': 'Дата начала документа',
            }),
            'date_end': DateInput(attrs={
                'class': 'form-control shadow-none',
                'id': 'date_end',
                'autocomplete': 'off',
                'placeholder': 'Дата окончания документа',
            }),
            'comment_for_access_office': Textarea(attrs={
                'class': 'md-textarea form-control shadow-none',
                'placeholder': 'Комментарий бюро',
                'rows': 4,
                'cols': 30,
            }),
            'comment_import': Textarea(attrs={
                'class': 'md-textarea form-control shadow-none',
                'placeholder': 'Ввоз',
                'rows': 4,
                'cols': 30,
            }),
            'comment_export': Textarea(attrs={
                'class': 'md-textarea form-control shadow-none',
                'placeholder': 'Вывоз',
                'rows': 4,
                'cols': 30,
            }),
            'crossing_point_name': SelectMultiple(attrs={
                'class': 'crossing_point_name_select',
            }),
            'document_file': FileInput(attrs={
                'class': 'form-control shadow-none',
            }),
            'auto': Select(attrs={
                'class': 'auto_select',
                'id': 'auto_select',
            }),
        }

    def clean(self):
        if self.cleaned_data.get('date_start') > datetime.now().date():
            self.cleaned_data['status'] = 'P'
        elif self.cleaned_data.get('date_end') < datetime.now().date():
            raise forms.ValidationError('Дата окончания не может быть меньше текущей даты.')
        else:
            self.cleaned_data['status'] = 'W'


class DocumentSecurityForm(ModelForm):
    class Meta:
        model = Document
        exclude = ['status', 'number_of_document', 'title', 'date_start', 'date_end',
                   'comment_for_access_office', 'crossing_point_name', 'document_file', 'auto']

        widgets = {
            'comment_for_security': Textarea(attrs={
                'id': 'comment_for_security',
                'class': 'md-textarea form-control shadow-none',
                'placeholder': 'Комментарий охраны',
                'rows': 4,
                'cols': 30,
            }),
        }


class AutomobileForm(ModelForm):
    class Meta:
        model = Automobile
        fields = ['license_plate', 'car_registration_number', 'car_brand', 'driver']

        widgets = {
            'license_plate': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Гос. рег. знак',
            }),
            'car_registration_number': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Номер свидетельства о рег. ТС',
            }),
            'car_brand': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Марка ТС',
            }),
            'driver': Select(attrs={
                'class': 'driver_select',
                'id': 'driver_select',
            })
        }


class DriverForm(ModelForm):
    class Meta:
        model = Driver
        fields = ['full_name', 'passport_details', 'date_of_birth', 'driver_license_number']

        widgets = {
            'full_name': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'ФИО',
            }),
            'passport_details': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Паспортные данные',
            }),
            'date_of_birth': TextInput(attrs={
                'class': 'form-control shadow-none',
                'id': 'date_of_birth',
                'autocomplete': 'off',
                'placeholder': 'Дата рождения',
            }),
            'driver_license_number': TextInput(attrs={
                'class': 'form-control shadow-none',
                'id': 'driver_license_number',
                'autocomplete': 'off',
                'placeholder': 'Номер водительского удостоверения',
            }),
        }


class CrossingPointForm(ModelForm):
    class Meta:
        model = CrossingPoint
        fields = ['crossing_point_name']

        widgets = {
            'crossing_point_name': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Пропукной пункт',
            }),
        }


class CustomStatusForm(ModelForm):
    class Meta:
        model = CustomStatus
        fields = ['custom_status']

        widgets = {
            'custom_status': TextInput(attrs={
                'class': 'form-control shadow-none',
                'placeholder': 'Кастомизируемый статус',
            }),
        }
