# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug import AutoSlugField

try:
    # problem with "ł" char in slug
    from unidecode import unidecode
except ImportError:
    raise ImportError('Required Unidecode for proper diacritics encode.')

__all__ = ['Province', 'County', 'Municipality', 'Place', 'City', 'Village', 'District', ]


class Base(models.Model):
    """
    Base model for all models
    """
    id = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(_('Name'), max_length=200, db_index=True)
    slug = AutoSlugField(populate_from='name', always_update=True, db_index=True)
    teryt_date = models.DateField(_('TERYT date'))
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    modified = models.DateTimeField(_('Modified'), auto_now=True)

    class Meta:
        abstract = True
        ordering = ('name',)
        unique_together = ('id', 'name')

    def __unicode__(self):
        return u'{name} ({id})'.format(name=self.name, id=self.id)

    def get_display_name(self):
        name = self.name
        parent = self.parent.get_display_name()
        if name in parent:
            return u'{parent}'.format(parent=parent)
        return u'{name}, {parent}'.format(name=name, parent=parent)


class Province(Base):
    """
    Province (Województwo) model.
    """
    class Meta:
        verbose_name = _('province')
        verbose_name_plural = _('provinces')

    @property
    def parent(self):
        return None

    def get_display_name(self):
        return u'{}'.format(self.name)


class County(Base):
    """
    County (Powiat) model.
    """
    province = models.ForeignKey(Province, verbose_name=_('Province'))

    class Meta:
        verbose_name = _('county')
        verbose_name_plural = _('counties')

    @property
    def parent(self):
        return self.province


class Municipality(Base):
    """
    Municipality (Gmina) model.
    """
    MUNICIPALITY_TYPE_CHOICES = (
        ('1', 'gmina miejska'),
        ('2', 'gmina wiejska'),
        ('3', 'gmina miejsko-wiejska'),
    )
    province = models.ForeignKey(Province, verbose_name=_('Province'))
    county = models.ForeignKey(County, verbose_name=_('County'))
    type = models.CharField(_('Type'), max_length=1, choices=MUNICIPALITY_TYPE_CHOICES)

    class Meta:
        verbose_name = _('municipality')
        verbose_name_plural = _('municipalities')

    @property
    def parent(self):
        return self.county


class Place(Base):
    """
    Place (Miejscowość) model.

    Base model for places.
    """
    CITY = '96'
    VILLAGE = '01'
    PLACE_TYPE_CHOICES = (
        (CITY, _('city')),
        (VILLAGE, _('village')),
    )
    province = models.ForeignKey(Province, verbose_name=_('Province'))
    county = models.ForeignKey(County, verbose_name=_('County'))
    municipality = models.ForeignKey(Municipality, verbose_name=_('Municipality'))
    type = models.CharField(_('Type'), max_length=2, choices=PLACE_TYPE_CHOICES)

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')

    @property
    def parent(self):
        return self.municipality


class CityManager(models.Manager):
    def get_query_set(self):
        return super(CityManager, self).get_query_set().filter(type='96')


class City(Place):
    """
    City (Miasto) model.
    """
    objects = CityManager()

    class Meta:
        proxy = True
        verbose_name = _('city')
        verbose_name_plural = _('cities')


class VillageManager(models.Manager):
    def get_query_set(self):
        return super(VillageManager, self).get_query_set().filter(type='01')


class Village(Place):
    """
    Village (Wieś) model.
    """
    objects = VillageManager()

    class Meta:
        proxy = True
        verbose_name = _('village')
        verbose_name_plural = _('villages')

# Workaround to reset fields after the proxy classes are defined to use RelatedManager (city_set and village_set)
City.add_to_class('province', models.ForeignKey(Province, verbose_name=_('Province')))
City.add_to_class('county', models.ForeignKey(County, verbose_name=_('County')))
City.add_to_class('municipality', models.ForeignKey(Municipality, verbose_name=_('Municipality')))
Village.add_to_class('province', models.ForeignKey(Province, verbose_name=_('Province')))
Village.add_to_class('county', models.ForeignKey(County, verbose_name=_('County')))
Village.add_to_class('municipality', models.ForeignKey(Municipality, verbose_name=_('Municipality')))


class District(Base):
    """
    District (Dzielnica) model.
    """
    province = models.ForeignKey(Province, verbose_name=_('Province'))
    county = models.ForeignKey(County, verbose_name=_('County'))
    municipality = models.ForeignKey(Municipality, verbose_name=_('Municipality'))
    city = models.ForeignKey(City, verbose_name=_('City'))

    class Meta:
        verbose_name = _('district')
        verbose_name_plural = _('districts')

    @property
    def parent(self):
        return self.city
