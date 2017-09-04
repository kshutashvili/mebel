# -*- coding: utf-8 -*-
from sorl.thumbnail import get_thumbnail


def get_admin_thumb(field, size, crop='center'):
    if field:
        thumb = get_thumbnail(field, size, crop=crop, upscale=False, quality=85)
        return '<img src="{}" />'.format(thumb.url)
