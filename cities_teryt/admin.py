from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import *


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('id', 'name', 'slug',)
    ordering = ('name',)
    readonly_fields = ('created', 'modified')


class CountyAdmin(admin.ModelAdmin):
    list_display = ('name', 'province')
    list_filter = ('province',)
    search_fields = ('id', 'name', 'slug', 'province__name')
    ordering = ('name',)


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_type', 'county', 'province')
    list_filter = ('type', 'province',)
    search_fields = ('id', 'name', 'slug', 'county__name', 'province__name')
    ordering = ('name',)

    def get_type(self, obj):
        return obj.get_type_display()
    get_type.short_description = _('Type')
    get_type.admin_order_field = 'get_type_display'


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_type', 'municipality', 'county', 'province')
    list_filter = ('type', 'province',)
    search_fields = ('id', 'name', 'slug', 'municipality__name', 'county__name', 'province__name')
    ordering = ('name',)

    def get_type(self, obj):
        return obj.get_type_display()
    get_type.short_description = _('Type')
    get_type.admin_order_field = 'get_type_display'


class PlaceChildBaseAdmin(PlaceAdmin):
    list_display = ('name', 'municipality', 'county', 'province')
    list_filter = ('province',)


class CityAdmin(PlaceChildBaseAdmin):
    pass


class VillageAdmin(PlaceChildBaseAdmin):
    pass


class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'city',)
    list_filter = ('province',)
    search_fields = ('id', 'name', 'slug', 'city__name',)
    ordering = ('city', 'name',)


admin.site.register(Province, ProvinceAdmin)
admin.site.register(County, CountyAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Village, VillageAdmin)
admin.site.register(District, DistrictAdmin)
