from django.contrib import admin

from .models import GenericUser, Legal, Password


admin.site.register(GenericUser)
admin.site.register(Legal)
admin.site.register(Password)