import shutil
import os
from pathlib import Path
import face_recognition
loopTimes = input("Enter times to loop: ")

loopDict = {}

class Files():
    def __init__(self, pathtosearch, dirname):
        self.pathtosearch = pathtosearch
        self.dirname = dirname

    def getpathtosearch(self):
        return self.pathtosearch

    def getdirname(self):
        return self.dirname
pathtosearch = input("Enter path for searching: ")
for loop in range(int(loopTimes)):


    checkingImage = input("Enter path for training: ")

    dirname = input("Enter directory to be created: ")

    loopDict[checkingImage] = Files(pathtosearch,dirname)

for key in loopDict:
    if not os.path.exists(str(loopDict[key].getdirname())):
        os.makedirs(str(loopDict[key].getdirname()))

    destdir = Path(str(loopDict[key].getpathtosearch()))
    files = [p for p in destdir.iterdir() if p.is_file()]
    # for p in files:
    #     with p.open() as f:
    #         print(f.name)

    trainingdir = Path(str(key))
    trainingFiles = [p for p in trainingdir.iterdir() if p.is_file()]




    # unknown_image = face_recognition.load_image_file("img/image4.jpg")

    listOfTrainedEncoding = []

    for index,img in enumerate(trainingFiles):
        with img.open() as f:
            print("Processing img: "+str(f.name))
            print("Image " + str(index) + " of " + str(len(trainingFiles)))
            known_image = face_recognition.load_image_file(str(f.name))
            try:

                training_encoding = face_recognition.face_encodings(known_image)[0]
                listOfTrainedEncoding.append(training_encoding)
            except:
                pass


    listOfImages = []
    listOfImagesEncoding = []
    for index,img in enumerate(files):
        with img.open() as f:
            error = False
            print(f.name)
            print("Image "+str(index)+" of "+str(len(files)))

            unknown_image = face_recognition.load_image_file(str(f.name))
            # unknown_image = face_recognition.load_image_file("img\image.jpg")
            # listOfImages.append(str(f.name))
            temp =""
            try:
                temp = face_recognition.face_encodings(unknown_image)[0]
            except:
                error = True
            print(error)
            # print(temp)
            if error is False:
                listOfImages.append(str(f.name))
                listOfImagesEncoding.append(temp)




    for index,encoding in enumerate(listOfImagesEncoding):
        print("-----------------")
        print("Image: " + str(index))
        totalTrue = 0
        totalFalse = 0
        for trainedEncoding in listOfTrainedEncoding:


            results = face_recognition.face_distance([trainedEncoding], encoding)
            print(results[0])
            if float(results[0]) < 0.45:
                totalTrue = int(totalTrue) + 1
            else:
                totalFalse = int(totalFalse) + 1

            # print(results[0])
            # if str(results[0]).lower() == str("True".lower()):
            #     print("Yes")
            #     totalTrue = int(totalTrue)+1
            #
            # else:
            #     print("NO")
            #     totalFalse = int(totalFalse)+1

        print("Image: " + str(listOfImages[index]))
        print("Voted yes: "+str(totalTrue)+"/"+str(len(listOfTrainedEncoding))+" | "+str(int(totalTrue)/int(len(listOfTrainedEncoding)))+"%")

        if (int(totalTrue)/int(len(listOfTrainedEncoding))) > 0.70:
            shutil.move(str(listOfImages[index]), str(loopDict[key].getdirname()))

