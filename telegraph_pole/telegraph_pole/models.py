from django.db import models
from django.utils.translation import ugettext as _


class Image(models.Model):
    OS_TYPES = (
        ('ubuntu', 'Ubuntu'),
        ('centos', 'Centos'),
    )
    iid = models.CharField(max_length=80)
    tag = models.CharField(max_length=20)
    created = models.CharField(max_length=40)
    repository = models.CharField(max_length=20)
    virtual_size = models.CharField(max_length=20)
    os_type = models.CharField(max_length=25, choices=OS_TYPES,
                               null=True, blank=True)
    os_version = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        app_label = "apphome"

Flavor = {
    '1': {
        'cpu': 1,
        'mem': 128,  # MB
        'name': 'tiny',
        'volume': 0,  # MB
        'sys_disk': 5120,  # MB
        'bandwidth': 512,  # KB
    },
    '2': {
        'cpu': 1,
        'mem': 256,  # MB
        'name': 'small',
        'volume': 0,  # MB
        'sys_disk': 10240,  # MB
        'bandwidth': 1024,  # MB
    },
    '3': {
        'cpu': 1,
        'mem': 512,  # MB
        'name': 'standard',
        'volume': 0,  # MB
        'sys_disk': 10240,  # MB
        'bandwidth': 1024,  # MB
    }
}


class Host(models.Model):
    ip = models.CharField(max_length=150)
    port = models.CharField(max_length=20)
    image = models.ManyToManyField(Image)
    status = models.BooleanField(_("Status"), default=True)
    total_cpu = models.IntegerField()   # Cores
    total_mem = models.IntegerField()   # GB
    total_sys_disk = models.IntegerField()  # GB
    total_volume = models.IntegerField()    # GB
    total_bandwidth = models.IntegerField()    # MB

    class Meta:
        app_label = "apphome"


class Container(models.Model):
    cid = models.CharField(max_length=80, null=True, blank=True)
    size = models.CharField(max_length=40, null=True, blank=True)
    flavor_id = models.CharField(max_length=20)
    image = models.CharField(max_length=80)
    user_id = models.CharField(max_length=25)
    host = models.ForeignKey(Host, null=True, blank=True)
    name = models.CharField(max_length=20, null=True, blank=True)
    command = models.CharField(max_length=200, null=True, blank=True)
    created = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=40, null=True, blank=True)
    ports = models.CharField(max_length=200, null=True, blank=True)
    hostname = models.CharField(max_length=80, null=True, blank=True)

    class Meta:
        app_label = "apphome"
