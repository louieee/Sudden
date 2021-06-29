from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST


class APISuccess:
    def __new__(cls, message='Success', data=None, status=HTTP_200_OK):
        if data is None:
            data = {}
        return Response(
            {
                'status': True,
                'message': message,
                'data': data
            },
            status
        )


class APIFailure:
    def __new__(cls, message='Error', status=HTTP_400_BAD_REQUEST):
        return Response(
            {
                'status': False,
                'message': message
            },
            status
        )
