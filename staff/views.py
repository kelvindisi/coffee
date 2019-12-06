from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.views import generic, View
from .models import Factory, FactoryStaff, FactoryPrice
from farmer.models import Product, Payment, Transaction
from . import forms as custForm
from account.models import UserModel
from django.http import HttpResponse
from django.contrib import messages
from account.forms import UpdateUserForm, ProfileForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class HomeView(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"

    def test_func(self):
        userlevel = self.request.user.userlevel

        if userlevel == 'accounts' or userlevel == 'factory_admin' or userlevel == 'manager':
            return True

    def get(self, request):
        return render(request, 'staff/index.html')


# create new factory
class CreateFactoryView(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"

    factoryForm = custForm.FactoryForm
    factoryPrice = custForm.CreateFactoryPriceForm
    template_name = 'manager/add_factory_form.html'

    def test_func(self):
        return self.request.user.userlevel == "manager"
    
    def get(self, request):
        context={
            'factory_price': self.factoryPrice(),
            'factory': self.factoryForm(),
        }
        return render(request, self.template_name, context)
    
    def post(self, request, *args, **kwargs):
        factory = self.factoryForm(request.POST)
        factory_price = self.factoryPrice(request.POST)
        
        context = {
            'factory_price': factory_price,
            'factory': factory
        }

        if factory.is_valid() and factory_price.is_valid():
            fact = factory.save()
            price = factory_price.save(commit=False)
            price.factory_id = fact.id
            price.save()

            return redirect('staff:factories')

        return render(request, self.template_name, context)


# List of all factories
class FactoryListView(LoginRequiredMixin, UserPassesTestMixin,generic.ListView):
    login_url = "/account/"
    
    template_name = 'manager/factory_list.html'
    model = Factory
    context_object_name = 'factories'

    def test_func(self):
        return self.request.user.userlevel == "manager"


class FactoryUpdateView(LoginRequiredMixin, UserPassesTestMixin,generic.UpdateView):
    login_url = "/account/"
    
    template_name = 'manager/factory_update_form.html'
    fields = ['name', 'email', 'phone_number', 'address']
    model = Factory

    def test_func(self):
        return self.request.user.userlevel == "manager"


class FactoryDeleteView(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template_name = 'manager/confirm_factory_delete.html'

    def test_func(self):
        return self.request.user.userlevel == "manager"
    
    def get(self, request, id):
        factory = get_object_or_404(Factory, pk=id)
        return render(request, self.template_name, context={'factory': factory})

    def post(self, request, id):
        factory = get_object_or_404(Factory, pk=id)
        factory.delete()
        return redirect('staff:factories')


"""
****************************************************************
            SUPER ADMIN PREVILEDGES
****************************************************************
"""
# Add new factory admin
class CreateFactoryAdmin(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    userForm = custForm.CreateUserForm
    template_name = 'manager/factory_admin_form.html'

    def test_func(self):
        return self.request.user.userlevel == "manager"

    def get(self, request):
        context = {
            'form': self.userForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.userForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('id_number')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            factory_id = form.cleaned_data.get('factories')

            user = UserModel.objects.create_user(id_number, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.userlevel = 'factory_admin'
            user.save()

            fact = get_object_or_404(Factory, pk=factory_id)

            factory_staff = FactoryStaff(staff=user, factory=fact)
            factory_staff.save()

            return redirect('staff:factory_admins_list')
        return render(request, self.template_name, context={'form': form})


#delete factory admin
class DeleteFactoryStaff(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    def test_func(self):
        return self.request.user.userlevel == "manager"

    def get(self, request, pk):
        staff = get_object_or_404(UserModel, pk=pk)
        return render(request, 'manager/confirm_factory_admin_delete.html', context={'staff': staff})

    def post(self, request, pk):
        staff_id = request.POST.get('user_id')
        try:
            staff_table = FactoryStaff.objects.get(staff=staff_id).first()
            staff_table.delete()
        except:
            pass
        staff = get_object_or_404(UserModel, pk=staff_id)
        staff.userlevel = None
        staff.save()
        messages.info(request, 'Staff access removed successfully')
        return redirect('staff:factory_admins_list')


class EditFactoryStaff(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template_name = 'manager/fact_admin_edit_form.html'
    form = custForm.UpdateUserForm

    def test_func(self):
        return self.request.user.userlevel == "manager"

    def get(self, request, pk):
        staff = get_object_or_404(UserModel, pk=pk)
        staff.factories = staff.factorystaff.factory.pk

        context = {
            'form': self.form(instance=staff)
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request, pk):
        user = get_object_or_404(UserModel, pk=pk)
        user.factories = user.factorystaff.factory.pk

        form = self.form(request.POST, instance=user)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.id_number
            user.save()

            factory = get_object_or_404(Factory, pk=request.POST.get('factories'))
            factory_staff = get_object_or_404(FactoryStaff, staff=user)
            factory_staff.factory = factory
            factory_staff.save()

            messages.success(request, 'Staff details updated successfully')
            return redirect('staff:factory_admins_list')

        return render(request, self.template_name, context={'form':form})

            

# Factory Admin List
class FactoryAdminList(LoginRequiredMixin, UserPassesTestMixin,generic.ListView):
    login_url = "/account/"
    
    context_object_name = 'factory_admins'
    template_name = 'manager/factory_admin_list.html'

    def test_func(self):
        return self.request.user.userlevel == "manager"

    def get_queryset(self):
        try:
            return list(UserModel.objects.filter(userlevel='factory_admin'))
        except:
            return []


"""
****************************************************************
                        FACTORY ADMIN
****************************************************************
"""

class RejectProduct(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    def test_func(self):
        return self.request.user.userlevel == "factory_admin"
    
    def get(self, request):
        return redirect('factory_admin:products_schedule')
    
    def post(self, request):
        factory_id = request.user.factorystaff.factory.id
        product = get_object_or_404(Product, factory=factory_id, scheduled='2', pk=request.POST.get('product_id'))
        product.scheduled = '0'
        product.save()
        return redirect('factory_admin:products_schedule')


class ReRejectProduct(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    def test_func(self):
        return self.request.user.userlevel == "factory_admin"
    
    def get(self, request):
        return redirect('factory_admin:products_schedule')
    
    def post(self, request):
        factory_id = request.user.factorystaff.factory.id
        product = get_object_or_404(Product, factory=factory_id, scheduled='1', pk=request.POST.get('product_id'))
        product.scheduled = '0'
        product.date_scheduled = None
        product.save()
        return redirect('factory_admin:scheduled')


#posted product to schedule collection
class NewProduct(LoginRequiredMixin, UserPassesTestMixin,generic.ListView):
    login_url = "/account/"
    
    template_name = 'factory_admin/collection_list.html'
    model = Product

    def test_func(self):
        return self.request.user.userlevel == "factory_admin"

    def get_queryset(self):
        factory_id = self.request.user.factorystaff.factory.id

        return list(Product.objects.filter(factory=factory_id, scheduled='2'))


class CollectedProduct(LoginRequiredMixin, UserPassesTestMixin,generic.ListView):
    login_url = "/account/"
    
    template_name = 'factory_admin/collected_list.html'
    model = Product

    def test_func(self):
        return self.request.user.userlevel == "factory_admin"

    def get_queryset(self):
        factory_id = self.request.user.factorystaff.factory.id

        return list(Product.objects.filter(factory=factory_id, scheduled='1', collected='1'))


class AddScheduleDate(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template_name = 'factory_admin/product_update.html'
    form = custForm.UpdateProductScheduleForm

    def test_func(self):
        return self.request.user.userlevel == "factory_admin"

    def get(self, request, **kwargs):
        factory_id = self.request.user.factorystaff.factory.id
        product_id = kwargs.get('pk')
        product = Product.objects.filter(factory=factory_id, scheduled='2', pk=product_id).first()
        context = {
            'product': product
        }
        return render(request, self.template_name, context=context)
    
    def post(self, request, **kwargs):
        factory_id = self.request.user.factorystaff.factory.id        
        product_id = kwargs.get('pk')

        product = Product.objects.filter(factory=factory_id, scheduled='2', pk=product_id).first()

        form = self.form(request.POST)
        if form.is_valid() and product:
            product.scheduled = '1'
            product.date_scheduled = form.cleaned_data.get('date_scheduled')
            
            product.save()
            return redirect("factory_admin:scheduled")
        return render(request, self.template_name, context={"product": product})



class ScheduledProduct(LoginRequiredMixin, UserPassesTestMixin,generic.ListView):
    login_url = "/account/"
    
    template_name = 'factory_admin/scheduled_list.html'
    model = Product

    def test_func(self):
        return self.request.user.userlevel == "factory_admin"

    def get_queryset(self):
        factory_id = self.request.user.factorystaff.factory.id
        ProductFilter = list(Product.objects.filter(scheduled='1', collected='0', factory=factory_id))

        return ProductFilter


class CollectProductView(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template_name = 'factory_admin/collect_product_form.html'
    form = custForm.UpdateProductQuantity

    def test_func(self):
        return self.request.user.userlevel == "factory_admin"

    def get(self, request, **kwargs):
        product = Product.objects.filter(
            pk=kwargs.get('pk'),
            collected='0',
            scheduled='1'
        ).first()
        if product:
            form = self.form()
            return render(request, self.template_name, context={'product': product, 'form': form})
        return redirect('factory_admin:scheduled')

    def post(self, request, **kwargs):
        product = Product.objects.filter(
            pk=kwargs.get('pk'),
            collected='0',
            scheduled='1'
        ).first()
        form = self.form(request.POST)
        if form.is_valid() and product:
            product.collected = '1'
            product.quantity = form.cleaned_data.get('quantity')
            product.save()

            payment = Payment(product=product, total_amount=(product.quantity * product.price_per_kg))
            payment.save()

            messages.success(request, 'Product details saved successfully')
            return redirect('factory_admin:scheduled')
        messages.info(request, 'Sorry... Product details failed to save')
        return render(request, self.template_name, context={'product': product, 'form': form})



#add new factory staff
class CreateFactoryStaff(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    userForm = custForm.CreateUserForm
    template_name = 'manager/factory_admin_form.html'

    def test_func(self):
        return self.request.user.userlevel == "factory_admin"

    def get(self, request):
        context = {
            'form': self.userForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.userForm(request.POST)
        if form.is_valid():
            id_number = form.cleaned_data.get('id_number')
            email = form.cleaned_data.get('email')
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            password = form.cleaned_data.get('password')
            factory_id = form.cleaned_data.get('factories')

            user = UserModel.objects.create_user(id_number, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.userlevel = 'accounts'
            user.save()

            fact = get_object_or_404(Factory, pk=factory_id)

            factory_staff = FactoryStaff(staff=user, factory=fact)
            factory_staff.save()

            return redirect('factory_admin:staff_list')
        return render(request, self.template_name, context={'form': form})


class FactoryStaffList(LoginRequiredMixin, UserPassesTestMixin,generic.ListView):
    login_url = "/account/"
    
    context_object_name = 'staffs'
    template_name = 'factory_admin/accountant_list.html'

    def test_func(self):
        return self.request.user.userlevel == "factory_admin"

    def get_queryset(self):
        try:
            return list(UserModel.objects.filter(userlevel='accounts'))
        except:
            return []


#delete factory staff
class DeleteStaffMember(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    def test_func(self):
        return self.request.user.userlevel == "factory_admin"
    
    def get(self, request, pk):
        staff = get_object_or_404(UserModel, pk=pk)
        return render(request, 'factory_admin/account_delete_confirm.html', context={'staff': staff})

    def post(self, request, pk):
        staff_id = request.POST.get('user_id')
        try:
            staff_table = FactoryStaff.objects.get(staff=staff_id).first()
            staff_table.delete()
        except:
            pass
        staff = get_object_or_404(UserModel, pk=staff_id)
        staff.userlevel = None
        staff.save()

        return redirect('factory_admin:staff_list')


class PendingBalances(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template_name = 'accountant/pending_payment_list.html'
    def test_func(self):
        return self.request.user.userlevel == "accounts"

    def get(self, request):
        accounts = list()
        factory_id = request.user.factorystaff.factory.id
        products = Product.objects.filter(factory=get_object_or_404(Factory, pk=factory_id))
        for product in products:
            try:
                payment = Payment.objects.get(product=product)
                balance = payment.total_amount - payment.paid_amount

                payment.balance = balance
                if balance > 0:
                    accounts.append(payment)
            except:
                pass
        return render(request, self.template_name, context={"accounts": accounts})

class PaymentHistory(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template = 'accountant/payment_report.html'
    form = custForm.PayForm

    def test_func(self):
        return self.request.user.userlevel == "accounts"


    def get(self, request, **kwargs):
        all = Transaction.objects.all()
        payments = list()
        user_factory = self.request.user.factorystaff.factory.id

        for one in all:
            if one.product.factory.id == user_factory:
                payments.append(one)
        context = {
                'payments': payments
            }
        return render(request, self.template, context)
    

class MakePayDeposit(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template = 'accountant/make_payment_form.html'
    form = custForm.PayForm

    def test_func(self):
        return self.request.user.userlevel == "accounts"


    def get(self, request, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('product'))
        payment = get_object_or_404(Payment, product=product) 
        payment.balance = payment.total_amount - payment.paid_amount

        context = {
                'form': self.form,
                'product': product,
                'payment': payment
            }
        return render(request, self.template, context)

    
    def post(self, request, **kwargs):
        product = get_object_or_404(Product, pk=kwargs.get('product'))
        payment = get_object_or_404(Payment, product=product) 
        payment.balance = payment.total_amount - payment.paid_amount

        form = self.form(request.POST)
        if form.is_valid():
            if payment.balance < form.cleaned_data.get('amount'):
                messages.info(request, "The amount you tried to pay is more than expected")
                return redirect('accountant:balances') 

            transaction = Transaction.objects.create(
                product = product,
                amount = form.cleaned_data.get('amount'),
                initiated_by = request.user,
                transaction_type = "deposit"
            )
            transaction.save()
            pay = get_object_or_404(Payment, product=product)
            pay.paid_amount += form.cleaned_data.get('amount')
            pay.save()

            return redirect('accountant:balances')

        context = {
            'form': form,
            'product': product,
            'payment': payment
        }
        
        return render(request, self.template, context)


#for all staff
class ProfileView(LoginRequiredMixin, UserPassesTestMixin,View):
    login_url = "/account/"
    
    template_name = 'staff/profile.html'

    def test_func(self):
        userlevel = self.request.user.userlevel

        if userlevel == 'accounts' or userlevel == 'factory_admin' or userlevel == 'manager':
            return True


    def get(self, request):
        context = {
            'userForm': UpdateUserForm(instance=request.user),
            'profileForm': ProfileForm(instance=request.user.profile)
        }
        return render(request, self.template_name, context)
    
    def post(self, request):
        user = UpdateUserForm(request.POST, instance=request.user)
        profile = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user.is_valid() and profile.is_valid():
            user.save()
            profile.save()
            messages.success(request, 'Account details updated...')
            return redirect('staff:profile')

        return render(request, self.template_name, context={"userForm": self.user, "profileForm": self.profile})
        