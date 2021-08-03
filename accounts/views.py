from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View


class Login(View):
    template_name = "accounts/login.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("accounts:user_redirect")

        return render(request, self.template_name)

    def post(self, request):
        try:
            username = request.POST["email"]
            pwd = request.POST["password"]

            user = auth.authenticate(username=username, password=pwd)

            if user is None:
                return JsonResponse({"status": False, "msg": "Invalid username or password"})

            auth.login(request, user)

            return JsonResponse({"status": True, "url": reverse("accounts:user_redirect")})
        except Exception as e:
            print("Exception in Login(post):", str(e))
            return JsonResponse({"status": False, "msg": "Something went wrong while processing your request. "
                                                         "Please try again."})


@login_required(login_url='/')
def user_redirect(request):
    if request.user.is_staff:
        return redirect("admin:index")

    if request.user.extendeduser.type == 'Staff':
        return redirect("staff:index")
    if request.user.extendeduser.type == 'Teacher':
        return redirect("teacher:index")
    if request.user.extendeduser.type == 'Student':
        return redirect("student:index")


def logout(request):
    auth.logout(request)
    return redirect("accounts:login")