import shutil
import os
from pathlib import Path

checkingImage = input("Enter relative path from .py to Image as base: ")
pathtosearch = input("Enter path for searching: ")
dirname = input("Enter directory to be created: ")

if not os.path.exists(str(dirname)):
    os.makedirs(str(dirname))

destdir = Path(str(pathtosearch))
files = [p for p in destdir.iterdir() if p.is_file()]
# for p in files:
#     with p.open() as f:
#         print(f.name)


import face_recognition
known_image = face_recognition.load_image_file(str(checkingImage))
# unknown_image = face_recognition.load_image_file("img/image4.jpg")

biden_encoding = face_recognition.face_encodings(known_image)[0]

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
    print("Image: "+str(index))
    results = face_recognition.compare_faces([biden_encoding], encoding)
    print(results[0])
    if str(results[0]).lower() == str("True".lower()):
        print("Yes")

        shutil.move(str(listOfImages[index]), str(dirname))
    else:
        print("NO")

