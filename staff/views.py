from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.views import generic, View
from .models import Factory, FactoryStaff
from farmer.models import Product
from . import forms as custForm
from account.models import UserModel
from django.http import HttpResponse


def index(request):
    return render(request, 'staff/index.html')


class CreateFactoryView(generic.CreateView):
    model = Factory
    template_name = 'manager/add_factory_form.html'
    fields = ['name', 'email', 'phone_number', 'address']


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


# Super admin
class CreateFactoryAdmin(View):
    userForm = custForm.CreateUserForm
    template_name = 'manager/add_factory_form.html'

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


class DeleteFactoryStaff(View):
    def get(self, request, pk):
        staff = get_object_or_404(UserModel, pk=pk)
        return render(request, 'manager/confirm_factory_admin_delete.html', context={'staff': staff})


    def post(self, request):
        staff_id = request.POST.get('user_id')
        staff_table = get_object_or_404(FactoryStaff, staff=staff_id)
        staff_table.delete()
        return redirect('staff:factory_admins_list')


class FactoryAdminList(generic.ListView):
    context_object_name = 'factory_admins'
    template_name = 'manager/factory_admin_list.html'

    def get_queryset(self):
        try:
            return list(UserModel.objects.filter(userlevel='factory_admin'))
        except:
            return []


# Factory Admin


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
