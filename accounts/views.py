

from django.contrib import messages
from django.shortcuts import render, redirect

from accounts.forms import UserForm
from accounts.models import RolesEnum, UserProfile
from vendor.forms import VendorForm


# Create your views here.
def register_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.role = RolesEnum.CUSTOMER
            form.save()
            messages.success(request, 'Your account has been created!')
            return redirect("register_user")
    form = UserForm()
    context = {'form': form}
    return render(request, "accounts/register_user.html", context)


def register_vendor(request):
    user_form = UserForm()
    vendor_form = VendorForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if user_form.is_valid() and vendor_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            user.set_password(password)
            user.role = RolesEnum.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been created!, please wait for approval')
    context = {'user_form': user_form, 'vendor_form': vendor_form}
    return render(request, "accounts/register_vendor.html", context)
