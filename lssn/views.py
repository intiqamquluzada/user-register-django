from django.shortcuts import render
from lssn.forms import RegistrationUserForm


def register_view(request):
    form = RegistrationUserForm()

    if request.method == "POST":
        form = RegistrationUserForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data.get("password1"))
            new_user.is_active = True
            new_user.save()


    context = {
        "form": form,
    }
    return render(request, "register.html", context)
