from django.urls import path

from .views import SearchFormView, ListResult, DetailResult


app_name = "search"

urlpatterns = [
    path("", SearchFormView.as_view(), name="search_form"),
    path("result/", ListResult.as_view(), name="list_result"),
    path("upload/<str:se>/<str:pk>/", DetailResult.as_view(), name="detail"),
]
