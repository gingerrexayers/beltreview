from django.shortcuts import render, redirect
from .models import Author, Book, Review
from ..loginreg.models import User
from django.core.urlresolvers import reverse
# Create your views here.

def index(request):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not 'errors' in request.session:
        request.session['errors'] = []
    context = {
        'user': User.manager.get(id=request.session['id']),
        'reviews': Review.objects.all().order_by('-created_at')[:5],
        'books': Book.objects.all().order_by('title')
    }
    return render(request, 'reviews/index.html', context)

def show(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not 'errors' in request.session:
        request.session['errors'] = []
    reviews = Review.objects.all().filter(book_id=id)
    context = {
        'reviews': reviews,
        'book': reviews[0].book
    }
    return render(request, 'reviews/show.html', context)

def add(request):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not 'errors' in request.session:
        request.session['errors'] = []
    context = {
        'authors': Author.objects.all().order_by('name'),
        'errors': request.session.pop('errors')
    }
    return render(request, 'reviews/add.html', context)

def addtoexisting(request, id):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not request.method=='POST':
        return redirect(reverse('books:show', kwargs={'id':id}))
    if len(request.POST['review']) == 0:
        request.session.errors.append('Must have a review!')
        return redirect(reverse('books:show', kwargs={'id':id}))

    b = Book.objects.get(id=id)
    Review.objects.create(user=User.manager.get(id=request.session['id']), book=b, rating=request.POST['rating'], review=request.POST['review'])
    return redirect(reverse('books:show', kwargs={'id':id}))

def create(request):
    if not 'id' in request.session:
        return redirect(reverse('login:index'))
    if not request.method=='POST':
        return redirect(reverse('books:add'))
    if len(request.POST['title']) == 0 or len(request.POST['review']) == 0:
        request.session.errors.append('Must have a title and a review!')
        return redirect(reverse('books:add'))

    if len(request.POST['authornew']) == 0:
        b = Book.objects.create(title=request.POST['title'], author=Author.objects.get(id=request.POST['authorselect']))
        Review.objects.create(user=User.manager.get(id=request.session['id']), book=b, rating=request.POST['rating'], review=request.POST['review'])
    else:
        a = Author.objects.create(name=request.POST['authornew'])
        b = Book.objects.create(title=request.POST['title'], author=a)
        Review.objects.create(user=User.manager.get(id=request.session['id']), book=b, rating=request.POST['rating'], review=request.POST['review'])
    return redirect(reverse('books:show', kwargs={'id':b.id}))

def delete(request, id):
    r = Review.objects.get(id=id)
    if request.session['id']==r.user.id:
        r.delete()
    return redirect(reverse('books:index'))
