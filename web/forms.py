from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.core.exceptions import ValidationError
from api.models import User, Group, Forum
from django import forms

class CustomFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'custom-select w-full h-12 px-3 py-2 agt-default-input'
                })
            elif isinstance(field.widget, forms.DateInput):
                field.widget.attrs.update({
                    'class': 'w-full h-12 px-3 py-2 agt-default-input',
                    'type': 'date'
                })
            else:
                field.widget.attrs.update({
                    'class': 'w-full h-12 px-3 py-2 agt-default-input'
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

class CustomAuthenticationForm(AuthenticationForm, CustomFormMixin):
    username = UsernameField(
        label= 'اسم المستخدم',
        widget=forms.TextInput(attrs={
            'autofocus': True, 
            'class': 'agt-default-input w-full px-3 py-2',
            'placeholder': 'اسم المستخدم'
        })
    )
    password = forms.CharField(
        strip=False,
        label= 'كلمة المرور',
        widget=forms.PasswordInput(attrs={
            'class': 'agt-default-input w-full px-3 py-2',
            'placeholder': 'كلمة المرور'
        }),
    )

    def confirm_login_allowed(self, user):
        if not user.is_active or not user.is_staff:
            raise ValidationError(
                self.error_messages["invalid_login"],
                code="invalid_login",
            )


class GroupForm(CustomFormMixin, forms.ModelForm):
    class Meta:
        model = Forum
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
                label='صورة:',
                required=False,
                label_suffix="",
                help_text="",
                widget=forms.FileInput(attrs={
                    'class': 'w-full px-3 py-2 agt-default-input'
                })
            )

            self.fields['is_active'] = forms.ChoiceField(
                label='مفعل؟',
                choices=[(True, 'نعم'), (False, 'لا')],
                widget=forms.RadioSelect(attrs={
                    'class': 'custom-radio',
                }),
                initial=self.instance.is_active
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.instance.pk:
            instance.is_active = True
        if commit:
            instance.save()
        return instance

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
                label='صورة:',
                required=False,
                label_suffix="",
                help_text="",
                widget=forms.FileInput(attrs={
                    'class': 'w-full px-3 py-2 agt-default-input'
                })
            )

            self.fields['is_active'] = forms.ChoiceField(
                label='مفعل؟',
                choices=[(True, 'نعم'), (False, 'لا')],
                widget=forms.RadioSelect(attrs={
                    'class': 'custom-radio',
                }),
                initial=self.instance.is_active
            )

    def save(self, commit=True):
        instance = super().save(commit=False)
        if not self.instance.pk:
            instance.is_active = True
        if commit:
            instance.save()
        return instance

class NotificationForm(forms.Form):
    title = forms.CharField(
        label='إضافة عنوان التنبيه',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border-b-2 border-red-500 bg-gray-100 text-gray-800',
            'placeholder': 'إضافة عنوان التنبيه'
        })
    )
    description = forms.CharField(
        label='إضافة نص التنبيه',
        widget=forms.Textarea(attrs={
            'class': 'w-full px-3 py-2 border-b-2 border-red-500 bg-gray-100 text-gray-800',
            'rows': 4,
            'placeholder': 'إضافة نص التنبيه'
        })
    )
    link = forms.URLField(
        label='إضافة رابط',
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-3 py-2 border-b-2 border-red-500 bg-gray-100 text-gray-800',
            'placeholder': 'إضافة رابط'
        })
    )