from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
	def registration_validator(self, postData):
		errors = {}
		if len(postData['name']) < 1:
			errors["name1"] = "Name is required!"
		else:
			if len(postData['name']) < 3:
				errors["name2"] = "Name must be at least 3 characters!"

		if len(postData['username']) < 1:
			errors["username1"] = "Username is required!"
		else:
			if len(postData['username']) < 3:
				errors["username2"] = "Username must be at least 3 characters!"

		if len(postData['password']) < 1:
			errors["password1"] = "Password is required!"
		else:
			if len(postData['password']) < 8:
				errors["password2"] = "Password must be at least 8 characters!"

		if postData['password'] != postData['pass_confirm']:
			errors["password3"] = "Password and confirmation field must match!"

		if list(User.objects.filter(username=postData['username'])) != []:
			errors["username3"] = "This username is already in use!"

		if postData['hired'] == '':
			errors['hired1'] = "Must enter hired date!"
		else:
			date_format = "%Y-%m-%d"
			input_hired = datetime.strptime(postData['hired'], date_format)
			now = datetime.now()
			if input_hired >= now:
				errors["hired2"] = "Date hired can not be in the future!"

		
		return errors

	def login_validator(self, postData):
		errors = {}
		if len(postData['username']) < 1:
			errors["login"] = "Username and password combination not in our record!"
		if len(postData['password']) < 1:
			errors["login"] = "Username and password combination not in our record!"
		try:
			user = User.objects.get(username=postData['username'])
			if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
				errors["login"] = "Password does not match our record."
		except:
			errors["login"] = "Username and password combination are not in our record"
		return errors

class ItemManager(models.Manager):
	def validator(self,postData):
		errors = {}
		if len(postData['name']) < 1:
			errors["name1"] = "Item field is required!"
		elif len(postData['name']) < 4:
			errors["name2"] = "Item field must be more than 3 characters!"
		return errors


class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	hired = models.DateTimeField(auto_now_add=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()

class Item(models.Model):
	name = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	user = models.ForeignKey('User', related_name="items") #user that added the quote
	wish_users = models.ManyToManyField('User', related_name="wish_items")

	objects = ItemManager()