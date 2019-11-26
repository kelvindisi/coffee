from django.shortcuts import render, get_object_or_404, redirect, get_list_or_404
from django.contrib.auth.models import User
from django.views import generic, View
from .models import Factory
from farmer.models import Product
from . import forms as custForm
from account.models import UserModel


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
        form = self.userForm(request.post)
        if not form.is_valid():
            return render(request, self.template_name, context={'form': form})
        form.userlevel = 'factory_admin'
        form.save()
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
