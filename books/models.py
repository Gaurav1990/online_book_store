from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
# Create your models here.

AVAILABLE_TYPES=(
    ('undefined','undefined'),
    ('philosophy','philosophy'),
    ('patriotic','patriotic'),
    ('gk','gk'),
    ('engineering','engineering'),
    ('cartoon','cartoon'),
    ('romantic','romantic'),
    ('historical','historical')
)


class Books(models.Model):
    name = models.CharField(max_length=200, blank=False, null=False)
    isbn = models.CharField(max_length=1000, blank=False, null=False, verbose_name="International Standard Book Number")
    type = models.CharField('type', max_length=50, choices=AVAILABLE_TYPES, default='undefined')
    description = models.CharField(max_length=1000, blank=False, null=False)
    author_name = models.CharField(max_length=200, blank=False, null=False)
    release_date = models.DateTimeField(default=datetime.now, blank=True)
    signed = models.BooleanField(default=False)
    price = models.IntegerField(blank=False, null=False)

    def __unicode__(self):
        return "%s" % (self.name)

