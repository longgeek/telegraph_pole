from django.contrib import admin
from models import Image
from models import Host
from models import Container
# Register your models here.

admin.site.register(Image)
admin.site.register(Host)
admin.site.register(Container)
