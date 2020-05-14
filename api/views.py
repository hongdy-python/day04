from rest_framework.response import Response
from rest_framework.views import APIView

from api import serializers
from api.models import Book, Fanju


class BookAPIVIewV2(APIView):
    def get(self, request, *args, **kwargs):

        book_id = kwargs.get("id")

        if book_id:
            try:
                book_obj = Book.objects.get(pk=book_id, is_delete=False)
                book_ser = serializers.BookModelSerializerV2(book_obj).data
                return Response({
                    "status": 200,
                    "message": "查询图书成功",
                    "results": book_ser
                })
            except:
                return Response({
                    "status": 200,
                    "message": "查询图书不存在",
                })
        else:
            book_list = Book.objects.filter(is_delete=False)
            book_data = serializers.BookModelSerializerV2(book_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询图书列表成功",
                "results": book_data
            })

    def post(self, request, *args, **kwargs):
        """
        只考虑增加单个
        同时完成添加多个对象
        """
        """
        单增：传的数据是与model类对应的一个字典
        群增：[ {} {} {} ]  群增的时候可以传递列表里面嵌套与model类对应的多个字典来完成群增
        """
        request_data = request.data

        if isinstance(request_data, dict):
            # 代表单增
            # book_ser = serializers.BookModelSerializerV2(data=request_data)
            many = False
        elif isinstance(request_data, list):
            # 代表秦增
            # book_ser = serializers.BookModelSerializerV2(data=request_data, many=True)
            many = True
        else:
            return Response({
                "status": 200,
                "message": "数据格式有误",
            })

        # 反序列化的时候需要将参数赋值关键字 data
        book_ser = serializers.BookModelSerializerV2(data=request_data, many=many)
        # 校验数据是否合法
        # raise_exception=True: 当校验失败的时候，马上终止当前视图方法，抛出异常到前台
        book_ser.is_valid(raise_exception=True)
        book_obj = book_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            # 报错
            "results": serializers.BookModelSerializerV2(book_obj, many=many).data
        })

    def delete(self, request, *args, **kwargs):
        """
        删除单个以及删除多个
        :param request: 请求的DRF对象
        # 单个删除：  有id  且是通过路径传参  v2/books/1/
        # 多个删除： 有多个id json传参 {"ids": [1,2,3]}
        """
        book_id = kwargs.get("id")
        if book_id:
            # 单删
            ids = [book_id]
        else:
            # 群删
            ids = request.data.get("ids")

        # 判断id是否图书存在 且未删除
        res = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if res:
            return Response({
                "status": 200,
                "message": "删除成功",
            })

        return Response({
            "status": 500,
            "message": "删除失败或者已删除",
        })

    def put(self, request, *args, **kwargs):
        """
        单整体改：修改一个对象的全部字段
        :param request:   获取修改对象的值
        :param kwargs:  需要知道我要修改哪个对象   获取修改对象的id
        :return:    更新后的对象
        """
        request_data = request.data
        book_id = kwargs.get("id")

        try:
            # 通过获取的id来找到要修改的对象
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "图书不存在",
            })

        # 前台提供了需要更新的数据request_data 数据更新需要校验
        # 更新数据时需要将参数赋值给data  方便钩子函数校验
        # 如果是修改操作，需要在序列化器中指定要修改的实例，否则将默认添加
        book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=False)
        book_ser.is_valid(raise_exception=True)

        # 如果校验通过 则保存
        book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            # 则修改完成的对象返回到前台，需要经过序列化器序列化
            "results": serializers.BookModelSerializerV2(book_obj).data
        })

    def patch(self, request, *args, **kwargs):
        """
        单局部改：修改一个对象的任意字段
        修改的字段不同
        """
        request_data = request.data
        book_id = kwargs.get("id")
        try:
            book_obj = Book.objects.get(pk=book_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "图书不存在",
            })
        # partial=True  指定序列化器为更新部分字段  有哪个字段的值就修改哪个字段  没有不修改
        book_ser = serializers.BookModelSerializerV2(data=request_data, instance=book_obj, partial=True)
        # 在数据校验之前告诉序列化器我要修改的是部分字段
        book_ser.is_valid(raise_exception=True)

        # 如果校验通过 则保存
        book_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            # 则修改完成的对象返回到前台，需要经过序列化器序列化
            "results": serializers.BookModelSerializerV2(book_obj).data
        })


#番剧表
class Fanjuview(APIView):
    def get(self,request, *args, **kwargs):
        fanju_id = kwargs.get("id")

        if fanju_id:
            try:
                fanju_obj = Fanju.objects.get(pk=fanju_id, is_delete=False)
                fanju_ser = serializers.FanjuSerializers(fanju_obj).data
                return Response({
                    "status": 200,
                    "message": "查询番剧成功",
                    "results": fanju_ser
                })
            except:
                return Response({
                    "status": 400,
                    "message": "查询番剧不存在",
                })
        else:
            fanju_list = Fanju.objects.filter(is_delete=False)
            fanju_data = serializers.FanjuSerializers(fanju_list, many=True).data

            return Response({
                "status": 200,
                "message": "查询番剧列表成功",
                "results": fanju_data
            })

    def post(self,request, *args, **kwargs):
        request_data = request.data
        if isinstance(request_data, dict):
            many = False
        elif isinstance(request_data, list):
            many = True
        else:
            return Response({
                "status": 300,
                "message": "数据格式有误",
            })

        fanju_ser = serializers.FanjuSerializers(data=request_data, many=many)
        fanju_ser.is_valid(raise_exception=True)
        fanju_obj = fanju_ser.save()

        return Response({
            "status": 200,
            "message": "success",
            "results": serializers.FanjuSerializers(fanju_obj, many=many).data
        })

    def delete(self,request, *args, **kwargs):
        fanju_id = kwargs.get("id")
        if fanju_id:
            ids = [fanju_id]
        else:
            ids = request.data.get("ids")
        res = Fanju.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if res:
            return Response({
                "status": 200,
                "message": "删除成功",
            })

        return Response({
            "status": 500,
            "message": "删除失败或者已删除",
        })

    def put(self,request, *args, **kwargs):
        request_data = request.data
        fanju_id = kwargs.get("id")

        try:
            fanju_obj = Fanju.objects.get(pk=fanju_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "番剧不存在",
            })
        fanju_ser = serializers.FanjuSerializers(data=request_data, instance=fanju_obj, partial=False)
        fanju_ser.is_valid(raise_exception=True)

        fanju_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.FanjuSerializers(fanju_obj).data
        })

    def patch(self,request, *args, **kwargs):
        request_data = request.data
        fanju_id = kwargs.get("id")
        try:
            fanju_obj = Fanju.objects.get(pk=fanju_id, is_delete=False)
        except:
            return Response({
                "status": 500,
                "message": "番剧不存在",
            })
        fanju_ser = serializers.FanjuSerializers(data=request_data, instance=fanju_obj, partial=True)

        fanju_ser.is_valid(raise_exception=True)

        fanju_ser.save()

        return Response({
            "status": 200,
            "message": "更新成功",
            "results": serializers.FanjuSerializers(fanju_obj).data
        })



