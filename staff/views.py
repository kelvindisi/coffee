from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from .models import Factory


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
