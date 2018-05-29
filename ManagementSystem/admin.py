from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.User)
admin.site.register(models.UC_Chapter)
admin.site.register(models.Section)
admin.site.register(models.Class)
admin.site.register(models.Students)
admin.site.register(models.Enrollment)
admin.site.register(models.Batch)