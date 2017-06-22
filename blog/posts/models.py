# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify


# Create your models here.
class Post(models.Model):
	CATEGORY_CHOICES = (
			('APP','Appetizers'),
			('SAL','Salads'),
			('PAS','Pasta'),
			('MEA','Meats'),
			('OTH','Other Entrees'),
			('SID','Sides'),
			('DES','Desserts'),
		)
	title = models.CharField(max_length=120)
	image = models.FileField(null=True, blank=True)
	slug = models.SlugField(unique=True)
	category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default=None)
	ingredients = models.TextField()
	directions = models.TextField()
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
	

	def __unicode__(self):
		return self.title

	def ingredients_as_list(self):
		return self.ingredients.split('\n')

	def directions_as_list(self):
		return self.directions.split('\n')
	# def get_absolute_url(self):
	# 	return "/posts/detail/%s/" %(self.id)
def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
		new_slug = "%s-%s" %(slug,qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def preSavePostReciever(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(preSavePostReciever, sender=Post)