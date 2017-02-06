from django.conf import settings
from django.contrib import messages
from django.core.signing import BadSignature, Signer
from django.utils.functional import SimpleLazyObject, empty
from django.utils.translation import ugettext_lazy as _

from oscar.core.loading import get_class, get_model

from .models import FavoriteList

Applicator = get_class('offer.utils', 'Applicator')
Selector = get_class('partner.strategy', 'Selector')

selector = Selector()


class FavoriteListMiddleware(object):

    # Middleware interface methods

    def process_request(self, request):
        # Keep track of cookies that need to be deleted (which can only be done
        # when we're processing the response instance).
        request.cookies_to_delete = []

        # Load stock/price strategy and assign to request (it will later be

        request._favlist_cache = None

        def load_full_favlist():

            favlist = self.get_favlist(request)

            return favlist

        def load_favlist_hash():

            favoritelist = self.get_favlist(request)
            if favoritelist.id:
                return self.get_favlist_hash(favoritelist.id)


        request.favlist = SimpleLazyObject(load_full_favlist)
        request.favlist_hash = SimpleLazyObject(load_favlist_hash)

    def process_response(self, request, response):
        # Delete any surplus cookies
        cookies_to_delete = getattr(request, 'cookies_to_delete', [])
        for cookie_key in cookies_to_delete:
            response.delete_cookie(cookie_key)

        if not hasattr(request, 'favlist'):
            return response

        if (isinstance(request.favlist, SimpleLazyObject)
                and request.favlist._wrapped is empty):
            return response

        cookie_key = self.get_cookie_key(request)

        has_favlist_cookie = (
            cookie_key in request.COOKIES
            and cookie_key not in cookies_to_delete)

        if (request.favlist.id and not request.user.is_authenticated()
                and not has_favlist_cookie):
            cookie = self.get_favlist_hash(request.favlist.id)
            response.set_cookie(
                cookie_key, cookie,
                max_age=settings.OSCAR_BASKET_COOKIE_LIFETIME,
                secure=settings.OSCAR_BASKET_COOKIE_SECURE, httponly=True)
        return response

    def get_cookie_key(self, request):

        return 'favlist'

    def process_template_response(self, request, response):
        if hasattr(response, 'context_data'):
            if response.context_data is None:
                response.context_data = {}
            if 'favlist' not in response.context_data:
                response.context_data['favlist'] = request.favlist
            else:
                response.context_data['favlist'] = request.favlist
        return response

    # Helper methods

    def get_favlist(self, request):

        if request._favlist_cache is not None:
            return request._favlist_cache

        manager = FavoriteList.objects
        cookie_key = self.get_cookie_key(request)
        cookie_favlist = self.get_cookie_favlist(cookie_key, request)

        if hasattr(request, 'user') and request.user.is_authenticated():

            try:
                favlist, __ = manager.get_or_create(owner=request.user)
            except FavoriteList.MultipleObjectsReturned:

                old_favlists = list(manager.filter(owner=request.user))
                favlist = old_favlists[0]


            favlist.owner = request.user

            if cookie_favlist:
                request.cookies_to_delete.append(cookie_key)

        elif cookie_favlist:

            favlist = cookie_favlist
        else:
            favlist = FavoriteList()
            favlist.save()


        request._favlist_cache = favlist

        return favlist

    def get_cookie_favlist(self, cookie_key, request):

        favlist = None
        if cookie_key in request.COOKIES:
            favlist_hash = request.COOKIES[cookie_key]
            try:
                favlist_id = Signer().unsign(favlist_hash)
                favlist = FavoriteList.objects.get(pk=favlist_id, owner=None)

            except (BadSignature, FavoriteList.DoesNotExist):
                request.cookies_to_delete.append(cookie_key)
        return favlist

    def get_favlist_hash(self, favlist_id):
        return Signer().sign(favlist_id)
