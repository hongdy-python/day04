from rest_framework.response import Response
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status


def exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    # print(exc, context)
    # 异常信息  一般具体的信息不给前端用户看
    error = "%s %s %s" % (context['view'], context['request'].method, exc)
    print(error)
    # 如果返回值为空，则异常需要自定义
    # 如果返回值不为空，则已经处理完成不需要自定义
    if response is None:
        return Response(
            {"error": "程序走神了，请稍等一会~"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR, exception=None)
    return response
