from django.urls import path
from . import views


urlpatterns = [
    path('package/types/', views.PackageTypeList.as_view()),
    path('packages/', views.PackageListFilter.as_view()),
    path('package/', views.PackageCreate.as_view()),
    # I wanted to use <int:pk>, but with a negative number
    # django raise error at the routing level
    path('package/<str:pk>/', views.PackageDetail.as_view()),
]
