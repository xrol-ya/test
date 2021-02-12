import datetime

from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django import forms


class ReviewForm(forms.Form):
    review = forms.CharField(max_length=1000, help_text='Оставьте свой отзыв для этой книги')

    def clean_review(self):
        data = self.cleaned_data['review']

        if data == '':
            raise ValidationError('Не оставляйте это поле пустым')

        return data


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100, help_text='Введите ваше имя', widget=forms.TextInput(attrs={'class': 'input'}))
    last_name = forms.CharField(max_length=100, help_text='Введите вашу фамилию',
                                widget=forms.TextInput(attrs={'class': 'input'}))
    username = forms.CharField(max_length=100, help_text='Введите username',
                               widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input'}),
                                       help_text='Повторите пароль')
    email = forms.EmailField(help_text='Введите вашу эл. почту', widget=forms.TextInput(attrs={'class': 'input'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password', 'confirm_password')


class MyAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=30, widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'input'}))

    def __init__(self, *args, **kwargs):
        super(MyAuthenticationForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'input'

    def confirm_login_allowed(self, user):
        if not user:
            raise forms.ValidationError('Пользователь не найден')
        elif not user.is_active or not user.is_validated:
            raise forms.ValidationError('Была проблема с твоим логином', code='invalid_login')


class BorrowBookForm(forms.Form):
    due_date = forms.DateField(help_text='Введите дату возврата')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError('Недействительная дата - обновление в прошлом')
        return data


class RenewBookForm(forms.Form):
    renewal_date = forms.DateField(help_text='Введите дату между сегодняшним днем и 4 неделями (по умолчанию 3)')

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']

        if data < datetime.date.today():
            raise ValidationError('Недействительная дата - обновление в прошлом')

        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError('Недействительная дата - продление более чем на 4 недели вперед.')

        return data