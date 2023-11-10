from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()


class UserAdminCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password1', 'password2')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'name', 'surname', 'password', 'is_active', 'is_superuser')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class RegistrationUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Şifrə"}))
    password2 = forms.CharField(label='Təkrar şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Təkrar şifrə"}))

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({"class": "form-control"})
            self.fields[field].required = True
        self.fields["name"].widget.attrs.update({"placeholder": "Adınızı daxil edin"})
        self.fields["email"].widget.attrs.update({"placeholder": "E-poçtunuzu daxil edin"})

    def clean(self):
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        # for n in phone:
        #     if n.isalpha():
        #         raise forms.ValidationError("Nömrəni düzgün daxil edin")

        if not (password1 and password2 and password1 == password2):
            raise forms.ValidationError("Şifrələr uyğun deyil")

        if len(password1) < 8:
            raise forms.ValidationError("Şifrənin uzunluğu minimum 8 simvoldan ibarət olmalıdır.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu e-poçtla hesab mövcuddur")

        return self.cleaned_data
