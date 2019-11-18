from django.shortcuts import render, redirect
from django.views import View, generic
from .forms import CreateUserForm as UserForm, UpdateUserForm, ProfileForm
from django.contrib import messages


class CreateAccountView(View):
    template_name = 'account/registration.html'

    def get(self, request):
        context = {"form": UserForm()}
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            # save data and redirect to login
            form.save(commit=True)
            messages.success(request, "User account was successfully created!")
            return redirect('account:login')
        return render(request, self.template_name, {'form': form})


class ProfileView(View):
    template_name = 'account/profile.html'

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
            return redirect('account:profile')

        return render(request, self.template_name, context={"userForm": self.user, "profileForm": self.profile})
        