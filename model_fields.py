# coding: utf-8

from django.db import models
from django.core.exceptions import ValidationError

try:
    from IPy import IP
    from decimal import Decimal

    IP.__long__ = IP.int
except Exception as e:
    print 'Install IPy tools!'


class IntIPAddressField(models.Field):
    __metaclass__ = models.SubfieldBase

    description = "IP address in the form of an decimal"

    empty_strings_allowed = False
    default_error_messages = {
        'invalid': 'Please enter a valid IP Address (x.x.x.x) or (x:x:x:x:x:x:x:x)',
    }

    def db_type(self, connection):
        return 'decimal(39, 0)'

    def get_internal_type(self):
        return 'DecimalField'

    def to_python(self, value):
        if not value:
            value = 0
        elif isinstance(value, basestring):
            return value
        elif isinstance(value, Decimal):
            value = long(value)
        elif isinstance(value, int) or isinstance(value, long):
            value = long(value)
        else:
            assert False, 'Error, revert ip adress'

        try:
            return IP(value).strCompressed()
        except Exception as e:
            print 'Error, revert ip adress'
            raise ValidationError(e)

    def get_db_prep_lookup(self, lookup_type, value, connection, prepared=False):
        try:
            if lookup_type in ('range', 'in'):
                return [self.get_db_prep_value(v) for v in value]

            return [self.get_db_prep_value(value)]
        except ValidationError:
            return super(DecimalField, self).get_db_prep_lookup(lookup_type, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        try:
            if not value:
                return 0
            elif isinstance(value, str):
                return IP(value).int()
            elif isinstance(value, int) or isinstance(value, long) or isinstance(value, Decimal):
                return value
        except TypeError:
            return None
