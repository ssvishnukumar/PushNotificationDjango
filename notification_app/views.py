from django.shortcuts import render
from django.http import HttpResponse
import requests
import json
from django.conf import settings

def send_notification(registration_ids , message_title , message_body, message_subtitle):
    cloud_messaging_api_key = settings.CLOUD_MESSAGING_API_KEY
    url = "https://fcm.googleapis.com/fcm/send"

    headers = {
    "Content-Type":"application/json",
    "Authorization": 'key=' + cloud_messaging_api_key
    }

    payload = {
        # we can use "to" for single device notification
        # "to": registration_id
        "registration_ids" :registration_ids,
        "priority" : "high",
        "notification" : {
            "body" : message_body,
            "title" : message_title,
            "subtitle": message_subtitle
            # "image" : image_link,
            # "icon": icon_link,
        }
    }

    result = requests.post(url,  data=json.dumps(payload), headers=headers )
    print(result.json())


def index(request):
    # key pair under web configuration
    vapid_key = settings.PUBLIC_VAPID_KEY
    context = {}
    context['vapid_key'] = vapid_key
    return render(request , 'index.html', context)


def send(request, fcm_notification_device_key):
    device_registration  = [
        fcm_notification_device_key
    ]
    send_notification(
        device_registration , 
        'query raised' , 
        '''A query has been raised in your area of expertise. Assist the learner and earn points.
Prajjwal Sharma has asked you a query.
Can you solve his/her doubt in bentley microstation?
"test query"'''
        , 'This is the Message Subtitle')
    return HttpResponse("Sent ")

def showFirebaseJS(request):
    data='importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-app.js");' \
         'importScripts("https://www.gstatic.com/firebasejs/8.6.3/firebase-messaging.js"); ' \
         'var firebaseConfig = {' \
         '        apiKey: "AIzaSyBUpL5bR5VjKaM7uOwlrlWyRtFpCFlgiEs",' \
         '        authDomain: "pushnotification-test-3fa8c.firebaseapp.com",' \
         '        projectId: "pushnotification-test-3fa8c",' \
         '        storageBucket: "pushnotification-test-3fa8c.appspot.com",' \
         '        messagingSenderId: "833444013728",' \
         '        appId: "1:833444013728:web:44275fd996a9d577b68bc5",' \
         '        measurementId: "G-6B9YHD1FE6"' \
         ' };' \
         'firebase.initializeApp(firebaseConfig);' \
         'const messaging=firebase.messaging();' \
         'messaging.setBackgroundMessageHandler(function (payload) {' \
         '    console.log(payload);' \
         '    const notification=JSON.parse(payload);' \
         '    const notificationOption={' \
         '        body:notification.body,' \
         '        icon:notification.icon' \
         '    };' \
         '    return self.registration.showNotification(payload.notification.title,notificationOption);' \
         '});'

    return HttpResponse(data,content_type="text/javascript")