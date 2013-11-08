# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
    print request.user
    if request.user.is_authenticated():
        return HttpResponse('authenticate %s <a href = "/accounts/logout/"> logout </a>,  <a href = "/accounts/logout_redirect">logout redirect</a> \t<a href="/accounts/password_change/">change_password</a>\t<a href="/accounts/password/reset/"> reset password</a>'  % request.user.username )

    return HttpResponse('unauthenticate, <a href="/accounts/login/">login</a>')
