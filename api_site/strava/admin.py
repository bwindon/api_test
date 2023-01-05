from django.contrib import admin
from .models import StravaToken, ActivityData, ActivityObject
# Register your models here.


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(StravaToken)
admin.site.register(ActivityData)
admin.site.register(ActivityObject)

