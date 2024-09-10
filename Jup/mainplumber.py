import pdfplumber
import os
import sys
import json
import time
import pymupdf
import io
import easyocr
import hashlib
def md5checker(fname):

    md5 = hashlib.md5()

    # handle content in binary form
    f = open(fname, "rb")

    while chunk := f.read(4096):
        md5.update(chunk)

    return md5.hexdigest()
from PIL import Image

class metadataextract:
    def __init__(self,arg1,arg2):
        self.arg1 = arg1
        self.arg2 = arg2

    def df_plumb(self):
        self.text1 = []
        lip = []
        files = pdfplumber.open(self.arg1)
        pdfpages = files.pages
        for pag in pdfpages:
            ptext = pag.extract_text()
            lip.append(ptext)
        return lip
    def save_images(self):
        pdf_file = pymupdf.open(self.arg1)
        print(self.arg1)
        for page_num in range(len(pdf_file)):
            pagey=pdf_file[page_num]
            for image_index, img in enumerate(pagey.get_images(),start=1):
                xref = img[0]
                base_image = pdf_file.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                try:
                    pil_image = Image.open(io.BytesIO(image_bytes))
                    image_path = f"images/image_{page_num}_{image_index}.{image_ext}"
                    pil_image.save(image_path)
                except:
                    pass
        texting = []
        reader = easyocr.Reader(['en'])
        for i in os.listdir("images"):
            print("images/"+i)
            if i.endswith(".jpeg"):
                result = reader.readtext("images/"+ i)
                for detection in result:
                    texting.extend(detection[1])
        for rem in os.listdir("images"):
            try:
                os.remove("images/"+rem)
            except:
                pass
        return texting

    def create_json(self,event1,event2):
        diction = {}
        diction["Title"] = self.arg1[:-4]
        diction["FileSize"] =  str(os.path.getsize(self.arg1)) +" Bits"
        diction["Time Of Creation"] = time.ctime(os.path.getmtime(self.arg1))
        diction["Last Modification"] = time.ctime(os.path.getctime(self.arg1))
        diction["Text"] = event1
        diction["Image Text"] = event2
        diction["MD5"] = md5checker(self.arg1)
        gnul = self.arg1.split("/")[1]
        gully = gnul[:-4]
        out_file = self.arg2 +"/" + gully + ".json"
        print("out: " + out_file)
        with open(out_file, "w") as jayson:
            json.dump(diction,jayson,indent=1)



if __name__ == '__main__':
    pdf_dir = sys.argv[1]
    out_dir = sys.argv[2]
    try:
        os.mkdir("images")
    except:
        pass
    try:
        os.mkdir(out_dir)

    except:
        pass
    for i in os.listdir(pdf_dir):
        if i.endswith(".pdf"):
            pdf_file = pdf_dir +"/"+ i
            process1 = metadataextract(pdf_file, out_dir)
            texty = process1.df_plumb()
            imers = process1.save_images()
            process1.create_json(texty,imers)
