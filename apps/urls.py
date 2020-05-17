from django.urls import path

from apps import views

urlpatterns = [

    path("books/", views.BookAPIView.as_view()),
    path("books/<str:id>/", views.BookAPIView.as_view()),

    path("v1/books/", views.BookGenericAPIView.as_view()),
    path("v1/books/<str:id>/", views.BookGenericAPIView.as_view()),

    path("v2/books/", views.BookGenericAPIView.as_view()),
    path("v2/books/<str:id>/", views.BookGenericAPIView.as_view()),

    path("v3/books/", views.BookGenericViewSet.as_view({'get': 'my_list', 'post': 'my_create'})),
    path("v3/books/<str:pk>/", views.BookGenericViewSet.as_view({'get': 'my_obj', 'delete': 'my_destroy'})),

]
