from rest_framework import serializers

from api.models import Book


class BookListSerializer(serializers.ListSerializer):

    def update(self, instance, validated_data):
        for index, obj in enumerate(instance):
            self.child.update(obj, validated_data[index])
        return instance


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name", "price", "pic", "authors", "publish", "author_list", "publish_name",)

        list_serializer_class = BookListSerializer

        extra_kwargs = {
            "book_name": {
                "required": True,
                "min_length": 3,
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度不够"
                }
            },
            "authors": {"write_only": True},
            "publish": {"write_only": True},
            "author_list": {"read_only": True},
            "publish_name": {"read_only": True },
            "pic": {"read_only": True},
        }

