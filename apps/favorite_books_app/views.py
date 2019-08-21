from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from apps.favorite_books_app.models import *

# Create your views here.
def index(request) :
    return render(request, "favorite_books_app/index.html")

# register
def register(request) :
    error = User.objects.validator(request.POST)
    if (len(error) > 0) :
        for key, value in error.items() :
            messages.add_message(request, messages.ERROR, value, extra_tags=key)
        tmp_inputs = {"first_name" : request.POST['first_name'],
                        "last_name" : request.POST['last_name'],
                        "email" : request.POST['email']
                        }
        request.session['tmp_inputs'] = tmp_inputs
        return redirect('/')
    else :
        # insert into User db
        hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(
                        first_name=request.POST['first_name'],
                        last_name=request.POST['last_name'],
                        email=request.POST['email'],
                        password=hashed_pw
                         )
        request.session['user_id'] = user.id
        request.session['user_fname'] = user.first_name
        return redirect('/login')

def login_try(request) :
    email = request.POST['login_email']
    try :
        user = User.objects.get(email=email)
        hashed_pw = user.password
        if (not bcrypt.checkpw(request.POST['login_password'].encode(), hashed_pw.encode())) :
           messages.add_message(request, messages.ERROR, "Invalid user information - wrong password", extra_tags="login") 
        else :
            request.session['user_id'] = user.id
            request.session['user_fname'] = user.first_name
            return redirect('/login')
    except :
        messages.add_message(request, messages.ERROR, "Invalid user information", extra_tags="login")
    return redirect('/')

def login(request) :
    return redirect('/books')

def logout(request) :
    request.session.clear()
    return redirect('/')

def books(request) :
    books = Book.objects.all()
    cur_user = User.objects.get(id=request.session['user_id'])
    context = {"books" : books, "cur_user" : cur_user}
    return render(request, "favorite_books_app/books.html", context)

def upload_fav_book(request) :
    errors = Book.objects.validator(request.POST)
    if (len(errors) > 0) :
        print ("here: error : ", errors)
        for key, value in errors.items() :
            messages.add_message(request, messages.ERROR, value)
        return redirect('/books')
    else :
        # insert a book
        book = Book.objects.create(
                        title = request.POST['title'],
                        desc = request.POST['description'],
                        uploaded_by = User.objects.get(id=request.session['user_id'])
                        )
        user = User.objects.get(id=request.session['user_id'])
        book.liked_by.add(user)
        return redirect(f'/books/{book.id}')

def book(request, id) :
    book = Book.objects.get(id=id)
    cur_user = User.objects.get(id=request.session['user_id'])
    context = {"book" : book, "cur_user" : cur_user}
    return render(request, "favorite_books_app/book.html", context)

def update_book(request, id) :
    errors = Book.objects.validator(request.POST)
    if (len(errors) > 0) :
        for key, value in errors.items() :
            messages.add_message(request, messages.ERROR, value)
        return redirect(f'/books/{id}')
    else :
        book = Book.objects.get(id=id)
        book.title = request.POST['title']
        book.desc = request.POST['description']
        book.save()
        messages.add_message(request, messages.SUCCESS, "Updated the book successfully.")
        return redirect(f'/books/{id}')

def delete_book(request, id) :
    Book.objects.get(id=id).delete()
    return redirect('/books')

def unfavorite_book(request, id) :
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    book.liked_by.remove(user)
    return redirect(f'/books/{id}')

def add_to_favorite(request, id) :
    book = Book.objects.get(id=id)
    user = User.objects.get(id=request.session['user_id'])
    book.liked_by.add(user)
    return redirect('/books')

def user_favorites(request) :
    favorite_books = User.objects.get(id=request.session['user_id']).books_liked
    context = {"favorite_books" : favorite_books}
    return render(request, "favorite_books_app/user.html", context)