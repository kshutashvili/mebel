# -*-coding: utf8-*-

from __future__ import unicode_literals

from django.db import models

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import pgettext_lazy

from oscar.core.compat import AUTH_USER_MODEL


@python_2_unicode_compatible
class SiteReview(models.Model):

    # Scores are between 0 and 5
    SCORE_CHOICES = tuple([(x, x) for x in range(0, 6)])
    score = models.SmallIntegerField(_("Score"), choices=SCORE_CHOICES)


    body = models.TextField(_("Body"))

    # User information.
    user = models.ForeignKey(
        AUTH_USER_MODEL, related_name='site_reviews', null=True, blank=True)

    # Fields to be completed if user is anonymous
    name = models.CharField(
        pgettext_lazy(u"Anonymous reviewer name", u"Name"),
        max_length=255, blank=True)
    email = models.EmailField(_("Email"), blank=True)

    FOR_MODERATION, APPROVED, REJECTED = 0, 1, 2
    STATUS_CHOICES = (
        (FOR_MODERATION, _("Requires moderation")),
        (APPROVED, _("Approved")),
        (REJECTED, _("Rejected")),
    )
    default_status = APPROVED
    if settings.OSCAR_MODERATE_REVIEWS:
        default_status = FOR_MODERATION
    status = models.SmallIntegerField(
        _("Status"), choices=STATUS_CHOICES, default=default_status)

    # Denormalised vote totals
    total_votes = models.IntegerField(
        _("Total Votes"), default=0)  # upvotes + down votes
    delta_votes = models.IntegerField(
        _("Delta Votes"), default=0, db_index=True)  # upvotes - down votes

    date_created = models.DateTimeField(auto_now_add=True)


    class Meta:

        ordering = ['-date_created', 'id']
        unique_together = (('user', ),)
        verbose_name = u'Отзыв'
        verbose_name_plural = u'Отзывы про сайт'

    def __str__(self):
        return self.body

    def clean(self):
        self.body = self.body.strip()
        if not self.user and not (self.name and self.email):
            raise ValidationError(
                _("Anonymous reviews must include a name and an email"))

    # Properties

    @property
    def is_anonymous(self):
        return self.user is None

    @property
    def pending_moderation(self):
        return self.status == self.FOR_MODERATION

    @property
    def is_approved(self):
        return self.status == self.APPROVED

    @property
    def is_rejected(self):
        return self.status == self.REJECTED


    @property
    def reviewer_name(self):
        if self.user:
            name = self.user.username
            return name if name else _('anonymous')
        else:
            return self.name