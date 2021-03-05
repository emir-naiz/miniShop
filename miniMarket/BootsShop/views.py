from email.headerregistry import Group
from django.contrib import messages
from django.contrib.auth import authenticate, login, get_user_model, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


from .forms import RegistrationForm, UserProfileForm, ProfileUpdateForm
from .models import Products, Category, UserProfile
from .tokens import account_activation_token


def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
             user = form.save(commit=False)
             user.is_active = False
             user.save()
             UserProfile.objects.create(user=user, phone=1,name=user.username)
             current_site = get_current_site (request)
             mail_subject = 'Активируйте свою учетную запись.'
             message = render_to_string('accounts/acc_active_email.html', {
                 'user': user,
                 'domain': current_site.domain,
                 'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                 'token': account_activation_token.make_token(user),
             })
             to_email = form.cleaned_data.get('email')
             email = EmailMessage(
                 mail_subject, message, to=[to_email]
             )
             email.send()
             return HttpResponse('Подтвердите свой адрес электронной почты для завершения регистрации')
        else:
            form = RegistrationForm()
    return render(request, 'accounts/user-create.html', {'form': form})

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()


        return HttpResponse('Спасибо за подтверждение по электронной почте. Теперь вы можете войти в свою учетную запись !')
    else:
        return HttpResponse('Ссылка для активации недействительна!')

def auth(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        login(request,user)
        return redirect('home')
    context = {}
    return render(request,'accounts/login.html',context)

def logout_page(request):
    logout(request)
    return redirect('login')

@login_required(login_url=['login'])
def CreateUser(request):
    user = request.user.userprofile
    form = UserProfileForm(instance= user)
    if request.method =='POST':
        form = UserProfileForm(request.POST,request.FILES,instance=user)
        form.save()
    context = {'form':form}
    return render(request,'accounts/profile.html',context)

@login_required
def profile(request):
    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.userprofile)
        if p_form.is_valid():
            p_form.save()

            return redirect('profile')
    else:
        p_form = ProfileUpdateForm(instance=request.user.userprofile)
    context = {
        'p_form': p_form
    }
    messages.success(request, f'Ваш аккаунт изменен!')
    return render(request, 'accounts/profile.html', context)


def productList(request):
    products = Products.objects.all()
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render (request, 'accounts/products.html', context)

def category(request, category_id):
    try:
        category = Category.objects.get(id=category_id)
    except Category.DoesNotExist:
        return HttpResponse('Page status = 404')

    products = category.products.all()
    context = {'category': category, 'products': products}
    return render (request, 'accounts/category.html', context)
