from django.urls import path
from . import views


urlpatterns = [
    path('package/types/', views.PackageTypeList.as_view() ),
    path('package/', views.PackageListCreate.as_view() ),
]