from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.views import View
from django.contrib import messages
from ..forms import CustomerRegistrationForm

class LogOutView(View):
    def get(self, request):
        # Xử lý logic đăng xuất và chuyển hướng
        logout(request)
        pre_url = request.META.get('HTTP_REFERER', 'home')
        return redirect(pre_url)

class CustomerLoginView(View):
    def get(self, request):
        request.session['pre_url'] = request.META.get('HTTP_REFERER')
        return render(request,'app/login.html')
    
    def post(self, request):
        pre_url = request.session.get('pre_url')
        if pre_url is None or pre_url == 'register' or pre_url == 'login':
            pre_url = 'home'
 
        loginName = request.POST.get('loginName')
        password = request.POST.get('password')
        user = authenticate(request, email=loginName, password=password) or authenticate(request, username=loginName, password=password)
        if user is not None:
            login(request, user)
            del request.session['pre_url']
            return redirect(pre_url)
      
        messages.error(request, 'Username, email, or password is incorrect')
        return render(request, 'app/login.html')
    

class CustomerRegisterView(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        context = {'form': form}
        return render(request,'app/register.html', context)
    
    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successfully")
            return redirect("login")
        else:
            messages.warning(request, 'Invalid Input Data')
        return render(request, 'app/register.html', locals())