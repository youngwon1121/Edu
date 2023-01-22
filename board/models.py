from django.db import models


class Site(models.TextChoices):
    IAM = 'IAM'
    NAVERBLOG = 'NAVERBLOG'
    BBC = 'BBC'


class Post(models.Model):
    url = models.CharField(max_length=300)
    title = models.CharField(max_length=300)
    body = models.TextField()
    published_datetime = models.DateTimeField()
    site_id = models.CharField(max_length=100)
    site = models.CharField(
        max_length=10,
        choices=Site.choices
    )

    def __str__(self):
        return self.title


class Attachment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="attachment_list")
    file_name = models.CharField(max_length=300)

    def __str__(self):
        return self.file_name
