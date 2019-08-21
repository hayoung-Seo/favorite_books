from django.db import models
import re

# Create your models here.
class UserManager(models.Manager):
    def validator(self, postData) :
        errors = {}
        # first_name & last_name
        first_name = postData['first_name']
        if (len(first_name) == 0) :
            errors['first_name'] = "First name field is required"
        elif (len(first_name) < 2) :
            errors['first_name'] = "First name should be at least 2 characters"

        last_name = postData['last_name']
        if (len(last_name) == 0) :
            errors['last_name'] = "Last name field is required"
        elif (len(last_name) < 2) :
            errors['last_name'] = "Last name should be at least 2 characters"

        # email
        email = postData['email']
        if (len(email) == 0) :
            errors['email'] = "Email field is required"
        else :
            EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
            if not EMAIL_REGEX.match(email) :
                errors['email'] = "Invalid Email!"
            else :
                # check uniqueness
                users_emails = User.objects.filter(email=email)
                if (len(users_emails) > 0) :
                    errors['email'] = "Email already exists!"

        # password
        password = postData['password']
        if (len(password) == 0) :
            errors['password'] = "Password field is required"
        elif (len(password) < 8) :
            errors['password'] = "Password should be at least 8 characters"
        else :
            confirm_password = postData['confirm_password']
            if password != confirm_password :
                errors['confirm_password'] = "Password should match!"
        
        return errors

class User(models.Model) :
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class BookManager(models.Manager) :
    def validator(self, postData) :
        errors = {}
        # title
        title = postData['title']
        if (len(title) == 0) :
            errors['title'] = "Title field is required"
        # else :
        #     # uniquness of book title
        #     books_title = Book.objects.filter(title=title)
        #     if (len(books_title) > 0) :
        #         errors['title'] = "Book title already exists!"
        
        # description
        desc = postData['description']
        if (len(desc) < 5) :
            errors['description'] = "Desciption field should be at least 5 characters"
        
        return errors

class Book(models.Model) :
    title = models.CharField(max_length=255)
    desc = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name="books_liked")
    objects = BookManager()