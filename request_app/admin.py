from django.contrib import admin
from .models import DataRequest, DataRequestLog

# Register your models here.
admin.site.register(DataRequest)
admin.site.register(DataRequestLog)
