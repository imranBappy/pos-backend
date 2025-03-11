"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from backend.schema import schema
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from apps.product.views import generate_invoice
from  apps.clients  import views as client_views
from django.http import HttpResponseForbidden

def tenant_admin_view(request):
    if not request.user.is_authenticated or not request.user.is_admin:
        return HttpResponseForbidden("Access Denied")
    return admin.site.urls

urlpatterns = [
    path("admin/", admin.site.urls),

    path("graphql/", csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))),
    path('invoice/<int:order_id>/', generate_invoice, name='generate_invoice'),
    path('', client_views.index)
]
