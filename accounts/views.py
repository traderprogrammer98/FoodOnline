from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.urls import reverse

from accounts.decorators import role_required
from accounts.forms import UserForm, LoginForm
from accounts.models import UserProfile, User
from vendor.forms import VendorForm


# Create your views here.
def register_user(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = UserForm()
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.role = User.Role.CUSTOMER
            user.save()
            messages.success(request, 'Your account has been created!')
            return redirect("register_user")
    context = {'form': form}
    return render(request, "accounts/register_user.html", context)


def register_vendor(request):
    if request.user.is_authenticated:
        return redirect("home")
    user_form = UserForm()
    vendor_form = VendorForm()
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if user_form.is_valid() and vendor_form.is_valid():
            user = user_form.save(commit=False)
            password = user_form.cleaned_data.get('password')
            user.set_password(password)
            user.role = User.Role.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            messages.success(request, 'Your account has been created!, please wait for approval')
            return redirect("register_vendor")
    context = {'user_form': user_form, 'vendor_form': vendor_form}
    return render(request, "accounts/register_vendor.html", context)


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, email=form.cleaned_data.get('email'),
                                password=form.cleaned_data.get('password'))
            if user is not None:
                auth.login(request, user)
                messages.success(request, 'You are now logged in!')
                if user.role == User.Role.CUSTOMER:
                    return redirect("customer_dashboard")
                elif user.role == User.Role.VENDOR:
                    return redirect("vendor_dashboard")
                else:
                    return redirect(reverse("admin:index"))
            else:
                messages.error(request, 'Invalid email or password')
                return redirect("login")
    context = {'form': form}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are now logged out!')
    return redirect("login")


@role_required(User.Role.CUSTOMER)
def customer_dashboard(request):
    return render(request, 'accounts/customer_dashboard.html')


@role_required(User.Role.VENDOR)
def vendor_dashboard(request):
    return render(request, 'accounts/vendor_dashboard.html')
