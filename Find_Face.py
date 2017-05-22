from sklearn.decomposition import RandomizedPCA
import numpy as np
import glob
import cv2
import math
import os
import os.path
import string

#function to get ID from filename
def ID_from_filename(filename):
    part = string.split(filename, '\\')
    return part[1].replace("s", "")
 
#function to convert image to right format
def prepare_image(filename):
    img_color = cv2.imread(filename)  # added 0 by umang
    img_gray = cv2.cvtColor(img_color, cv2.cv.CV_RGB2GRAY)  #make comment by umang 
    img_gray = cv2.equalizeHist(img_gray)
    return img_gray.flat

def searchImage(noOfface):

    IMG_RES = 92 * 112 # img resolution
    NUM_EIGENFACES = noOfface # images per train person
    NUM_TRAINIMAGES = (len(os.walk('Database').next()[1])-1)*noOfface # total images in training set

    #loading training set from folder train_faces
    folders = glob.glob('Database/*')
     
    # Create an array with flattened images X
    # and an array with ID of the people on each image y
    X = np.zeros([NUM_TRAINIMAGES, IMG_RES], dtype='int8')
    y = []

    # Populate training array with flattened imags from subfolders of train_faces and names
    c = 0
    for x, folder in enumerate(folders):
        train_faces = glob.glob(folder + '/*.pgm')
        for i, face in enumerate(train_faces):
            X[c,:] = prepare_image(face)
            y.append(ID_from_filename(face))
            c = c + 1

    # perform principal component analysis on the images
    pca = RandomizedPCA(n_components=NUM_EIGENFACES, whiten=True).fit(X)
    X_pca = pca.transform(X)

    # load test faces (usually one), located in folder test_faces
    test_faces = glob.glob('temp/*.pgm')

    # Create an array with flattened images X
    X = np.zeros([len(test_faces), IMG_RES], dtype='int8')
     
    # Populate test array with flattened imags from subfolders of train_faces 
    for i, face in enumerate(test_faces):
        X[i,:] = prepare_image(face)
     
    # run through test images (usually one)
    for j, ref_pca in enumerate(pca.transform(X)):
        distances = []
        # Calculate euclidian distance from test image to each of the known images and save distances
        for i, test_pca in enumerate(X_pca):
            dist = math.sqrt(sum([diff**2 for diff in (ref_pca - test_pca)]))
            distances.append((dist, y[i]))
        
        distances.sort()
        firstten=distances[:10]
        idlist=[]
        for i in firstten:
            idlist.append(i[1])
        found_ID = max(set(idlist), key=idlist.count)
##        found_ID = min(distances)[1]
        return found_ID 
##        print(min(distances)[0])

##        print "Identified (result: "+ str(found_ID) +" - dist - " + str(min(distances)[0])  + ")"

##        if(min(distances)[0] >= 0.65):   #changes            
##            return 0        
##        else:            
##            return found_ID              
