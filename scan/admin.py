from django.contrib import admin

from scan.models import Scaner, Session

# Register your models here.

admin.site.register(Scaner)
admin.site.register(Session)