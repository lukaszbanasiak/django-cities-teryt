# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

import logging
from datetime import datetime
from lxml import etree
from optparse import make_option
from os import path, mkdir

from ...models import Province, County, Municipality, City, Village, District
from ...settings import *

IMPORT_OPT = ('province', 'county', 'municipality', 'city', 'village', 'district')


class Command(BaseCommand):
    args = '[--data ...] [--import] [--flush]'
    help = 'Import/flush TERYT data'

    logger = logging.getLogger("cities_teryt")

    option_list = BaseCommand.option_list + (
        make_option('--data', action='append', default=[],
                    help='Comma separated list of data types.'),
        make_option('--import', action='store_true', default=True,
                    help='Import selected types of data.'),
        make_option('--flush', action='store_true', default=False,
                    help='Flush selected types of data.'),
    )

    def handle(self, *args, **options):
        if not path.exists(IMPORT_DIR):
            self.logger.info('Creating %s' % IMPORT_DIR)
            mkdir(IMPORT_DIR)

        self.terc = normpath(join(IMPORT_DIR, 'TERC.xml'))
        self.simc = normpath(join(IMPORT_DIR, 'SIMC.xml'))

        if not path.isfile(normpath(join(IMPORT_DIR, 'TERC.xml'))):
            raise IOError('File not exist {}'.format(self.terc))
        if not path.isfile(normpath(join(IMPORT_DIR, 'SIMC.xml'))):
            raise IOError('File not exist {}'.format(self.simc))

        data = options['data']

        if 'all' in data:
            data = IMPORT_OPT

        if options.get('flush', False):
            for flush in data:
                func = getattr(self, "flush_" + flush)
                func()

        if options.get('import', False):
            for import_ in data:
                func = getattr(self, "import_" + import_)
                func()

    def _update_or_create(self, model, **kwargs):
        try:
            obj = model.objects.get(id=kwargs['id'], name=kwargs['name'])
            for key, value in kwargs.iteritems():
                if getattr(obj, key) != value:
                    setattr(obj, key, value)
                    self.logger.info(u'Update {obj} with {key}: {value}'.format(obj=obj, key=key, value=value))
            obj.save()
        except model.DoesNotExist:
            obj = model(**kwargs)
            obj.save()

    def import_province(self):
        self.logger.info('Importing province data')
        items = etree.parse(self.terc)
        for item in items.xpath(u'//col[text()="województwo"]/ancestor::row'):
            values = {
                'id': item[0].text,
                'name': item[4].text.lower(),
                'teryt_date': self.__str2date(item[6].text),
            }
            self._update_or_create(Province, **values)

    def import_county(self):
        self.logger.info('Importing county data')
        items = etree.parse(self.terc)
        for item in items.xpath(u'//col[text()[contains(.,"powiat")]]/ancestor::row'):
            values = {
                'id': '%s%s' % (item[0].text, item[1].text),
                'name': item[4].text,
                'teryt_date': self.__str2date(item[6].text),
                'province_id': item[0].text,
            }
            self._update_or_create(County, **values)

    def import_municipality(self):
        self.logger.info('Importing municipality data')
        items = etree.parse(self.terc)
        for item in items.xpath(u'//col[text()[contains(.,"gmina")]]/ancestor::row'):
            values = {
                'id': '%s%s%s' % (item[0].text, item[1].text, item[2].text),
                'name': item[4].text,
                'teryt_date': self.__str2date(item[6].text),
                'province_id': item[0].text,
                'county_id': '%s%s' % (item[0].text, item[1].text),
                'type': item[3].text,
            }
            self._update_or_create(Municipality, **values)

    def import_city(self):
        self.logger.info('Importing city data')
        items = etree.parse(self.simc)
        for item in items.xpath(u'//col[@name="RM"][text()="96"]/ancestor::row'):
            values = {
                'id': '%s' % item[7].text,
                'name': item[6].text,
                'teryt_date': self.__str2date(item[9].text),
                'province_id': item[0].text,
                'county_id': '%s%s' % (item[0].text, item[1].text),
                'municipality_id': '%s%s%s' % (item[0].text, item[1].text, item[2].text),
                'type': item[4].text,
            }
            self._update_or_create(City, **values)

    def import_village(self):
        self.logger.info('Importing village data')
        items = etree.parse(self.simc)
        for item in items.xpath(u'//col[@name="RM"][text()="01"]/ancestor::row'):
            values = {
                'id': '%s' % item[7].text,
                'name': item[6].text,
                'teryt_date': self.__str2date(item[9].text),
                'province_id': item[0].text,
                'county_id': '%s%s' % (item[0].text, item[1].text),
                'municipality_id': '%s%s%s' % (item[0].text, item[1].text, item[2].text),
                'type': item[4].text,
            }
            self._update_or_create(Village, **values)

    def import_district(self):
        self.logger.info('Importing district data')
        items = etree.parse(self.simc)
        for item in items.xpath(u'//col[@name="RM"][text()="99"]/ancestor::row'):
            values = {
                'id': '%s' % item[7].text,
                'name': item[6].text,
                'teryt_date': self.__str2date(item[9].text),
                'province_id': item[0].text,
                'county_id': '%s%s' % (item[0].text, item[1].text),
                'municipality_id': '%s%s%s' % (item[0].text, item[1].text, item[2].text),
            }
            try:
                city = City.objects.get(province=values['province_id'], county=values['county_id'],
                                        municipality=values['municipality_id'])
            except City.DoesNotExist:
                # City with "delegatura"
                city = City.objects.get(province=values['province_id'], county=values['county_id'])
                values.update({'municipality_id': city.municipality_id})
            values.update({'city': city})
            self._update_or_create(District, **values)

    def flush_province(self):
        self.logger.info('Flushing province data')
        Province.objects.all().delete()

    def flush_county(self):
        self.logger.info('Flushing county data')
        County.objects.all().delete()

    def flush_municipality(self):
        self.logger.info('Flushing municipality data')
        Municipality.objects.all().delete()

    def flush_city(self):
        self.logger.info('Flushing city data')
        City.objects.all().delete()

    def flush_village(self):
        self.logger.info('Flushing village data')
        Village.objects.all().delete()

    def __str2date(self, string):
        return datetime.strptime(string, "%Y-%m-%d").date()