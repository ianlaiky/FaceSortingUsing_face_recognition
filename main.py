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

for loop in range(int(loopTimes)):


    checkingImage = input("Enter path for training: ")
    pathtosearch = input("Enter path for searching: ")
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

    for img in trainingFiles:
        with img.open() as f:
            print("Processing img: "+str(f.name))
            known_image = face_recognition.load_image_file(str(f.name))
            try:

                training_encoding = face_recognition.face_encodings(known_image)[0]
                listOfTrainedEncoding.append(training_encoding)
            except:
                pass


    listOfImages = []
    listOfImagesEncoding = []
    for img in files:
        with img.open() as f:
            error = False
            print(f.name)

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
        print("Image: " + str(index))
        totalTrue = 0
        totalFalse = 0
        for trainedEncoding in listOfTrainedEncoding:


            results = face_recognition.compare_faces([trainedEncoding], encoding)

            print(results[0])
            if str(results[0]).lower() == str("True".lower()):
                print("Yes")
                totalTrue = int(totalTrue)+1

            else:
                print("NO")
                totalFalse = int(totalFalse)+1

        print(totalTrue)
        print(len(listOfTrainedEncoding))
        if (int(totalTrue)/int(len(listOfTrainedEncoding)))>0.95:
            shutil.move(str(listOfImages[index]), str(loopDict[key].getdirname()))

