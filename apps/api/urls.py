from django.urls import path
from . import views


urlpatterns = [
    path('package/types/', views.PackageTypeList.as_view()),
    path('packages/', views.PackageListFilter.as_view()),
    path('package/', views.PackageCreate.as_view()),
    path('package/<int:pk>/', views.PackageDetail.as_view()),
]
