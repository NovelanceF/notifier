from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'Notifier.views.index', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #user login
    url(r'^login/$', 'Notifier.views.login_v', name='login'),
    url(r'^logout/$', 'Notifier.views.logout_v', name='logout'),

    #django admin page
    url(r'^admin/', include(admin.site.urls)),

    #send notification
    url(r'^sendNF/$','NFBasic.views.NFIndex'),
    url(r'^sendNF/nf_sended', 'NFBasic.views.sendNotification'),

    #send announcement
    url(r'^sendAC/$','NFBasic.views.ACIndex'),
    url(r'^sendAC/ac_sended', 'NFBasic.views.sendAnnouncement'),

    #send Announce: 127.0.0.1:8000/sendAC/?a_t=???&a_d=???&date=???&grade=???&account=???
    url(r'^getNFList/$','NFBasic.views.getNFList'),
	url(r'^getACList/$','NFBasic.views.getACList'),

    #get notification list: 127.0.0.1:8000/getNFList/
    url(r'latestAC/$','NFBasic.views.latest_announcement'),

    #get latest announcement: 127.0.0.1:8000/latestAC
    url(r'^confirmU/$','NFAdmin.views.confirmUser'),
    #/?account=???&password=???

    url(r'^detail/$','Notifier.views.detailIndex'),
    
    url(r'^iOStoken','NFBasic.views.receiveTokenFromIOS'),
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
