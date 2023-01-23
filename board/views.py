from django.db import transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from board.serailizers import PostSerializer
from board.services import get_post


@api_view(['POST'])
@transaction.atomic
def get(request: Request):
    if request.method == "POST":
        if request.data.get('url') is None:
            return Response({"message": "Field 'url' is empty"}, status=status.HTTP_400_BAD_REQUEST)

        posts = get_post(request.data['url'])
        serializer = PostSerializer(posts, many=True)
        return Response(
            {'count': len(serializer.data), 'data': serializer.data},
            status=status.HTTP_200_OK
        )
