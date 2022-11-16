from PIL import Image

# Example file : C:\\temp\Images\filename.jpg   to  temp\Images\filename.png
def jpegToPng(tempImageObj,actualPath):
    # your code here
    # ne kor
   # pathX = open(file,'r+')
    # img = Image.open(actualPath+file)
    #img.save(actualPath+file,'png')
    Image.open(tempImageObj.image.url).convert('RGB').save(tempImageObj.image.url[:-3]+"png")
    tempImageObj.image = tempImageObj.image.url[:-3]+"png"
    tempImageObj.save()
    print("===>>>>",tempImageObj.image.url)