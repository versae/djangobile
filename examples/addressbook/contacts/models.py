from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _


class Contact(models.Model):
    nick = models.CharField(_('Nick'), max_length=250)
    first_name = models.CharField(_('First name'), max_length=250, blank=True,
                                  null=True)
    last_name = models.CharField(_('Last name'), max_length=250, blank=True,
                                 null=True)
    birthdate = models.DateField(blank=True, null=True)
    GENDER_TYPES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )
    gender = models.CharField(_('Gender'), max_length=1, choices=GENDER_TYPES,
                              blank=True, null=True)
    notes = models.TextField(_('Notes'), blank=True, null=True)

    user = models.ForeignKey(User, verbose_name=_('user'), blank=True,
                             null=True)

