from django.contrib import admin

from .models import SiteReview
# Register your models here.

@admin.register(SiteReview)
class SiteReviewAdmin(admin.ModelAdmin):
    list_display = ('reviewer_name', 'date_created', 'status')
