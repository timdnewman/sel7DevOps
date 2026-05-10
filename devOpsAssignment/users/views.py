from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

from .forms import LoginForm

# Create your views here.
class UserLoginView(LoginView):

    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):

    next_page = reverse_lazy("users:login")