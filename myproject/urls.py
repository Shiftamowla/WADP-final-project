from django.contrib import admin
from django.urls import path
from myproject.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    path('skillmatching/', skillmatching, name='skillmatching'),
    path('deletejob/<int:id>', deletejob, name='deletejob'),
    path('mainprofile/<int:id>', mainprofile, name='mainprofile'),
    path('editjob/<int:id>', editjob, name='editjob'),
    path('Addjob/', Addjob, name='Addjob'),
    path('jobfeed/', jobfeed, name='jobfeed'),


    path('searchJob/', searchJob, name='searchJob'),
    path('appliedJob/', appliedJob, name='appliedJob'),
    path('ApplyNow/<str:job_title>/<int:apply_id>', ApplyNow, name='ApplyNow'),
    path('totalTable/', totalTable, name='totalTable'),
    path('Table/', Table, name='Table'),
    path('base/', base, name='base'),
    path('home/', home, name='home'),

    path('Profile/', Profile, name='Profile'),
    path('updateprofile/<int:id>', updateprofile, name='updateprofile'),

    path('', loginpage, name='loginpage'),
    path('password_change', password_change, name='password_change'),
    path('registerpage/', registerpage, name='registerpage'),
    path('logoutpage/', logoutpage, name='logoutpage'),


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
