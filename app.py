#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
	req = request.get_json(silent=True, force=True)

	print("Request:")
	print(json.dumps(req, indent=4))

	res = makeWebhookResult(req)

	res = json.dumps(res, indent=4)
	print(res)
	r = make_response(res)
	r.headers['Content-Type'] = 'application/json'
	return r

def makeWebhookResult(req):

	from collections import defaultdict	

	import re
	import pickle
	url_dict=defaultdict(list)

	with open('url_tags.pickle','rb') as handle:
		url_dict=pickle.load(handle)

	model=defaultdict(lambda:1)

	def train(features):
		for f in features:
			model[f]+=1
		return model	

	all_words_list=url_dict.keys()

	NWORDS=train(all_words_list)						
	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	def edits1(word):
		s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes    = [a + b[1:] for a, b in s if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
		replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
		inserts    = [a + c + b     for a, b in s for c in alphabet]
		return set(deletes + transposes + replaces + inserts)


	def known_edits2(word):
		return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

	def known_edits1(word):
		return set(e1 for e1 in edits1(word) if e1 in NWORDS)	


	any_list=['Sikim','Cham dance']

	def valid(item):
		dummy_set=set()
		if item in NWORDS:
			dummy_set.add(item)
			return dummy_set
		elif len(known_edits1(item))>0:
			return known_edits1(item) 	
		else:
			return known_edits2(item)
<<<<<<< HEAD

	print("save me o lord")
	try:
		print("I wanna die")
=======
	
	print("Help me o Lord")
	try:
		print("Save me")
>>>>>>> bdec59e8438564815f56c0c694b040f7d9d25349
		if req.get("result").get("action") == 'search_blog':
			print("I will survive")
			result=req.get("result")
			print("I will survive")
			parameters=result.get("parameters")
			if len(parameters.get("search_blog"))>0:
				any_list=parameters.get('any')
				
				init_set=set()
				temp_set=set()
				count=0
				print(any_list)
				for item in any_list:
					item=item.lower()
					items=valid(item)
					for item in items:
						for j in url_dict[item]:
							temp_set.add(j)
						if count==0:
							init_set=temp_set
						else:
							init_set=init_set&temp_set
					#print(init_set)
					count+=1	
					temp_set=set()	
				print(init_set)
				
				speech=""
				

				if len(init_set)>=6:
					print(init_set)
					#dummy_set=set()
					for i in init_set:
						for j in any_list:
							if j in i:	
								#dummy_set.add(i)
								speech=speech+i+'\n'
								break
					print(dummy_set)
				else:
					for i in init_set:
						speech=speech+i+"\n"	
					# print(speech)		
					
				
				return {
					"speech": speech,
					"displayText": speech,
					"data":{},# {"facebook":{"attachment": {"type": "file","payload": {"url": "https://examples.api.ai/RichMessagesFiles/LoremIpsum.pdf"}}}},
					"contextOut": [],
					"source": "apiai-onlinestore-shipping"
				}
		else:
			return{}
			
				
	except Exception as error:
		#speech=str(error)
		speech="I am inside error module \n"
		#print("Speech:"+'\t'+speech+'\t'+"flag:"+'\t'+str(flag))
		return {
			"speech": speech,
			"displayText": speech,
			#"data": {},
			# "contextOut": [],
			"source": "apiai-onlinestore-shipping"
		}

if __name__ == '__main__':
	port = int(os.getenv('PORT', 5000))

	print("Starting app on port %d" % port)

	app.run(debug=True, port=port, host='0.0.0.0')

