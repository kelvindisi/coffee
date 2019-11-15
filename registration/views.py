from django.shortcuts import render, redirect
from django.views import View, generic
#from django.contrib.auth.forms import UserCreationForm as UserForm
from .forms import CreateUserForm as UserForm
from django.contrib import messages

class CreateAccountView(View):
    template_name = 'registration/registration.html'

    def get(self, request):
        context = {"form": UserForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            # save data and redirect to login
            form.save(commit=True)
            messages.success(request, "User account was successfully created!")
            return redirect('user:login')
        return render(request, self.template_name, {'form': form})
