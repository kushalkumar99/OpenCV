# LBPH face recognizer, fisherface recognizer
#local binary pattern-> matrix, labels pixels by comparing neighbour pixels, threshold

import cv2.face
import numpy,os
haar_file = 'haarcascade_frontalface_default.xml'
face_cascade = cv2.CascadeClassifier(haar_file)
datasets = 'people'
print('training')
(images,lables,names,id) =([],[],{},0)

for (subdirs,dirs,files) in os.walk(datasets):
    for subdir in dirs:
        names[id] = subdir
        subjectpath = os.path.join(datasets,subdir)
        for filename in os.listdir(subjectpath):
            path = subjectpath + '/' + filename
            label= id
            images.append(cv2.imread(path,0))
            lables.append(int(label))
            # print(label)
        id += 1

(images,lables) = [numpy.array(lis) for lis in [images,lables]] # this numpy.array converts all images into list of an array
# print(images,lables)
(width,height)=(130,100)
model = cv2.face.LBPHFaceRecognizer_create() #--> LBPHFaceRecognizer_create() is classifier
#model = cv2.face.FisherFaceRecognizer_create()

model.train(images,lables)
webcam = cv2.VideoCapture(0)
cnt =0
while True:
    _,img=webcam.read()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,255,0),2)
        face = gray[y:y+h,x:x+w] #croping part, we need only not full body
        face_resize = cv2.resize(face,(width,height))

        prediction = model.predict(face_resize)
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),3)
        
        if prediction[1]<950:#-> prediction[1] resembles accuracy ,increase this for more accuracy,vice versa
            cv2.putText(img,'%s-%.0f'%(names[prediction[0]],prediction[1]),(x-10,y-10),cv2.FONT_ITALIC,1,(0,0,255))
            print(names[prediction[0]])
            cnt =0
        else:
            cnt+=1
            cv2.putText(img,'unknown',(x-10,y-10),cv2.FONT_ITALIC,1,(0,0,255))
            if cnt >100:
                print("unknown person")
                cv2.imwrite("unknown.jpg",img)
                cnt = 0
    cv2.imshow('FaceRecognition',img)
    key = cv2.waitKey(10)
    if key ==27:
        break
webcam.release()
cv2.destroyAllWindows()