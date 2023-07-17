from django.views.generic import (TemplateView, FormView)
from django.contrib.auth.views import (LoginView, LogoutView)
from django.contrib.auth.forms import UserCreationForm
from devices.views import DeviceListView, UserDeviceListView

def home(request):
    if request.user.is_superuser:
        return DeviceListView.as_view()(request)
    elif request.user.is_authenticated:
        return UserDeviceListView.as_view()(request)
    else:
        return HomePageView.as_view()(request)

class RegisterPageView(FormView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/login/'
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
class HomePageView(TemplateView):
    template_name='home.html'

class LoginPageView(LoginView):
    template_name='registration/login.html'
    next_page='/'

class LogoutPageView(LogoutView):
    next_page='/'
