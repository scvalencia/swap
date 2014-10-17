from django.contrib import admin

from .models import GenericUser, Legal


admin.site.register(GenericUser)
admin.site.register(Legal)