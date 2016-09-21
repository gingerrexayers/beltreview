from django.shortcuts import render, redirect
from .models import User
from ..reviews.models import Review, Book
from django.core.urlresolvers import reverse

# Create your views here.

def index(request):
    if not 'errors' in request.session:
        request.session['errors'] = []
    return render(request, 'loginreg/index.html')

def register(request):
    if request.method=='POST':
        result = User.manager.register(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirmation'])

        if result[0]:
            request.session['id'] = result[1].id
            request.session.pop('errors')
            return redirect(reverse('login:success'))
        else:
            request.session['errors'] = result[1]
            return redirect(reverse('login:index'))

def login(request):
    if request.method=='POST':
        result = User.manager.login(request.POST['email'], request.POST['password'])
        if result[0]:
            request.session['id'] = result[1].id
            request.session.pop('errors')
            return redirect(reverse('login:success'))

def logout(request):
    request.session.pop('id')
    return redirect(reverse('login:index'))

def success(request):
    return redirect(reverse('books:index'))

def user(request, id):
    u = User.manager.get(id=id)
    reviews = Review.objects.all().filter(user_id=id)
    context = {
        'user': u,
        'reviews': reviews
    }
    return render(request, 'loginreg/user.html', context)
