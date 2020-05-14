from django.urls import path

from api import views

urlpatterns = [
    path("v2/books/", views.BookAPIVIewV2.as_view()),
    path("v2/books/<str:id>/", views.BookAPIVIewV2.as_view()),

    path("fanju/", views.Fanjuview.as_view()),
    path("fanju/<str:id>/", views.Fanjuview.as_view()),
]
