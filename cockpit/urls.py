from django.contrib import admin
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from django.urls import path
from graphene_subscriptions.views import GraphQLSubscriptionView

urlpatterns = [
    path("admin/", admin.site.urls),
    path('graphql/', GraphQLSubscriptionView.as_view()),
]
