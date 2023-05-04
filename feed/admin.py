from django.contrib import admin
from .models import FeedPost, Comment, Tags
# Register your models here.

admin.site.register(FeedPost)
admin.site.register(Comment)
admin.site.register(Tags)
