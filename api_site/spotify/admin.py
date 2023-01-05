from django.contrib import admin
from .models import SpotifyToken
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(SpotifyToken)