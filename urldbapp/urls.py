# This is the urlconf file for savewhatyoulookedat Django based application. The urls specified here are
# mapped to the request handlers in handlers.py file. The specific handlers have been imported in this file
# below.
#
# -- Supriyo.


from django.conf.urls.defaults import *
from urldbapp.test1 import current_datetime
from urldbapp.savewhatyoulookedat.handlers import userLogin, userRegister, saveURL, userLogout, firefoxPluginDownload, manageData, executeCommand, showImage, searchURL
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    (r'^time/$', current_datetime),
    (r'^savewhatyoulookedat/login/$', userLogin),
    (r'^savewhatyoulookedat/register/$', userRegister),
    (r'^savewhatyoulookedat/$', saveURL),
    (r'^savewhatyoulookedat/logout/$', userLogout),
    (r'^savewhatyoulookedat/downloadPlugin/$', firefoxPluginDownload),
    (r'^savewhatyoulookedat/managedata/$', manageData),
    (r'^savewhatyoulookedat/commandHandler/$', executeCommand),
    (r'^savewhatyoulookedat/showimage/$', showImage),
    (r'^savewhatyoulookedat/search/$', searchURL),
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)


