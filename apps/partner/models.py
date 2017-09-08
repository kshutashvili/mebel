# -*-coding:utf8-*-

from oscar.apps.partner.abstract_models import AbstractStockRecord, AbstractPartner


class StockRecord(AbstractStockRecord):
    @property
    def price_with_discount(self):
        excl_tax = self.price_excl_tax
        if not self.product.discount_type:
            return excl_tax
        if self.product.discount_type == 1:
            return excl_tax - self.product.discount_value
        return excl_tax - excl_tax * self.product.discount_value / 100


class Partner(AbstractPartner):
    pass
