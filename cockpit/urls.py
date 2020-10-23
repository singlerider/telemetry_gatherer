import pathlib

import django
from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView


def graphiql(request):
    """Trivial view to serve the `graphiql.html` file."""
    del request
    graphiql_filepath = pathlib.Path(__file__).absolute().parent / "telemetry/graphiql.html"
    with open(graphiql_filepath) as f:
        return django.http.response.HttpResponse(f.read())


urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql", graphiql),
]
