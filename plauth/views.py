import hashlib
import random
import string

import requests
from django.conf import settings
from django.contrib.auth import login, get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import transaction
from django.shortcuts import redirect
from django.utils.http import urlencode
from jwkest.jwk import RSAKey
from jwkest.jws import JWS
from requests.auth import HTTPBasicAuth
from pl.service.models import Service


def oidc_login(request):
    login_url = Service.objects.get(name='login').url

    def random_string():
        return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(12))

    params = {
        'client_id': settings.OIDC_CLIENT_ID,
        'response_type': 'code',
        'scope': ' '.join(settings.OIDC_SCOPES),
        'state': random_string(),
        'redirect_uri': settings.OIDC_REDIRECT_URI
    }
    oauth_url = '%s/openid/authorize?%s'
    response = redirect(oauth_url % (login_url, urlencode(params)))
    response.set_cookie('oidc_state', params['state'], 60*30, httponly=True, domain=settings.OIDC_STATE_COOKIE_DOMAIN)
    return response


def oidc_callback(request):
    login_url = Service.objects.get(name='login').url
    User = get_user_model()
    state = request.COOKIES.get('oidc_state')
    if not state or state != request.GET.get('state'):
        # if you've successfuly logged in, you're actually gonna make a round trip and come back here with a valid state.
        # you won't have to enter your credentials again
        return redirect(reverse('oidc_login'))

    client_id = settings.OIDC_CLIENT_ID
    client_secret = settings.OIDC_CLIENT_SECRET

    data = {
        'code': request.GET.get('code'),
        'redirect_uri': settings.OIDC_REDIRECT_URI,
        'grant_type': 'authorization_code',
    }

    token_url = '%s/openid/token/' % (login_url)

    response = requests.post(token_url, data, auth=HTTPBasicAuth(client_id, client_secret), verify=False) # TODO set to true when letsencrypt is set up

    json_response = response.json()

    access_token = json_response['access_token']
    id_token = json_response['id_token']

    rsa_key = [RSAKey(**settings.OIDC_PUBLIC_KEY)]
    _jws = JWS(alg='RS256')

    claim = _jws.verify_compact(id_token, rsa_key)
    user, created = User.objects.get_or_create(uuid=claim['sub'])


    userinfo_url = '%s/api/v1/user/%s/' % (login_url, claim['sub'])
    userinfo_response = requests.get(userinfo_url, headers={'Authorization': 'JWT {}'.format(id_token)}, verify=False) # TODO set to true when letsencrypt is set up
    user_data = userinfo_response.json()
    user.is_superuser = user_data['is_superuser']
    user.is_staff = user_data['is_staff']
    user.save()

    user.backend = 'django.contrib.auth.backends.ModelBackend'

    login(request, user)

    return redirect('/')