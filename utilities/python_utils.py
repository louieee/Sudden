from customer.models import Client

public = 'localhost:8000'


def get_schema(request):
    schema = request.META.get('HTTP_X_DTS_SCHEMA', None)
    if schema is None:
        host = request.get_host().split(public)[0][:-1]
        if Client.objects.filter(schema_name=host.replace('.', '_')).exists():
            return host
        return 'public'
    return schema


def get_schema_from_url(url, local='localhost'):
    return url.split(local)[0][:-1].replace('.', '_')
