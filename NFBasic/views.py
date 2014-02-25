from django.shortcuts import render
from django.http import HttpResponse
from NFBasic.models import Notification,Announcement,DeviceToken
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from NFBasic.forms import DocumentForm
from PIL import Image
import json
import APNSWrapper
import binascii
from igetui.igt_message import IGtAppMessage
from igetui.template.igt_notification_template import NotificationTemplate
from igetui.template.igt_transmission_template import TransmissionTemplate
from igt_push import IGeTui

APPKEY = "UB6wJSU87x5aOmNoLLgxP4"
APPID = "msjBsSDWwl6g09Lx17Q302"
MASTERSECRET = "uzkp0Ezn1r5tYTiMBKvOTA"
HOST = 'http://sdk.open.api.igexin.com/apiex.htm'

def NFIndex(request):
	if request.user.is_authenticated():
		return render(request, 'sendNF/index.html')
	else:
		return render(request, 'templates/notifier/log_req.html')

def ACIndex(request):
	if request.user.is_authenticated():
		return render(request, 'sendAC/index.html')
	else:
		return render(request, 'templates/notifier/log_req.html')

@csrf_exempt
def sendNotification(request):
	if request.user.is_authenticated():
		detail = request.POST['n_d']
		date = timezone.now()
		grade = request.POST['n_grade']
		account = request.user
		#create and save
		nf = Notification(n_detail=detail,n_pubDate=date,n_grade=grade,n_sender=account,n_date=date)
		nf.save()
		#send to app
		###
		push_Android(nf.n_detail)
		push_iOS(nf.n_detail,account.last_name)
		return render(request, 'sendNF/nf_sended.html')
	else:
		return -1

def resizeThePicture(imagePath):
	imagePath = "Notifier"+imagePath
	image = Image.open(imagePath)
	crop = ()
	x = image.size[0]
	y = image.size[1]
	if x<2*y:
		crop = (0,y/2-x/4,x,y/2+x/4)
	else:
		crop = (x/2-y,0,x/2+y,y)
	newImage = image.crop(crop)
	newImage = newImage.resize((1800,900),Image.ANTIALIAS)
	path1 = imagePath.split('.')[0]
	path2 = imagePath.split('.')[1]
	newImage.save(path1+'cropped.'+path2)

@csrf_exempt
def sendAnnouncement(request):
	#parameters
	if request.user.is_authenticated():
		title = request.POST['a_t']
		detail = request.POST['a_d']
		date = timezone.now()
		grade = request.POST['a_grade']
		u = request.user
		ac = Announcement(a_title=title,a_detail=detail,a_pubDate=date,a_grade=grade,a_sender=u)
		form = DocumentForm(request.POST, request.FILES)    
		if form.is_valid():
			ac.a_image = request.FILES['docfile']
		ac.save()
		resizeThePicture(ac.a_image.url)
		#send to app
		###
		push_Android(title)
		push_iOS(title,u.last_name)
		return render(request, 'sendAC/ac_sended.html')
	else:
		return -1

def GetListOfGrade(grade):
	list = Notification.objects.all()
	nf_list = []
	if grade == '0':
		for n in list:
			nf_list = nf_list + [n]
	else:
		for n in list:
			if n.n_grade == grade:
				nf_list = nf_list+[n]
	return nf_list


def getNFList(request):
	ITEMS_PAGE = 10

	#which pagea
	page = request.GET['page']
	list = Notification.objects.all()
	grade = request.GET['grade']
	nf_list = GetListOfGrade(grade)
	nf_list.sort(lambda x,y: cmp(x.n_pubDate,y.n_pubDate), reverse=True)

	#low - up
	low = ITEMS_PAGE * (int(page)-1)
	up = ITEMS_PAGE * int(page)
	if low>len(nf_list)-1:
		return HttpResponse('wrong')
	if up>len(nf_list):
		up = len(nf_list)
	result = []
	for i in range(low,up):
		nf = nf_list[i]
		detail = {
					'detail':nf.n_detail,
					'date':nf.n_pubDate,
					'grade':nf.n_grade,
					'name':nf.n_sender.last_name
				}
		result = result+[detail]

	dic = {
			"per_page":ITEMS_PAGE,
			"page":page,
			"pages":int(len(nf_list)/ITEMS_PAGE)+1,
			"total":len(list),
			"list":result
			}
	return HttpResponse(json.dumps(dic))

def getACList(request):
	list = Announcement.objects.all()
	ac_list = []
	for a in list:
		ac_list = ac_list+[a]
	ac_list.sort(lambda x,y: cmp(x.a_pubDate,y.a_pubDate))
	result = []
	for i in range(1,4):
		ac = ac_list[len(ac_list)-i]
		dic = {
				'title':ac.a_title,
				'detail':ac.a_detail,
				'date':ac.a_pubDate,
				'grade':ac.a_grade,
				'name':ac.a_sender.last_name,
				'imageURL':ac.a_image.url
			}
		result = result+[dic]
	dic = {
		"list":result
	}
	return HttpResponse(json.dumps(dic))

def latest_announcement(request):
	list = Announcement.objects.all()
	ac_list = []
	for a in list:
		ac_list = ac_list+[a]
	ac_list.sort(lambda x,y: cmp(x.a_pubDate,y.a_pubDate))
	ac = ac_list[len(ac_list)-1]
	result = {
				'title':ac.a_title,
				'detail':ac.a_detail,
				'date':ac.a_pubDate,
				'grade':ac.a_grade,
				'name':ac.a_sender.last_name,
				'imageURL':ac.a_image.url
			}
	return HttpResponse(json.dumps(result))

@csrf_exempt
def receiveTokenFromIOS(request):
	token = request.POST['token']
	new_token = DeviceToken(ios_token=token)
	new_token.save()
	return HttpResponse('sended')

def push_iOS(content,name):
	message_length = 3
	tokens = DeviceToken.objects.all()
	for token in tokens:
		deviceToken = binascii.unhexlify(token.ios_token)
		wrapper = APNSWrapper.APNSNotificationWrapper('apns.pem', True)
		message = APNSWrapper.APNSNotification()   
		message.badge(1)    
		message.token(deviceToken)
		alert_string = str(name)+":"+str(content)[0:message_length*3]
		message.alert(alert_string)
		wrapper.append(message)
		wrapper.notify()  

def push_Android(text):
	push = IGeTui(HOST, APPKEY, MASTERSECRET)
	template = NotificationTemplate()
	#1:click to open,2:click to nothing
	template.transmissionType = 1
	template.appId = APPID
	template.appKey = APPKEY
	template.transmissionContent = text
	template.title = "Notifier"
	template.text = text
	message = IGtAppMessage()
	message.data = template
	message.isOffline = True
	message.offlineExpireTime = 1000 * 3600 * 12
	message.appIdList.extend([APPID])
	ret = push.pushMessageToApp(message)
	print(ret)