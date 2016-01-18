from __future__ import unicode_literals

from django.utils.encoding import python_2_unicode_compatible
from django.db import models

# used the following link to verify my model (told me about managed and max_length size):
# https://docs.djangoproject.com/en/1.9/howto/legacy-databases/
# can try later:
#   * Make sure each model has one field with primary_key=True
# tried without declaring "id" field, then declared it. same problem with both: cannot see fields other than id.

@python_2_unicode_compatible
class ItemSale(models.Model):
    id = models.IntegerField(primary_key=True) # id (int): unique id for an item, created by Postgres
    title = models.CharField(max_length=120, help_text='Title of the item (e.g. Xbox One)'),
    list_price = models.IntegerField(help_text='The price at which the item was listed'),
    sell_price = models.IntegerField(help_text='The price at which the item was sold'),
    city = models.CharField(max_length=120, help_text='The city in which the item was listed'),
    cashless = models.BooleanField(help_text='The seller will accept a credit card payment'),

    class Meta:
        managed = False
        db_table = 'itemPrices_itemsale'

    def __str__(self):
        return '%d %s' % (self.id, self.title)
