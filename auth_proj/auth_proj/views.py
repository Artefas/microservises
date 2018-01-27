from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse


@login_required()
def secret_page(request, *args, **kwargs):
    return HttpResponse('OK', status=200)

@login_required()
def get_user(request, *args, **kwargs):
    return HttpResponse(request.user, status=200)

