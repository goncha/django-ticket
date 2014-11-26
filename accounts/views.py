from django.conf import settings
from django.contrib.auth import authenticate as auth_authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, resolve_url
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.http import require_http_methods


from accounts.forms import UserProfileForm
from accounts.models import UserProfile


@require_http_methods(['GET', 'POST'])
def login(request):
    context = {}
    if 'POST' == request.method:
        username = request.POST['username']
        password = request.POST['password']
        user = auth_authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                auth_login(request, user)
                next = request.POST['next'] or \
                       resolve_url(settings.LOGIN_REDIRECT_URL)
                return HttpResponseRedirect(next)
            else:
                context['error_message'] = _('Disabled account')
        else:
            context['error_message'] = _('Invalid username or password')
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
def register(request):
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
                    context['error_message'] = _('User already exists')
            else:
                context['error_message'] = _('Password not matched')
        else:
            context['error_message'] = _('Empty username or password')
    else:                       # GET method
        if request.user.is_authenticated():
            return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))

    return render(request, 'accounts/register.html', context)


@require_http_methods(['GET', 'POST'])
@login_required
def password(request):
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
                    context['info_message'] = _("New password saved")
                except User.DoesNotExist:
                    logout(request)
                    return HttpResponseNotFound("User `%s` not found" % (username,))
            else:
                context['error_message'] = _('Password not matched')
        else:
            context['error_message'] = _('Empty password')

    return render(request, 'accounts/password.html', context)


@login_required
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


@login_required
def home(request):
    return HttpResponseRedirect(resolve_url(settings.LOGIN_REDIRECT_URL))


@require_http_methods(['GET', 'POST'])
@login_required
def profile(request):
    context = {}
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            try:
                profile = UserProfile.objects.get(user_id=request.user.id)
                form.instance.pk = profile.pk
            except ObjectDoesNotExist:
                pass

            form.instance.user = request.user
            form.save()
            context['info_message'] = _('Profile saved')
    else:
        try:
            profile = UserProfile.objects.get(user_id=request.user.id)
            form = UserProfileForm(instance=profile)
        except ObjectDoesNotExist:
            form = UserProfileForm()

    context['form'] = form
    return render(request, 'accounts/profile.html', context)


@login_required
def hello(request):
    return HttpResponse('Hello, %s' % request.user.username)
