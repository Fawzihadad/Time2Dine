from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import login


def register(request):

    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():

            user = form.save(commit=False)

            # save email from form
            user.email = request.POST.get("email")

            # require email verification
            user.is_active = False
            user.save()

            current_site = get_current_site(request)

            subject = "Activate your Time2Dine account"

            message = render_to_string("emails/email_verification.html", {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": default_token_generator.make_token(user),
                "protocol": "http",
            })

            send_mail(
                subject,
                "",
                "noreply@time2dine.com",
                [user.email],
                html_message=message,
            )

            return render(request, "accounts/verify_email.html")

    else:
        form = UserCreationForm()

    return render(request, "accounts/register.html", {"form": form})


def activate(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    # If user exists
    if user is not None:

        # If account already activated
        if user.is_active:
            login(request, user)
            return redirect("home")

        # Validate token
        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()

            login(request, user)

            return render(request, "accounts/activation_success.html")

    return render(request, "accounts/activation_invalid.html")