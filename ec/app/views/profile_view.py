from django.shortcuts import render, redirect
from django.views import View
from django.views import View
from django.contrib import messages
from ..forms import CustomerProfileForm
from ..models import Customer

class CustomerProfileView(View):
    def get(self, request):
        if request.user.is_authenticated:
            customer = Customer.objects.get(user=request.user) if Customer.objects.filter(user=request.user).exists() else None
            form  = CustomerProfileForm(instance=customer)
        else:
            return redirect("login")
        return render(request, "app/profile.html", {'form': form})
    
    def post(self, request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            selected_city = form.cleaned_data['city']
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            mobile = form.cleaned_data['mobile']          
            customer, created = Customer.objects.get_or_create(
                user=user, 
                defaults={'city': selected_city.region, 
                          'name': name, 
                          'locality': locality, 
                          'mobile': mobile
                          }
            )
            if not created:
                customer.name = name
                customer.locality = locality
                customer.mobile = mobile
                customer.city = selected_city.region
                customer.save()
                messages.success(request, 'Profile đã được cập nhật thành công.')
            else:
                messages.success(request, 'Profile đã được tạo thành công.')
        else:
            messages.warning(request, 'Invalid input data')
        return render(request, "app/profile.html", {'form': form})