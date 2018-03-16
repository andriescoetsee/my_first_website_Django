from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout

# Extra Imports for the Login and Logout Capabilities
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# def user_login(request):

#     if request.method == 'POST':
#         # First get the username and password supplied
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#         # Django's built-in authentication function:
#         user = authenticate(email=email, password=password)

#         # If we have a user
#         if user:
#             #Check it the account is active
#             if user.is_active:
#                 # Log the user in.
#                 login(request,user)
#                 return HttpResponseRedirect(reverse('landing'))
#             else:
#                 messages.error(request, "Account is not active ")
#                 return HttpResponseRedirect(reverse('home'))
#         else:
#             print("Someone tried to login and failed for {}".format(email))
#             messages.error(request, "Incorrect login details ")
#             return redirect('accounts:user_login')

#     else:
#         #Nothing has been provided for username or password.
#         return render(request, 'accounts/login.html', {})



