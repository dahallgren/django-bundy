# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils import timezone
from datetime import datetime, date, time


class Workday(models.Model):
    date = models.DateField(unique=True, blank=False, db_index=True, primary_key=True)
    intime = models.TimeField(blank=False)
    outtime = models.TimeField(blank=True, null=True)
    total = models.DurationField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.outtime:
            t = timezone.now()
            self.outtime = time(t.hour, t.minute, t.second)

        self.total = datetime.combine(date.today(), self.outtime) - datetime.combine(date.today(), self.intime)
        super(Workday, self).save(*args, **kwargs)