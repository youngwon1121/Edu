from django.db import models


class Site(models.TextChoices):
    IAM = 'IAM'
    NAVERBLOG = 'NAVERBLOG'
    BBC = 'BBC'


class PostSequence(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Post(models.Model):
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    body = models.TextField()
    published_datetime = models.DateTimeField()
    hash_content = models.CharField(max_length=64, unique=True)
    site = models.CharField(
        max_length=10,
        choices=Site.choices
    )
    sequence = models.ForeignKey(PostSequence, on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return self.title


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachment_list")
    file_name = models.CharField(max_length=300)

    def __str__(self):
        return self.file_name
