import re
import operator

msglist=[]		#this list will contain dictionary of each message
infile=open('WhatsApp Chat with 601-1.txt', 'r')

badwords=[
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* was added$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* were added$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* added .*$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* left$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* was removed$'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* changed to \+.*'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* created group .*'),
re.compile('^\d?\d/\d?\d/\d\d, \d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)? .* Messages you send to this chat and calls are now secured with end-to-end encryption.')
]
fucksgiven=0

for aline in infile.readlines():
	if any(badword.match(aline) for badword in badwords): #this will skip unwanted messages
		continue
	msg={}
	isNewMsg=re.search(r'^(\d?\d/\d?\d/\d\d), (\d?\d:\d?\d(?: [AaPp]\.?[Mm]\.?)?) - (.*?): (.*)',aline) #regex matching a new message line
	if isNewMsg:
		#add everything to a dictionary
		msg['date'] = isNewMsg.group(1)
		msg['time'] = isNewMsg.group(2)
		msg['sender'] = isNewMsg.group(3)
		msg['message'] = isNewMsg.group(4)
		msglist.append(msg)
	else:		#if it is not a new message line then it is part of the previous message so append to that
		msg=msglist.pop()
		msg['message']+=aline
		msglist.append(msg)

print("Number of messages in this conversation:"+str(len(msglist)))
print("")

#find stats of each member
memberstats={}
for msg in msglist:
	
	if msg['sender'] in memberstats:
		memberstats[msg['sender']]+=1
	else:
		memberstats[msg['sender']]=1

print("Top five most active members:")
sortedmembers = sorted(memberstats.items(), key=operator.itemgetter(1), reverse=True)
for member in sortedmembers[0:5]:
	print(member[0]+" : "+str(member[1]) )

print("")
#finding most active and least active users
#mostactive=max(memberstats.iteritems(), key=operator.itemgetter(1))[0]
leastactive=min(memberstats.iteritems(), key=operator.itemgetter(1))[0]
print("Least active member:")
print(leastactive+" sent "+str(memberstats[leastactive])+" messages")

