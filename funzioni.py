from fpdf import FPDF
import os
import requests
from bs4 import BeautifulSoup
from PIL import Image
import colorama

def progress_bar(progress , total , prefix):
    percent = 100 * (progress / float(total))
    bar = '█' * int(percent) + '-' * (100 - int(percent))
    color = colorama.Fore.YELLOW
    if percent < 50 :
        print(colorama.Fore.RED + f"\r{prefix} |{bar}| {percent:.2f}%", end="\r")
    else:
        print(color + f"\r{prefix} |{bar}| {percent:.2f}%", end="\r")
    if progress == total:
        print(colorama.Fore.GREEN + f"\r{prefix} |{bar}| {percent:.2f}%", end="\r")

def extract_integer(filename):
    return int(filename.split('.')[0].split("_")[1])

def create_pdf(path, file_name):
    dir = sorted(os.listdir(path), key=extract_integer)

    pdf = FPDF(unit='mm')

    pdf.set_image_filter("DCTDecode")
    
    bar = ""
    for i in range(len(dir)):
        bar += " "

    bar = list(bar)

    i = 1
    for f in dir:
        progress_bar(i , len(bar) , "Creando PDF:")
        i+=1
        img = Image.open(f"{path}/{f}")
        width , height = img.size
        width, height = float(width * 0.264583), float(height * 0.264583)
        pdf.add_page(format=(width, height))
        pdf.image(f"{path}/{f}" , 0, 0 ,width ,height)

    pdf.output(file_name)

def open_pdf(file_name):
    os.system(f"start {file_name}")

def cerca(name:str):
    
    params = (
        ('keyword', name),
    )

    response = requests.get('https://www.mangaworld.in/archive', params=params)

    with open('file/search.html', 'w', encoding="utf-8") as f:
            f.write(response.text)

    with open('file/search.html','r' ,encoding="utf-8") as f:
            content = f.read()

    soup = BeautifulSoup(content,'html.parser')

    a_tag = soup.find_all("a", class_="manga-title")

    all = []
    for link in a_tag:
        href = link["href"]
        title = link["title"]
        # print(f"{title.upper()}: {href}")
        all.append({title:href})

    return all

def sel_cap(url:str):
    response = requests.get(url)

    with open("file/sel.html","w",encoding="utf-8") as f:
        f.write(response.text)

    with open("file/sel.html","r",encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content , "html.parser")

    div_tag = soup.find_all("div", class_="chapter")

    all = []
    for link in div_tag:
        href = link.a["href"]
        # print(f"{title.upper()}: {href}")
        all.append(href)

    return all

def get_fot(url:str):
    response = requests.get(url)

    with open("file/chapter.html","w",encoding="utf-8") as f:
        f.write(response.text)

    with open("file/chapter.html","r",encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    div = soup.find_all("div", id="page")

    img = div[0].img["src"]

    return img

def remove_non_alp(s:str):
    final = ""
    for c in s:
        if c.isalnum():
            final += c
        else:
            final += "_"

    return final