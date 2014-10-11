from django.contrib import admin

from .models import Contact, Location, Professional, Profile


admin.site.register(Contact)
admin.site.register(Location)
admin.site.register(Professional)
admin.site.register(Profile)