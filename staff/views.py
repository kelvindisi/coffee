from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.views import generic, View
from .models import Factory, FactoryStaff, FactoryPrice
from farmer.models import Product
from . import forms as custForm
from account.models import UserModel
from django.http import HttpResponse
from django.contrib import messages

def index(request):
    return render(request, 'staff/index.html')


# create new factory
class CreateFactoryView(View):
    factoryForm = custForm.FactoryForm
    factoryPrice = custForm.CreateFactoryPriceForm
    template_name = 'manager/add_factory_form.html'

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
class FactoryListView(generic.ListView):
    template_name = 'manager/factory_list.html'
    model = Factory
    context_object_name = 'factories'


class FactoryUpdateView(generic.UpdateView):
    template_name = 'manager/factory_update_form.html'
    fields = ['name', 'email', 'phone_number', 'address']
    model = Factory


class FactoryDeleteView(View):
    template_name = 'manager/confirm_factory_delete.html'

    def get(self, request, id):
        factory = get_object_or_404(Factory, pk=id)
        return render(request, self.template_name, context={'factory': factory})

    def post(self, request, id):
        factory = get_object_or_404(Factory, pk=id)
        factory.delete()
        return redirect('staff:factories')

"""
 SUPER ADMIN PREVILEDGES
"""
# Add new factory admin
class CreateFactoryAdmin(View):
    userForm = custForm.CreateUserForm
    template_name = 'manager/factory_admin_form.html'

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
class DeleteFactoryStaff(View):
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


class EditFactoryStaff(View):
    template_name = 'manager/fact_admin_edit_form.html'
    form = custForm.UpdateUserForm

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
class FactoryAdminList(generic.ListView):
    context_object_name = 'factory_admins'
    template_name = 'manager/factory_admin_list.html'

    def get_queryset(self):
        try:
            return list(UserModel.objects.filter(userlevel='factory_admin'))
        except:
            return []


"""
FACTORY ADMIN

"""


class NewProduct(View):
    template_name = 'factory_admin/add_farmer_produce.html'

    def get(self, request):
        productForm = custForm.CreateProductForm()
        context = {
            'form': productForm,
            'searchForm': custForm.SearchUserForm()
        }
        return render(request, self.template_name, context)


class ProductList(generic.ListView):
    model = Product
    context_object_name = 'products'




#add new factory staff
class CreateFactoryStaff(View):
    userForm = custForm.CreateUserForm
    template_name = 'manager/factory_admin_form.html'

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


class FactoryStaffList(generic.ListView):
    context_object_name = 'staffs'
    template_name = 'manager/staff_list.html'

    def get_queryset(self):
        try:
            return list(UserModel.objects.filter(userlevel='accounts'))
        except:
            return []


#delete factory staff
class DeleteStaffMember(View):
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

        return redirect('factory_admin:staff_list')


