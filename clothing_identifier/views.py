from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here..
from .forms import *
from .models import *
from Ekagni_AI_ML.settings import *
import os
import mimetypes
from threading import Thread
from .cloth_segmentation_main.infer import *

from .utils import *

@csrf_exempt
def image_clothing_segmentation(request):
   try:
      response = str(request.FILES["image"].read())
      try :
         form = TempVideoForm({},{'image' : request.FILES['image']})
         if(form.is_valid()):
            tempImageObj = form.save()
            tempImageObj = TempVideo.objects.get(id=tempImageObj.id)
            
            # file = (MEDIA_ROOT+str(tempImageObj.image.url))

            # return JsonResponse({
            #    'error' : tempImageObj.image.url.split('/', -1)[-1]
            # })
            # print("bEFORE ",TempVideo.objects.get(id=tempImageObj.id).image.url)
            if(tempImageObj.image.url[len(tempImageObj.image.url) - 3:] != "png") :
               jpegToPng(tempImageObj,MEDIA_ROOT)
            file = (MEDIA_ROOT+str(tempImageObj.image.url))
            print("----------------------->",file)
            generateOutput(image_dir=file,result_dir=file)
                        # ,tempImage=TempVideo.objects.get(id=tempImageObj.id))
            # print(outputImageObj.image.url)
            # file = (MEDIA_ROOT+str(outputImageObj.image.url))
            # print("After ",TempVideo.objects.get(id=tempImageObj.id).image.url)
            # file = (MEDIA_ROOT+str(TempVideo.objects.get(id=tempImageObj.id).image.url))
            path = open(file, 'rb')
            mime_type, _ = mimetypes.guess_type(file)

            # Thread(target=tempImageObj.delete).start()
            # Thread(target=outputImageObj.delete).start()

            return HttpResponse(path,content_type=mime_type)
         else :
            print(form)
            pass
      except Exception as e:
         print(e)
   except Exception as e:
      print(e)
      

   return JsonResponse({
      'error' : "something went wrong"
   })
