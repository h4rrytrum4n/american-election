from django.contrib import admin
from .models import Hashtag
from .models import Tweet

# Register your models here.
admin.site.register(Hashtag)
admin.site.register(Tweet)