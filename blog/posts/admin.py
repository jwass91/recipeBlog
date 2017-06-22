# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from posts.models import Post

class PostAdmin(admin.ModelAdmin):
	list_display = ["__unicode__","title","category","ingredients","directions","timestamp","updated"]
	list_filter = ["category","updated","timestamp"]
	search_fields = ["title","ingredients","directions"]
	class Meta:
		model = Post

admin.site.register(Post, PostAdmin)