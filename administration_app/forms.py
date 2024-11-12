from django import forms
from administration_app.models import User, CustomGroup, Permissions, PermissionApp
from django.contrib.auth.forms import UserCreationForm


class SuperuserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class NormalUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class CustomGroupCreationForm(forms.ModelForm):
    class Meta:
        model = CustomGroup
        fields = "__all__"


# ------------------------------ User Password Change Form (Only Super Admin)----------------------------------
class SuperuserChangePasswordForm(forms.Form):
    new_password = forms.CharField(label="New Password", widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label="Confirm New Password", widget=forms.PasswordInput
    )

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get("new_password")
        confirm_password = cleaned_data.get("confirm_password")

        if new_password and confirm_password and new_password != confirm_password:
            self.add_error("confirm_password", "New passwords do not match.")

        return cleaned_data

    def save(self, user):
        new_password = self.cleaned_data["new_password"]
        user.set_password(new_password)
        user.save()


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["first_name", "email", "password1", "password2"]

    def save(self, commit=True):
        user = super(RegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# class RegistrationForm(forms.ModelForm):
#     password = forms.CharField(widget=forms.PasswordInput, label="Password")
#     confirm_password = forms.CharField(
#         widget=forms.PasswordInput, label="Confirm Password"
#     )

#     class Meta:
#         model = User
#         fields = ["first_name", "email", "password"]

#     def clean(self):
#         cleaned_data = super().clean()
#         password = cleaned_data.get("password")
#         confirm_password = cleaned_data.get("confirm_password")

#         if password != confirm_password:
#             raise forms.ValidationError("Passwords do not match")

#         return cleaned_data


class SuperuserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class NormalUserRegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "password", "first_name", "last_name"]


class PermissionsForm(forms.ModelForm):
    class Meta:
        model = Permissions
        fields = "__all__"


class PermissionAppForm(forms.ModelForm):
    class Meta:
        model = PermissionApp
        fields = "__all__"
