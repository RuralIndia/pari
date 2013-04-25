from .models import Type


def types(request):
    return {'types': Type.objects.all()}
