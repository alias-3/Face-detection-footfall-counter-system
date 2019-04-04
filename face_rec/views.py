from django.shortcuts import render
from django.http import HttpResponse
from . import empFace,recognition,empTrainer,empregister
import sys
from .footfall import footfall
import json
import time

def index(request):
	if request.method=="POST" and request.POST.get('face')=='face':
		empFace.face()
		return render(request,'home.html')
		# tweet_list = twitter_script.tweets(request.POST.get('query'),request.POST.get('numtweets'))
		# pos,neg,net,csv_list,pol_dict = twitter_script.analysis(tweet_list)
		# context = {
		# 	'tweet_list' : tweet_list,
		# 	'pos': (pos*100/int(request.POST.get('numtweets'))),
		# 	'neg': (neg*100/int(request.POST.get('numtweets'))),
		# 	'net': (net*100/int(request.POST.get('numtweets'))),
		# 	'csv_list' : json.dumps(csv_list),   
		# 	'csv_len' : len(csv_list),
		# 	'pol_dict' : pol_dict,
		# 	't': len(tweet_list)
		# }
		# return render(request,"index.html",context)
	#else: 
		# context = {
		# 	'csv_len' : 0,
		# 	'q': request.POST.get('query')
		# }
	elif request.method=="POST" and request.POST.get('test')=='test':
		recognition.rec()
		return render(request,'home.html')

	elif request.method=="POST" and request.POST.get('train')=='train':
		empTrainer.train()
		return render(request,'home.html')
	elif request.method=="POST" and request.POST.get('startcount')=='startcount':
		footfall.count()
		return render(request,'home.html')
	else:

		return render(request,'home.html')	

def register_employee(request):
	if request.method == "POST" :
		ename = str(request.POST.get('empname'))
		eid = (request.POST.get('empid'))
		empregister.empregister(eid,ename)
		time.sleep(2)
		empFace.face(eid)
		time.sleep(2)
		return render(request,'success.html')
	else:
		return render(request,'addemployee.html')

def train(request):
	if request.method == "POST":
		empTrainer.train()
		return render(request,'home.html')
	else:
		return render(request,'train.html')