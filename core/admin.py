from django.contrib import admin
from django.utils.html import format_html

from .models import (
    CompanyInfo, PhoneNumber, ServiceCategory, GalleryImage,
    Partner, ContactMessage, HeroSlide, Stat, Brand,
)

admin.site.site_header = 'Tryvis Investments — site manager'
admin.site.site_title = 'Tryvis Investments'
admin.site.index_title = 'Manage the website content'


class PhoneNumberInline(admin.TabularInline):
    model = PhoneNumber
    extra = 1


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'tin')
    inlines = [PhoneNumberInline]
    fieldsets = (
        ('Identity', {'fields': ('name', 'tagline', 'logo')}),
        ('About', {'fields': ('about', 'vision', 'mission', 'values')}),
        ('Contact', {'fields': ('address_line', 'po_box', 'email', 'whatsapp_number')}),
        ('Registration', {'fields': ('tin', 'brela_reg_no', 'business_license_no')}),
    )


@admin.register(HeroSlide)
class HeroSlideAdmin(admin.ModelAdmin):
    list_display = ('preview', '__str__', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    list_display_links = ('__str__',)

    @admin.display(description='Image')
    def preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:44px;border-radius:2px">', obj.image.url)
        return '—'


@admin.register(Stat)
class StatAdmin(admin.ModelAdmin):
    list_display = ('value', 'label', 'order')
    list_editable = ('order',)


@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'kind', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    list_filter = ('kind',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('preview', 'name', 'order')
    list_editable = ('order',)
    list_display_links = ('name',)

    @admin.display(description='Logo')
    def preview(self, obj):
        if obj.logo:
            return format_html('<img src="{}" style="height:32px;border-radius:2px">', obj.logo.url)
        return '—'


@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'order')
    list_editable = ('order',)
    list_filter = ('category',)


@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'company_name', 'phone', 'email', 'created_at', 'is_read')
    list_editable = ('is_read',)
    list_filter = ('is_read',)
    readonly_fields = ('name', 'company_name', 'phone', 'email', 'message', 'created_at')
