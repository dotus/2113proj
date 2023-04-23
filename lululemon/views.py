from django.views.generic import ListView
from django.shortcuts import redirect 
from lululemon.forms import LogMessageForm 
from lululemon.models import Action, LogMessage, Category
from django.utils.timezone import datetime 
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from lululemon.models import Item, UserProfile
from lululemon.forms import ItemForm, NewItemForm, UserCreateForm, UserUpdateForm, UserProfileForm
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm

def home(request):
 return render(request, "lululemon/home.html")

def about(request):
 return render(request, "lululemon/about.html")

def contact(request):
 return render(request, "lululemon/contact.html")
 
def log_message(request):
    form = LogMessageForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            if "checkin_form" in request.POST:
                 #do checkin stuff
                 print("checkin")
            else:
                 print("checkin")
            qrcode=request.POST.get('qrcode')
            product=request.POST.get('product')
            #staffname=request.POST.get('staffname')
            message= form.save(commit=False)
            message.log_date = datetime.now()
            message.save()
            #LogMessage.objects.create(product=product,message=message,qrcode=qrcode)
            return redirect("home")
    else:
        return render(request, "lululemon/log_message.html", {"form": form})

class HomeListView(ListView):
    """Renders the home page, with a list of all messages."""
    model = {LogMessage}
    def get_context_data(self, **kwargs):
        context = super(HomeListView, self).get_context_data(**kwargs)
        #kwargs['message'] = LogMessage.objects.all()
        return context

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'lululemon/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality

class CustomLoginView(LoginView):
    form_class = LoginForm
'''
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'lululemon/password_reset.html'
    email_template_name = 'lululemon/password_reset_email.html'
    #subject_template_name = 'lululemon/password_reset_subject'
    #success_message = "We've emailed you instructions for setting your password, " \       
    success_url = reverse_lazy('users-home')

'''
class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'lululemon/change_password.html'
    success_message = "Your password has been successfully changed"
    success_url = reverse_lazy("home")


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'You have successfully updated your profile')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'lululemon/profile.html', {'user_form': user_form, 'profile_form': profile_form})

def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "lululemon/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="lululemon/password_reset.html", context={"password_reset_form":password_reset_form})

#Show Item_List
@login_required
def item_list(request):
    items = Item.objects.all()
    return render(request, 'lululemon/item_list.html', {'items': items})


@login_required
def item_new(request):
    if request.method == 'POST':
        # request.POST['categories'] = Category.objects.get(pk=request.POST['categories'])
        form = NewItemForm(request.POST)
        print(form)
        if form.is_valid():
            item = form.save(commit=False)
            # item.staffname = request.user.username
            item.available_quantity = form.cleaned_data['available_quantity']
            # item.checkin_quantity = form.cleaned_data['available_quantity']
            
            item.save()
            return redirect('item_detail', pk=item.pk)  # Redirect to item_detail view with valid pk value
    else:
        form = NewItemForm()
    return render(request, 'lululemon/item_new.html', {'form': form})
'''
@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            quantity = int(request.POST.get('quantity'))
            operation = request.POST.get('operation')
            if operation == 'check_in':
                item.available_quantity += quantity
                item.checkin_quantity += quantity
            elif operation == 'check_out':
                if item.available_quantity >= quantity:
                    item.available_quantity -= quantity
                    item.checkout_quantity += quantity
                else:
                    form.add_error('quantity', 'Invalid quantity, please input again.')
                    return render(request, 'lululemon/item_edit.html', {'form': form, 'item': item})
            item.save()
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'lululemon/item_edit.html', {'form': form, 'item': item})
'''

@login_required
def item_edit(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            quantity = int(request.POST.get('quantity'))
            operation = request.POST.get('operation')
            if operation == 'check_in':
                item.available_quantity += quantity
                item.checkin_quantity += quantity
            elif operation == 'check_out':
                if item.available_quantity >= quantity:
                    item.available_quantity -= quantity
                    item.checkout_quantity += quantity
                else:
                    form.add_error('quantity', 'Invalid quantity, please input again.')
                    context = {'form': form, 'item': item, 'available_quantity': item.available_quantity, 'checkin_quantity': item.checkin_quantity, 'checkout_quantity': item.checkout_quantity}
                    return render(request, 'lululemon/item_edit.html', context)
            item.save()

            # Create a new Action object to record the action performed on the item
            action_type = 'checkin' if operation == 'check_in' else 'checkout'
            action = Action(item=item, action_type=action_type, quantity=quantity)
            action.save()

            context = {'form': form, 'item': item, 'available_quantity': item.available_quantity, 'checkin_quantity': item.checkin_quantity, 'checkout_quantity': item.checkout_quantity}
            return redirect('item_detail', pk=item.pk)
    else:
        form = ItemForm(instance=item)
        context = {'form': form, 'item': item, 'available_quantity': item.available_quantity, 'checkin_quantity': item.checkin_quantity, 'checkout_quantity': item.checkout_quantity}
    return render(request, 'lululemon/item_edit.html', context)

@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    item.delete()
    return redirect('item_list')

@login_required
def inventory_management(request):
    query = request.GET.get('q')
    actions = Action.objects.all()
    if query:
        actions = actions.filter(
            Q(item__product__icontains=query) |
            Q(item__categories__categoryName__icontains=query) |
            Q(item__color__icontains=query) |
            Q(item__size__icontains=query) |
            Q(action_type__icontains=query)
        ).distinct()
    # print(Action.objects.all()[0].item)
    context = {
        # 'items': items,
        'actions': actions
    }
    return render(request, 'lululemon/inventory_management.html', context)

# class InventoryManagementView(ListView):
#     model = Action
#     template_name = 'lululemon/inventory_management.html'
#     context_object_name = 'actions'

#     def get_queryset(self):
#         return Action.objects.all()
'''
@login_required
def checkout_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    checkout = CheckOut(item=item, user=request.user)
    checkout.save()
    item.is_available = False
    item.save()
    return redirect('item_detail', pk=item.pk)

@login_required
def checkin_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    checkout = CheckOut.objects.filter(item=item, checkin_date=None).first()
    checkout.checkin_date = datetime.now()
    checkout.save()
    item.is_available = True
    item.save()
    return redirect('item_detail', pk=item.pk)

@login_required
def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    checkouts = CheckOut.objects.filter(item=item)
    return render(request, 'lululemon/item_detail.html', {'item': item, 'checkouts': checkouts})
'''
@login_required
def check_in_item(request, pk):
    item = Item.objects.get(pk=pk)
    if request.method == 'POST':
        check_in_quantity = int(request.POST.get('check_in_quantity'))
        item.available_quantity += check_in_quantity
        item.checkin_quantity += check_in_quantity
        item.save()
        return redirect('item_detail', pk=pk)
    context = {
        'item': item,
    }
    return render(request, 'lululemon/check-in.html', context)

@login_required
def item_detail(request, pk):
    item = Item.objects.get(pk=pk)
    context = {
        'item': item,
    }
    return render(request, 'lululemon/item_detail.html', context)