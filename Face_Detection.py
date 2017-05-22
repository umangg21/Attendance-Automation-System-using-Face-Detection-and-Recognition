import cv2 as cv
from PIL import Image 
import glob
import os

def DetectFace(image, faceCascade, returnImage=False):
    # This function takes a grey scale cv image and finds
    # the patterns defined in the haarcascade function

    #variables    
    min_size = (20,20)
    haar_scale = 1.1
    min_neighbors = 3
    haar_flags = 0

    # Equalize the histogram
    cv.cv.EqualizeHist(image, image)

    # Detect the faces
    faces = cv.cv.HaarDetectObjects(
            image, faceCascade, cv.cv.CreateMemStorage(0),
            haar_scale, min_neighbors, haar_flags, min_size
        )

    # If faces are found
    if faces and returnImage:
        for ((x, y, w, h), n) in faces:
            # Convert bounding box to two CvPoints
            pt1 = (int(x), int(y))
            pt2 = (int(x + w), int(y + h))
            cv.cv.Rectangle(image, pt1, pt2, cv.cv.RGB(255, 0, 0), 5, 8, 0)

    if returnImage:
        return image
    else:
        return faces

def pil2cvGrey(pil_im):
    # Convert a PIL image to a greyscale cv image
    pil_im = pil_im.convert('L')
    cv_im = cv.cv.CreateImageHeader(pil_im.size, cv.cv.IPL_DEPTH_8U, 1)
    cv.cv.SetData(cv_im, pil_im.tostring(), pil_im.size[0]  )
    return cv_im

def cv2pil(cv_im):
    # Convert the cv image to a PIL image
    return Image.fromstring("L", cv.cv.GetSize(cv_im), cv_im.tostring())

def imgCrop(image, cropBox, boxScale=1):
    # Crop a PIL image with the provided box [x(left), y(upper), w(width), h(height)]

    # Calculate scale factors
    xDelta=max(cropBox[2]*(boxScale-1),0)
    yDelta=max(cropBox[3]*(boxScale-1),0)

    # Convert cv box to PIL box [left, upper, right, lower]
    PIL_box=[cropBox[0]-xDelta, cropBox[1]-yDelta, cropBox[0]+cropBox[2]+xDelta, cropBox[1]+cropBox[3]+yDelta]

    return image.crop(PIL_box)

def faceCrop(imagePattern,flag,boxScale=1):
    # Select one of the haarcascade files:
    #   haarcascade_frontalface_alt.xml  <-- Best one?
    #   haarcascade_frontalface_alt2.xml
    #   haarcascade_frontalface_alt_tree.xml
    #   haarcascade_frontalface_default.xml
    #   haarcascade_profileface.xml
    faceCascade = cv.cv.Load('haarcascade_frontalface_alt.xml')
    if flag==2:
        imgList=glob.glob(imagePattern)
    else:
        imgList=imagePattern
    if len(imgList)<=0:
        print 'No Images Found'
        return
    
    count=1
    for img in imgList:
        pil_im=Image.open(img)
        cv_im=pil2cvGrey(pil_im)
        faces=DetectFace(cv_im,faceCascade)
        
        if faces:
            n=1
            for face in faces:
                croppedImage=imgCrop(pil_im, face[0],boxScale=boxScale)
                cv_im=pil2cvGrey(croppedImage)
                croppedImage=cv2pil(cv_im)
                fname,ext=os.path.splitext(img)
                ext='.pgm'
                size=92,112
                croppedImage = croppedImage.resize(size, Image.ANTIALIAS)
                croppedImage.save(str(mypath)+'\\'+str(count)+'_'+str(n)+ext)
                
                n+=1
        else:
            return False
        count=count+1
    return True


# Test the algorithm on an image
##test('2.jpg')

# Crop all jpegs in a folder. Note: the code uses glob which follows unix shell rules.
# Use the boxScale to scale the cropping area. 1=opencv box, 2=2x the width and height

mypath=''
def cropface(mypath_var,search_path,flag):
    global mypath
    mypath=mypath_var
    if flag==2:
        search_path=search_path+'/*.jpg'
    if flag==1:
        search_path=[search_path]        
    if(faceCrop(search_path,flag,boxScale=1)):
        return True
    else:
        return False
    
