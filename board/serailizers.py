from rest_framework import serializers
from .models import Post, Attachment


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ('file_name',)


class PostSerializer(serializers.ModelSerializer):
    attachment_list = AttachmentSerializer(many=True)

    class Meta:
        model = Post
        fields = ('id', 'url', 'title', 'body', 'published_datetime', 'site', 'attachment_list')
