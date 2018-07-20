import shutil
import os
from pathlib import Path

checkingImage = input("Enter path for training: ")
pathtosearch = input("Enter path for searching: ")
dirname = input("Enter directory to be created: ")

if not os.path.exists(str(dirname)):
    os.makedirs(str(dirname))

destdir = Path(str(pathtosearch))
files = [p for p in destdir.iterdir() if p.is_file()]
# for p in files:
#     with p.open() as f:
#         print(f.name)

trainingdir = Path(str(checkingImage))
trainingFiles = [p for p in trainingdir.iterdir() if p.is_file()]


import face_recognition

# unknown_image = face_recognition.load_image_file("img/image4.jpg")

listOfTrainedEncoding = []

for img in trainingFiles:
    with img.open() as f:
        print("Processing img: "+str(f.name))
        known_image = face_recognition.load_image_file(str(f.name))
        training_encoding = face_recognition.face_encodings(known_image)[0]
        listOfTrainedEncoding.append(training_encoding)


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
            totalTrue= int(totalTrue)+1

        else:
            print("NO")
            totalFalse = int(totalFalse)+1

    print(totalTrue)
    print(len(listOfTrainedEncoding))
    if (int(totalTrue)/int(len(listOfTrainedEncoding)))>0.66:
        shutil.move(str(listOfImages[index]), str(dirname))

