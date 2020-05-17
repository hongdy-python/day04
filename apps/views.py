from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin
from rest_framework.generics import ListCreateAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from api.models import Book
from apps import serializers
from apps.serializers import BookModelSerializer
from utils.response import MYResponse


class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        book_list = Book.objects.filter(is_delete=False).all()
        book_ser = serializers.BookModelSerializer(book_list, many=True)
        book_data = book_ser.data

        return MYResponse(results=book_data)


class BookGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         GenericAPIView):
    queryset = Book.objects.filter(is_delete=False).all()
    serializer_class = BookModelSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            response = self.retrieve(request, *args, **kwargs)
        else:
            response = self.list(request, *args, **kwargs)

        return MYResponse(results=response.data, data_message="查询成功")

    def post(self, request, *args, **kwargs):
        response = self.create(request, *args, **kwargs)
        return MYResponse(results=response.data)

    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return MYResponse(results=response.data)

    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return MYResponse(results=response.data)


class BookListCreateAPIView(ListCreateAPIView):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer


class BookGenericViewSet(RetrieveModelMixin,
                         ListModelMixin,
                         GenericViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer

    def my_list(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def my_obj(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def my_create(self, request, *args, **kwargs):
        request_data = request.data
        print(request_data)
        return MYResponse(results="OK")

    def my_destroy(self, request, *args, **kwargs):
        book_obj = self.get_object()
        print("book_obj", book_obj, type(book_obj))
        if not book_obj:
            return MYResponse(500, "删除失败")
        book_obj.is_delete = True
        book_obj.save()
        return MYResponse(200, "删除成功")


class BookExampleGenericViewSet(ModelViewSet):
    queryset = Book.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer

