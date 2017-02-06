# -*-coding:utf8-*-

import hashlib
import random

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import six
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from oscar.core.compat import AUTH_USER_MODEL


class FavoriteList(models.Model):
    """
    Represents a user's wish lists of products.

    A user can have multiple wish lists, move products between them, etc.
    """

    # Only authenticated users can have wishlists
    owner = models.ForeignKey(AUTH_USER_MODEL, related_name='favoritelists',
                              verbose_name=_('Owner'), blank=True, null=True )
    name = models.CharField(verbose_name=_('Name'), default=_('Default'),
                            max_length=255)

    #: This key acts as primary key and is used instead of an int to make it
    #: harder to guess
    key = models.CharField(_('Key'), max_length=6, db_index=True, unique=True,
                           editable=False)

    date_created = models.DateTimeField(
        _('Date created'), auto_now_add=True, editable=False)

    def __unicode__(self):
        return u"%s's Favorute List '%s'" % (self.owner, self.name)

    def save(self, *args, **kwargs):
        if not self.pk or kwargs.get('force_insert', False):
            self.key = self.__class__.random_key()
        super(FavoriteList, self).save(*args, **kwargs)

    @classmethod
    def random_key(cls, length=6):
        """
        Get a unique random generated key based on SHA-1 and owner
        """
        while True:
            rand = six.text_type(random.random()).encode('utf8')
            key = hashlib.sha1(rand).hexdigest()[:length]
            if not cls._default_manager.filter(key=key).exists():
                return key

    def is_allowed_to_edit(self, user):
        # currently only the owner can edit their wish list
        return user == self.owner

    class Meta:
        ordering = ('date_created', )
        verbose_name = u'Список желаемого'
        verbose_name_plural = u'Списки желаемого'

    def get_absolute_url(self):
        return reverse('customer:wishlists-detail', kwargs={
            'key': self.key})

    def add(self, product):
        """
        Add a product to this wishlist
        """
        lines = self.lines.filter(product=product)
        if len(lines) == 0:
            self.lines.create(
                product=product, title=product.get_title())
        else:
            line = lines[0]
            line.quantity += 1
            line.save()

    def remove(self, product):
        """
         Remove product from this favlist
        """
        lines = self.lines.filter(product=product)
        if not len(lines) == 0:
            line = lines[0]
            line.delete()

    def exist(self, product):
        lines = self.lines.filter(product=product)
        if len(lines) == 0:
            return False
        else:
            return True

class FavoriteListLine(models.Model):
    """
    One entry in a wish list. Similar to order lines or basket lines.
    """
    favlist = models.ForeignKey(FavoriteList, related_name='lines',
                                 verbose_name=u'Список желаемого')
    product = models.ForeignKey(
        'catalogue.Product', verbose_name=_('Product'),
        related_name='favlist_lines', on_delete=models.SET_NULL,
        blank=True, null=True)
    quantity = models.PositiveIntegerField(_('Quantity'), default=1)
    #: Store the title in case product gets deleted
    title = models.CharField(
        pgettext_lazy(u"Product title", u"Title"), max_length=255)

    def __str__(self):
        return u'%sx %s on %s' % (self.quantity, self.title,
                                  self.wishlist.name)

    def get_title(self):
        if self.product:
            return self.product.get_title()
        else:
            return self.title

    class Meta:
        ordering = ['pk']
        unique_together = (('favlist', 'product'), )
        verbose_name = _('Wish list line')
