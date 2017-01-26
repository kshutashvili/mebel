import zlib
from oscar.apps.basket.abstract_models import AbstractBasket, AbstractLine


class Basket(AbstractBasket):
    def add_product(self, product, quantity=1, options=None, multi_options=None):
        """
                Add a product to the basket

                'stock_info' is the price and availability data returned from
                a partner strategy class.

                The 'options' list should contains dicts with keys 'option' and 'value'
                which link the relevant product.Option model and string value
                respectively.

                Returns (line, created).
                  line: the matching basket line
                  created: whether the line was created or updated

                """
        if options is None:
            options = []
        if not self.id:
            self.save()

        if multi_options is None:
            multi_options = []
        if not self.id:
            self.save()

        # Ensure that all lines are the same currency
        price_currency = self.currency
        stock_info = self.strategy.fetch_for_product(product)
        if price_currency and stock_info.price.currency != price_currency:
            raise ValueError((
                                 "Basket lines must all have the same currency. Proposed "
                                 "line has currency %s, while basket has currency %s")
                             % (stock_info.price.currency, price_currency))

        if stock_info.stockrecord is None:
            raise ValueError((
                                 "Basket lines must all have stock records. Strategy hasn't "
                                 "found any stock record for product %s") % product)

        # Line reference is used to distinguish between variations of the same
        # product (eg T-shirts with different personalisations)
        line_ref = self._create_line_reference(
            product, stock_info.stockrecord, options, multi_options)

        # Determine price to store (if one exists).  It is only stored for
        # audit and sometimes caching.
        defaults = {
            'quantity': quantity,
            'price_excl_tax': stock_info.price.excl_tax,
            'price_currency': stock_info.price.currency,
        }
        if stock_info.price.is_tax_known:
            defaults['price_incl_tax'] = stock_info.price.incl_tax

        line, created = self.lines.get_or_create(
            line_reference=line_ref,
            product=product,
            stockrecord=stock_info.stockrecord,
            defaults=defaults)
        if created:
            print(multi_options)
            print(options)
            for option_dict in options:
                line.attributes.create(
                    option=option_dict['option'],
                    value=option_dict['value']
                )

            for moption_dict in multi_options:
                line.options_choices.create(
                    variant=moption_dict['value']
                )
                print(moption_dict['value'])

        else:
            line.quantity = max(0, line.quantity + quantity)
            line.save()
        self.reset_offer_applications()

        # Returning the line is useful when overriding this method.
        return line, created

    def _create_line_reference(self, product, stockrecord, options, multi_options):
        """
        Returns a reference string for a line based on the item
        and its options.
        """
        base = '%s_%s' % (product.id, stockrecord.id)
        if not options and not multi_options:
            return base
        repr_options_1 = [{'option': repr(option['option']),
                         'value': repr(option['value'])} for option in options]

        repr_options_2 = [{'option': repr(option['multi_option']),
                           'value': repr(option['value'])} for option in multi_options]
        repr_options = repr_options_1 + repr_options_2
        return "%s_%s" % (base, zlib.crc32(repr(repr_options).encode('utf8')))


class Line(AbstractLine):
    def get_preview_info(self):
        return 'X'.join([var.variant.variant.name for var in self.options_choices.all() if var.variant.variant.group.preview])

    @property
    def additional_price(self):
        if self.options_choices.all():
            add_price = [choices.variant.additional_price for choices in self.options_choices.all()]
            return sum(add_price)

    @property
    def unit_tax(self):
        return super(Line, self).unit_tax + self.additional_price

    @property
    def unit_price_incl_tax(self):
        return super(Line, self).unit_price_incl_tax + self.additional_price

    @property
    def unit_price_excl_tax(self):
        return super(Line, self).unit_price_excl_tax + self.additional_price


from oscar.apps.basket.models import *  # noqa

