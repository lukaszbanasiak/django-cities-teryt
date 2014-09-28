===================
django-cities-teryt
===================

Polish region and city data for Django.

This app provides models, admin integration and commands to import region and city data in your database.

The data is pulled from `TERYT <http://bip.stat.gov.pl/en/teryt/>`_ database
(National Official Register of the Territorial Division of the Country). TERYT is maintained by
Polish Central Statistical Office (`GUS <http://stat.gov.pl/en/>`_)

Database contains:
- provinces
- counties
- municipalities
- villages
- cities
- city districts

Installation
------------

Install django-cities-teryt
.. code:: bash

    $ pip install django-cities-teryt

Or dev version
..code:: bash
    pip install -e git+git@github.com:lukaszbanasiak/django-cities-teryt.git#egg=cities_teryt

Add ``cities_teryt`` to your ``INSTALLED_APPS``.
.. code:: python
    INSTALLED_APPS = (
        ...
        'cities_teryt',
    )

Now, run ``syncdb``, it will only create tables for models:
.. code:: bash

    ./manage.py syncdb

Configuration
-------------

1. Download ``SIMC`` and ``TERC`` xml files from TERYT website http://www.stat.gov.pl/broker/access/prefile/listPreFiles.jspa
 and save them to one directory.
2. Setup in your ``settings.py`` full path to above directory:
.. code:: python
    # Default directory is `import` dir in `django-cities-teryt` app directory
    CITIES_TERYT_IMPORT_DIR = '/path/to/dir'

Importing data
--------------

To populate your database with all TERYT data use command:
.. code:: bash
    ./manage.py cities_teryt --data all --import

To remove data use command:
.. code:: bash
    ./manage.py cities_teryt --data all --flush

To operate on specific type of data enumerate them after ``--data`` argument
.. code:: bash
    ./manage.py cities_teryt --data province, county, municipality --import
    ./manage.py cities_teryt --data city, village, district --flush

Notice
^^^^^^
Data have relations so it's best to import everything.
Data are large and take time to import (there's no progress display).
Verbosity is controlled through LOGGING.

Examples
--------

Get ``City`` by name
.. code:: python
    >>> City.objects.get(name='Swarzędz')
    <City: Swarzędz (0971502)>

To get name of ``Municipality`` of this City we can use ``parent`` method or call directly ``municipality`` attrib
.. code:: python
    >>> City.objects.get(name='Swarzędz').parent
    <Municipality: Swarzędz (302116)>
    >>> City.objects.get(name='Swarzędz').municipality
    <Municipality: Buk (302103)>
    >>> Municipality.objects.get(city__name='Swarzędz')
    <Municipality: Swarzędz (302116)>

In this way we can get also ``Province`` or ``County``
.. code:: python
    >>> City.objects.get(name='Swarzędz').province
    <Province: wielkopolskie (30)>
    >>> Province.objects.get(city__name='Swarzędz')
    <Province: wielkopolskie (30)>

... or even ``Districts``
.. code:: python
    >>> c = City.objects.get(name='Swarzędz')
    >>> c.district_set.all()
    [<District: Nowa Wieś (0971519)>, <District: Zieleniec (0971525)>]
    >>> District.objects.filter(city=c)
    [<District: Nowa Wieś (0971519)>, <District: Zieleniec (0971525)>]

List all ``Cities`` in the same ``County``
.. code:: python
    >>> County.objects.get(city__name='Swarzędz').city_set.all()
    [<City: Buk (0970520)>, <City: Murowana Goślina (0971152)>, <City: Kostrzyn (0970885)>, <City: Mosina (0971057)>, <City: Pobiedziska (0971287)>, <City: Puszczykowo (0971376)>, <City: Kórnik (0970922)>, <City: Swarzędz (0971502)>, <City: Luboń (0970974)>, <City: Stęszew (0971494)>]

Get pretty display name
.. code:: python
    # Village, Municipality, County, Province
    >>> print Village.objects.get(name='Kaczkowo', province__name='wielkopolskie').get_display_name()
    Kaczkowo, Rydzyna, leszczyński, wielkopolskie
    # `Municipality` and `County` for "Poznań" is the same so we got only `City` and `Province` name
    >>> print City.objects.get(name='Poznań').get_display_name()
    Poznań, wielkopolskie

Requirements
------------

See ``requirements.txt``
