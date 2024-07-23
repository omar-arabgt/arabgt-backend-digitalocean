from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

from api.models import *

class CustomFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            })
class UserForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nick_name', 'phone_number', 'birth_date', 'gender', 'nationality', 'country', 'has_business', 'has_car', 'car_type', 'hobbies', 'favorite_presenter', 'favorite_show']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'nick_name': 'اللقب',
            'phone_number': 'رقم الهاتف',
            'birth_date': 'تاريخ الميلاد',
            'gender': 'الجنس',
            'nationality': 'الجنسية',
            'country': 'البلد',
            'has_business': 'لديه عمل',
            'has_car': 'لديه سيارة',
            'car_type': 'نوع السيارة',
            'hobbies': 'هوايات',
            'favorite_presenter': 'المذيع المفضل',
            'favorite_show': 'العرض المفضل',
        }
        help_texts = {
            'username': 'مطلوب. 150 حرف أو أقل. حروف، أرقام و @/./+/-/_ فقط.',
        }


from api.models import *

class CustomFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
            })
class UserForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nick_name', 'phone_number', 'birth_date', 'gender', 'nationality', 'country', 'has_business', 'has_car', 'car_type', 'hobbies', 'favorite_presenter', 'favorite_show']
        labels = {
            'username': 'اسم المستخدم',
            'email': 'البريد الإلكتروني',
            'nick_name': 'اللقب',
            'phone_number': 'رقم الهاتف',
            'birth_date': 'تاريخ الميلاد',
            'gender': 'الجنس',
            'nationality': 'الجنسية',
            'country': 'البلد',
            'has_business': 'لديه عمل',
            'has_car': 'لديه سيارة',
            'car_type': 'نوع السيارة',
            'hobbies': 'هوايات',
            'favorite_presenter': 'المذيع المفضل',
            'favorite_show': 'العرض المفضل',
        }
        help_texts = {
            'username': 'مطلوب. 150 حرف أو أقل. حروف، أرقام و @/./+/-/_ فقط.',
        }



class CustomAuthenticationForm(CustomFormMixin, AuthenticationForm):
    username = UsernameField(
        label='',
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'placeholder': 'اسم المستخدم'
        })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'كلمة المرور'
        }),
        label=''
    )

    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_staff:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
            )
