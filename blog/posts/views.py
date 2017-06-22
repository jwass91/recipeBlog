# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Post
from django.db.models import Q
from .forms import PostForm
from django.contrib import messages
# Create your views here.

def posts_create(request):
	if request.user.is_authenticated():
		form = PostForm(request.POST or None, request.FILES or None)
		message = ""
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request,'Post Created',extra_tags='html_save')
			message="suc"
			return HttpResponseRedirect("/posts/detail/%s" %instance.id)
		context = {
			"form":form,
			"message":message,
		}
		return render(request,"post_form.html",context)
	else:
		context = {
			"title":"List"
		}
		return render(request, "error.html", context)

def posts_detail(request,slug):
	auth = False
	if request.user.is_authenticated():
		auth = True
	instance = get_object_or_404(Post,slug=slug)
	context = {
		"instance":instance,
		"auth":auth
	}
	return render(request, "post.html", context)


def posts_list(request):
	auth = False
	if request.user.is_authenticated():
		auth = True
	queryset_list = Post.objects.all().order_by('-timestamp')

	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(
			Q(title__icontains=query) |
			Q(directions__icontains=query) |
			Q(ingredients__icontains=query) |
			Q(category__icontains=query)
			).distinct()
	paginator = Paginator(queryset_list, 7) # Show 25 contacts per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
	    # If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
	    # If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	if queryset_list.count() % 7 != 0:
		last_page = queryset_list.count() / 7 + 1
	else:
		last_page = queryset_list.count() / 7

	if queryset_list.count() % 14 != 0:
		middle = queryset_list.count() / 14 + 1
	else:
		middle = queryset_list.count() / 14

	if last_page < 3:
		oneOrTwo = True
	else:
		oneOrTwo = False	
				
	context = {
		"objects":queryset,
		"auth":auth,
		"last_page": last_page,
		"middle": middle,
		"middle2": middle + 1,
		"numMiddle": last_page % 2,
		"oneORTwo":	oneOrTwo,
	}
	return render(request, "index.html", context)


def posts_update(request,slug=None):
	if request.user.is_authenticated():
		instance = get_object_or_404(Post,slug=slug)
		form = PostForm(request.POST or None, request.FILES or None, instance=instance)
		message = ""
		if form.is_valid():
			instance = form.save(commit=False)
			instance.save()
			messages.success(request,'Post Saved',extra_tags='html_save')
			return HttpResponseRedirect("/posts/detail/%s" %instance.slug)
		context = {
			"instance":instance,
			"form":form,
			"message":message,
		}
		return render(request, "post_update.html", context)
	else:
		context = {
			"title":"List"
		}
		return render(request, "error.html", context)

def posts_delete(request,slug):
	if request.user.is_authenticated():
		instance = get_object_or_404(Post,slug=slug)
		instance.delete()
		messages.success(request,'Post Deleted',extra_tags='html_save')
		return redirect("posts")
	else:
		context = {
			"title":"List"
		}
		return render(request, "error.html", context)