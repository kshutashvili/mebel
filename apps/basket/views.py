from oscar.apps.basket.views import *
from oscar.apps.basket.views import BasketAddView as CoreBasketAddView

from  django.views.generic import FormView

class BasketAddView(CoreBasketAddView):
    def form_valid(self, form):
        offers_before = self.request.basket.applied_offers()
        print(form.cleaned_data['quantity'])
        print('Forma Valid')
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
