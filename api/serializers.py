from rest_framework import serializers

from api.models import Book, Press, Fanju


class PressModelSerializer(serializers.ModelSerializer):
    class Meta:
        # 执行序列化的类  为图书查询的时候提供对应的出版社的信息
        model = Press
        # 指定字段
        fields = ("press_name", "address", "id")

class BookModelSerializerV2(serializers.ModelSerializer):
    class Meta:
        model = Book
        # filed 应该填写哪些字段  应该填写序列化与反序列所有字段的并集
        fields = ("book_name", "price", "pic", "authors", "publish", "author_list", "publish_name",)
        # 为序列化与反序列化的字段提供校验规则
        # 可以通过write_only属性指定哪个字段只参与反序列化  read_only指定只参与序列化
        extra_kwargs = {
            "book_name": {
                "required": True,  # 设置为必填字段
                "min_length": 2,  # 设置最小长度
                "error_messages": {
                    "required": "图书名是必填的",
                    "min_length": "图书名长度不够"
                }
            },
            # 只参与反序列化
            "authors": {"write_only": True},
            "publish": {"write_only": True},
            # 只参与序列化
            "author_list": {"read_only": True},
            "publish_name": {"read_only": True},
            "pic": {"read_only": True},
        }

    # 自己添加额外的校验规则  局部钩子
    def validate_book_name(self, value):
        # 检查图书名是否存在
        if "zz" in value:
            raise serializers.ValidationError("zz图书已存在")
        else:
            return value

    def validate(self, attrs):
        publish = attrs.get("publish")
        book_name = attrs.get("book_name")
        # 一个出版社不能发布重复的书籍名
        book_obj = Book.objects.filter(book_name=book_name, publish=publish)
        if book_obj:
            raise serializers.ValidationError("该出版社已经发布过该图书")

        return attrs

class FanjuSerializers(serializers.ModelSerializer):
    class Meta:
        model = Fanju
        fields = ("name","author","mount")
        extra_kwargs = {
            "name": {
                "required": True,
                "min_length": 2,
                "error_messages": {
                    "required": "番剧名是必填的",
                    "min_length": "番剧名长度不够"
                                    }
                    },
            "authors": {"required": True, },
            "mount": {"required": True, },
        }