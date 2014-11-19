from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.views.decorators.http import require_http_methods

@require_http_methods(['GET', 'POST'])
def login_view(request):
    context = {}
    if 'POST' == request.method:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                next = request.POST['next'] or \
                       resolve_url(settings.LOGIN_REDIRECT_URL)
                return HttpResponseRedirect(next)
            else:
                context['error_message'] = 'Disabled account'
        else:
            context['error_message'] = 'Invalid username or password'
        context['username'] = username
    else:                       # GET method
        if request.user.is_authenticated():
            return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))
        else:
            next = request.GET.get('next')
            if next:
                context['next'] = next

    return render(request, 'accounts/login.html', context)


@require_http_methods(['GET', 'POST'])
def register_view(request):
    context = {}

    if 'POST' == request.method:
        username = request.POST['username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        context['username'] = username

        if username and password and repassword:
            if password == repassword:
                try:
                    User.objects.get(username=username)
                except User.DoesNotExist:
                    user = User.objects.create_user(username, password=password)
                    user.save()
                    return render(request, 'accounts/register_result.html', {
                        'login_url': resolve_url(settings.LOGIN_URL),
                    })
                else:
                    context['error_message'] = 'User already exists'
            else:
                context['error_message'] = 'Password not matched'
        else:
            context['error_message'] = 'Empty username or password'
    else:                       # GET method
        if request.user.is_authenticated():
            return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))

    return render(request, 'accounts/register.html', context)


@require_http_methods(['GET', 'POST'])
@login_required
def password_view(request):
    username = request.user.username
    context = {'username': username }

    if 'POST' == request.method:
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password and repassword:
            if password == repassword:
                try:
                    user = User.objects.get(username=username)
                    user.set_password(password)
                    user.save()
                    context['info_message'] = "Password has been changed"
                except User.DoesNotExist:
                    logout(request)
                    return HttpResponseNotFound("User `%s` not found" % (username,))
            else:
                context['error_message'] = 'Password not matched'
        else:
            context['error_message'] = 'Empty password'

    return render(request, 'accounts/password.html', context)


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


@login_required
def home_view(request):
    return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@login_required
def profile_view(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)


@login_required
def hello_view(request):
    return HttpResponse('Hello, %s' % request.user.username)
