# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
from django.contrib import messages
from random import randint

# Create your views here.
def sessCheck(request):
	try:
		return request.session['user_id']
	except:
		return False

def welcome(request):
	return render(request, 'user_gold/welcome.html')

def home(request):
	if sessCheck(request) == False:
		return redirect('/')
	context = {'users': User.objects.all(), 'user': User.objects.get(id = request.session['user_id'])}
	return render(request, 'user_gold/home.html', context)

def leaderboard(request):
	users = User.objects.all().order_by('-gold')
	context = {'users': User.objects.all().order_by('-gold')[:5], 'user': User.objects.get(id = request.session['user_id'])}
	return render(request, 'user_gold/leaderboard.html', context)

def show(request):
	user = User.objects.get(id = request.session['user_id'])
	context = {'user': User.objects.get(id = request.session['user_id']), 'activities': Activity.objects.filter(user_id = user.id).order_by('-created_at')}
	return render(request, 'user_gold/show.html', context)

def play(request):
	# Check if line below is needed since context exists
	users = User.objects.all().order_by('-gold')
	count = 1
	for user in users:
		user.rank = count
		user.save()
		count += 1
	context = {'user': User.objects.get(id = request.session['user_id']), 'activities': Activity.objects.filter(user_id = request.session['user_id']).order_by('-created_at')}
	return render(request, 'user_gold/play.html', context)

def register(request):
	results =  User.objects.RegVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	user = User.objects.creator(request.POST)
	messages.success(request, 'User has been created. Please log into continue!')
	return redirect('/')

def login(request):
	results = User.objects.LogVal(request.POST)
	if results['status'] == False:
		for error in results['errors']:
			messages.error(request, error)
		return redirect('/')
	request.session['user_id'] = results['user'].id
	request.session['user_name'] = results['user'].name
	return redirect('/home')


def process(request):
	user = User.objects.get(id = request.session['user_id'])
	og_gold = user.gold
	if request.POST.get('building') == 'farm':
		user.gold += randint(-1, 1)
	if request.POST.get('building') == 'cave':
		user.gold += randint(-5, 5)
	if request.POST.get('building') == 'castle':
		user.gold += randint(-10, 10)
	users = User.objects.all().order_by('-gold')
	user.save()
	new_gold = user.gold
	gold_diff = new_gold - og_gold
	if request.POST['building']:
		if gold_diff >= 0:
			activity = Activity.objects.create(
				description = ('{} gold earned on'.format(gold_diff)), user_id = user.id)
			activity.save()
		if gold_diff < 0:
			activity = Activity.objects.create(
				description = ('{} gold lost on'.format(gold_diff)), user_id = user.id)
			activity.save()

	if user.gold < 0:
		activities = Activity.objects.all()
		user_activities = activities.filter(user_id = user.id)
		user_activities.delete()
		user.delete()
		return redirect('/')
	return redirect('/play')

def delete(request, id):
	user = User.objects.get(id = id)
	activities = Activity.objects.all()
	user_activities = activities.filter(user_id = user.id)
	user_activities.delete()
	user.delete()
	return redirect('/home')

def logout(request):
	request.session.flush()
	return redirect('/')