from django.shortcuts import render, get_list_or_404, redirect, get_object_or_404
from django.views import generic, View
from staff.models import FactoryPrice, Factory
from .models import Product, Payment, Transaction
from . import forms as custForm
from django.contrib import messages


class HomePageView(View):
    def get(self, request):
        top_factory = FactoryPrice.objects.all()[:10]
        context = {
            "factories": top_factory
        }

        return render(request, 'farmer/home.html', context)


class FactoryList(generic.ListView):
    model = FactoryPrice
    context_object_name = 'factories'
    template_name = 'farmer/factory_list.html'


class CreateCollectionScheduler(View):
    form = custForm.CreateProduceForm
    template_name = 'farmer/product_create_form.html'

    def get(self, request):
        return render(request, self.template_name, context={'form': self.form()})

    def post(self, request):
        form = self.form(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            factory = product.factory
            factory_price = get_object_or_404(
                FactoryPrice, factory_id=factory.pk)
            product.price_per_kg = factory_price.price
            product.save()
            messages.success(
                request, 'Your request was send successfully wait for processing')
            return redirect('farmer:schedules')
        return render(request, self.template_name, context={'form': form})


class ScheduleList(generic.ListView):
    model = Product


class PendingPayment(View):
    template_name = 'farmer/payment_list.html'

    def get(self, request):
        pending = []
        for payment in Payment.objects.all():
            if payment.product.farmer == request.user:
                pend = payment.total_amount - payment.paid_amount
                if pend > 0:
                    payment.balance = pend
                    pending.append(payment)
        return render(request, self.template_name, context={'payments': pending})


class PaymentHistory(View):
    context_object_name = "transactions"

    def get(self, request):
        trans = list()
        user = self.request.user
        transactions = Transaction.objects.all()
        for transaction in transactions:
            farmer = transaction.product.farmer
            if farmer.id == user.id:
                trans.append(transaction)
        return render(request, 'farmer/transaction_list.html', context={
            "transactions": trans
        })
