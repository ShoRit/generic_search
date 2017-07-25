from collections import defaultdict
import re
import pickle
import sys
url_dict=defaultdict(list)

url_add=sys.argv[1]

print(url_add.split('//')[1])
b=url_add.split('//')[1]
c=b.split('.')
if c[0]=='www':
	file_ext=c[1]
else:
	file_ext=c[0]

print(file_ext)

inp_file=file_ext+'_url_tags.pickle'

with open(inp_file,'rb') as handle:
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

import sys
text_string=sys.argv[2]
any_list=text_string.split(' ')


def valid(item):
	dummy_set=set()
	if item in NWORDS:
		dummy_set.add(item)
		return dummy_set
	elif len(known_edits1(item))>0:
		return known_edits1(item) 	
	else:
		return known_edits2(item)


init_set=set()
temp_set=set()
count=0

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

remove_set=set()
for i in init_set:
	if '/?replytocom' in i:
		remove_set.add(i)

init_set=init_set.difference(remove_set)		

if len(init_set)>=10:
	dummy_set=set()
	for i in init_set:
		for j in any_list:
			if j in i:	
				dummy_set.add(i)
				break
	print(dummy_set)
else:
	print(init_set)			
	


'''
	
	import re
	url_dict=defaultdict(list)

	PFT='http://www.anirbansaha.com/parsi-fire-temple-kolkata-india/'
	query_list1=['Calcutta Walks','Iftekhar Ahsan','Parsi community in Kolkata','Parsi Fire Temple']

	for i in query_list1:
		i=i.lower()
		url_dict[i].append(PFT)

	Saga_dawa='http://www.anirbansaha.com/saga-dawa-gangtok-sikkim/'
	query_list2=['Buddhist festivals in Sikkim','Saga Dawa','Saga Dawa Gangtok','Saga Dawa Sikkim','Sikkim','Gangtok']

	for i in query_list2:
		i=i.lower()
		url_dict[i].append(Saga_dawa)

	Ravangla='http://www.anirbansaha.com/ravangla-geyzing-monastery-chham-photographs/'
	query_list3=['Geyzing','Hills','north east india','Pelling','Pemayangtse monastery','Rabdantse','Ralang monastery','Ravangla', 'Sikkim', 'Sikkim tourism', 'Simptham', 'Travel destinations','Travel to Sikkim from Kolkata']

	for i in query_list3:
		i=i.lower()
		url_dict[i].append(Ravangla)

	Cham='http://www.anirbansaha.com/kayged-festival-ralang-monastery-cham-dance-in-ralang-monastery-sikkim/'
	query_list4=[ 'Black hat dance', 'Buddhist custom', 'Cham', 'Cham dance costumes', 'Cham dance mask', 'Cham dance photographs', 'cham mask', 'chham dance', 'chham dance sikkim', 'chham festival', 'chham festival sikkim', 'Folk culture', 'Folk dance', 'Kaged festival', 'Kagyat festival', 'Karma Lama', 'Karmapa Mahakala Dance', 'Mahakala Dance', 'Masked Dances', 'Tibetan dance','Sikkim','Chaam','Chaam Dance']	

	for i in query_list4:
		i=i.lower()
		url_dict[i].append(Cham)

	paragliding='http://www.anirbansaha.com/paragliding-gangtok-sikkim/'
	query_list5=['Sikkim','Winter','Travel',"Gangtok",'Paragliding']

	for i in query_list5:
		i=i.lower()
		url_dict[i].append(paragliding)

	print(url_dict['sikkim'])

	model=defaultdict(lambda:1)

	def train(features):
		for f in features:
			model[f]+=1
		return model	

	all_words_list=[]

	for i in query_list1:
		i=i.lower()
		all_words_list.append(i)
	for i in query_list2:
		i=i.lower()
		all_words_list.append(i)
	for i in query_list3:
		i=i.lower()
		all_words_list.append(i)				
	for i in query_list4:
		i=i.lower()
		all_words_list.append(i)
	for i in query_list5:
		i=i.lower()
		all_words_list.append(i)

	NWORDS=train(all_words_list)						
	alphabet = 'abcdefghijklmnopqrstuvwxyz'

	def edits1(word):
		s = [(word[:i], word[i:]) for i in range(len(word) + 1)]
		deletes= [a + b[1:] for a, b in s if b]
		transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
		replaces= [a + c + b[1:] for a, b in s for c in alphabet if b]
		inserts   = [a + c + b     for a, b in s for c in alphabet]
		return set(deletes + transposes + replaces + inserts)


	def known_edits2(word):
		return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

	def known_edits1(word):
		return set(e1 for e1 in edits1(word) if e1 in NWORDS)	

	def valid(item):
		dummy_set=set()
		if item in NWORDS:
			dummy_set.add(item)
			return dummy_set
		elif len(known_edits1(item))>0:
			return known_edits1(item) 	
		else:
			return known_edits2(item)	
'''			
