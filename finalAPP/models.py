from django.db import models
import re
import bcrypt
class RegisterManager(models.Manager):
    def register_validation(self, postData):
        errors={}
        if len(postData['first_name'])<2:
            errors["first_name"]='First name needs to be longer than 2 characters'
        if len(postData['last_name'])<2:
            errors["last_name"]='Last name needs to be longer than 2 characters'
        EMAIL_REGEX=re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors["email"]="Invalid Email"
        if len(postData['password'])<8:
            errors["password"]="Passwords needs to be 8 characters minimum"
        if postData['password'] != postData['pw_confirmation']:
            errors['pw_no_match']="Your Password needs to match both fields"
        return errors
    def login_validation(self, postData):
        errors= {}
        existing_user=Register.objects.filter(postData['email'])
        if len(existing_user)< 1:
            errors["email"]="Email not Found"
        if len(postData['email']) == 0:
            errors['email'] = "Email must be entered"
        if len(postData['password'])<8:
            errors['password']='Password is too short, 8 characters minimum'
        elif bcrypt.checkpw(postData['password'].encode(), existing_user[0].password.encode()):
            errors['user_not_found']='Account info invalid, check email and password'
        return errors
    def authenticate(self, email, password):
        user = Register.objects.filter(email=email)
        if user:
            user=user[0]
            if bcrypt.checkpw(password.encode(), user.password.encode()):
                return True
            else:
                return False

class Register(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=255)
    objects=RegisterManager()

# ------------TRIP MODELS---------------------------------
class TripManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        if len(postData['trip']) < 2:
            errors["trip"]="Trip needs to be least 2 characters"
        if len(postData['plan']) >0 and len(postData['plan'])<15:
            errors["plan"]="Plan needs to be least 15 characters"
        if len(postData['start_date']) < 1:
            errors["start_date"]="Starting Date is needed to proceed"
        if len(postData['end_date']) < 1:
            errors["end_date"]="End Date is needed to proceed"

        return errors
class Trip(models.Model):
    name=models.CharField(max_length=255)
    plan=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    objects=TripManager()
