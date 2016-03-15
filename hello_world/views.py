from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext


def index(request):
    return render_to_response('index.html',
                              context_instance=RequestContext(request))


@login_required
def authenticated(request):
    return render_to_response('authenticated.html',
                              context_instance=RequestContext(request))