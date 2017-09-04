# coding:utf-8

from PIL import Image, ImageFilter, ImageEnhance
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'E:/Program Files/Tesseract-OCR/tesseract'


def get_kaptcha():
    im = Image.open("kaptcha.jpg")
    im = im.convert('L')
    v_code = pytesseract.image_to_string(im,config='-psm 6 digits')
    return v_code
# print(v_code)

