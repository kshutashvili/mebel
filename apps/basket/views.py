from oscar.apps.basket.views import *
from oscar.apps.basket.views import BasketAddView as CoreBasketAddView, BasketView as CoreBasketView


from apps.order.forms import SimpleOrderForm


class BasketView(CoreBasketView):

    def get_context_data(self, **kwargs):
        ctx = super(BasketView, self).get_context_data(**kwargs)

        ctx['order_form'] = SimpleOrderForm()

        return ctx



class BasketAddView(CoreBasketAddView):
    def form_valid(self, form):
        offers_before = self.request.basket.applied_offers()
        self.request.basket.add_product(
            form.product, form.cleaned_data['quantity'],
            form.cleaned_options(), form.cleaned_multiple_options())
        messages.success(self.request, self.get_success_message(form),
                         extra_tags='safe noicon')
        # Check for additional offer messages
        BasketMessageGenerator().apply_messages(self.request, offers_before)
        # Send signal for basket addition
        self.add_signal.send(
            sender=self, product=form.product, user=self.request.user,
            request=self.request)
        return super(CoreBasketAddView, self).form_valid(form)
