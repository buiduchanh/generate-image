import os 
import shutil
import glob

DIR = '/home/asilla/hanh/TextRecognitionDataGenerator/out'
TXT = '/home/asilla/hanh/TextRecognitionDataGenerator/texts/final_add.txt'
DES = '/home/asilla/hanh/TextRecognitionDataGenerator/data'
txt = []
namelist = []
imglist = sorted(glob.glob('{}/*'.format(DIR)))
for imgname in imglist:
    basename = os.path.basename(imgname)
    text = basename.split('_')[0]
    txt.append(text)
    namelist.append(basename)
newname = ['address_201081123_%07d.jpg' % i for i in range (len(txt))]
print(txt)
print(newname)
print(namelist)
exit()

with open('/home/asilla/hanh/TextRecognitionDataGenerator/texts/newadd.txt' , 'a') as f:
    for id_ , name in enumerate(newname):
        f.writelines('{} {}'.format(name, txt[id_] + "\n"))
    
    f.close()

for idx, img in enumerate (namelist):
    path = os.path.join(DIR, img)
    newpath = os.path.join(DES, newname[idx])
    shutil.copy2(path, newpath)
