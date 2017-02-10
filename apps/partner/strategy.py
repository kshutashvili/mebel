from oscar.apps.partner.strategy import *

class Selector(object):
    """
    Responsible for returning the appropriate strategy class for a given
    user/session.

    This can be called in three ways:

    #) Passing a request and user.  This is for determining
       prices/availability for a normal user browsing the site.

    #) Passing just the user.  This is for offline processes that don't
       have a request instance but do know which user to determine prices for.

    #) Passing nothing.  This is for offline processes that don't
       correspond to a specific user.  Eg, determining a price to store in
       a search index.

    """

    def strategy(self, request=None, user=None, **kwargs):
        """
        Return an instanticated strategy instance
        """
        # Default to the backwards-compatible strategy of picking the first
        # stockrecord but charging zero tax.
        return Default(request)


class FixedPrice(Base):
    """
    This should be used for when the price of a product is known in advance.

    It can work for when tax isn't known (like in the US).

    Note that this price class uses the tax-exclusive price for offers, even if
    the tax is known.  This may not be what you want.  Use the
    TaxInclusiveFixedPrice class if you want offers to use tax-inclusive
    prices.
    """
    exists = True

    def __init__(self, currency, excl_tax, tax=None, old_tax=None):
        self.currency = currency
        self.excl_tax = excl_tax
        self.tax = tax
        self.old_tax = old_tax

    @property
    def incl_tax(self):
        if self.is_tax_known:
            return self.excl_tax + self.tax
        raise prices.TaxNotKnown(
            "Can't calculate price.incl_tax as tax isn't known")

    @property
    def is_tax_known(self):
        return self.tax is not None


class NoTax(object):
    """
    Pricing policy mixin for use with the ``Structured`` base strategy.
    This mixin specifies zero tax and uses the ``price_excl_tax`` from the
    stockrecord.
    """

    def pricing_policy(self, product, stockrecord):
        # Check stockrecord has the appropriate data
        if not stockrecord or stockrecord.price_excl_tax is None:
            return prices.Unavailable()

        excl_tax = stockrecord.price_excl_tax
        old_tax = None
        if product.is_discountable:
            if product.discount_type == 1:
                excl_tax = excl_tax - product.discount_value
            elif product.discount_type == 2:
                excl_tax =excl_tax - excl_tax*product.discount_value/100
            old_tax = stockrecord.price_excl_tax

        return prices.FixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=excl_tax,
            tax=D('0.00'))

    def parent_pricing_policy(self, product, children_stock):
        stockrecords = [x[1] for x in children_stock if x[1] is not None]
        if not stockrecords:
            return prices.Unavailable()
        # We take price from first record
        stockrecord = stockrecords[0]
        return prices.FixedPrice(
            currency=stockrecord.price_currency,
            excl_tax=stockrecord.price_excl_tax,
            tax=D('0.00'))


class Default(UseFirstStockRecord, StockRequired, NoTax, Structured):
    pass