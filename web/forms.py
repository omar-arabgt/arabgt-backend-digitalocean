from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from api.models import User, Group, Forum

class CustomFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'custom-select w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400 appearance-none bg-white'
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
                    'type': 'date'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
                })

class UserForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'nick_name', 'phone_number', 'birth_date', 'gender', 'nationality', 'country', 'has_business', 'has_car', 'car_type', 'hobbies', 'favorite_presenter', 'favorite_show']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }
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


class ForumForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Forum
        fields = ['name', 'image']
        labels = {
            'name': 'اسم المنتدى',
            'image': 'صورة',   
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields['image']
            self.fields['image'] = forms.FileField(
                label=':صورة',
                required=False,
                label_suffix="",
                help_text="",
                widget=forms.FileInput(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
                })
            )
            self.fields['is_active'] = forms.BooleanField(
                label='مفعل؟',
                initial=self.instance.is_active,
                required=False,
            )
        else:
            self.fields['image'].label = 'صورة'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.instance.pk:
            instance.is_active = True
        elif 'is_active' in self.cleaned_data:
            instance.is_active = self.cleaned_data['is_active']
        if commit:
            instance.save()
        return instance

class CustomAuthenticationForm(AuthenticationForm):
    username = UsernameField(
        label='',
        widget=forms.TextInput(attrs={
            'autofocus': True, 
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
            'placeholder': 'اسم المستخدم'
        })
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400',
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

class GroupForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'image']
        labels = {
            'name': 'اسم المجموعة',
            'image': 'صورة',   
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields['image']
            self.fields['image'] = forms.FileField(
                label=':صورة',
                required=False,
                label_suffix="",
                help_text="",
                widget=forms.FileInput(attrs={
                    'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-400'
                })
            )
            self.fields['is_active'] = forms.BooleanField(
                label='مفعل؟',
                initial=self.instance.is_active,
                required=False,
            )
        else:
            self.fields['image'].label = 'صورة'

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.instance.pk:
            instance.is_active = True
        elif 'is_active' in self.cleaned_data:
            instance.is_active = self.cleaned_data['is_active']
        if commit:
            instance.save()
        return instance
