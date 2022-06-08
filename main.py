import requests
from bs4 import BeautifulSoup
import shutil
from funzioni import *
import os
import colorama
from winotify import Notification

def download_page(response, path , index):
    if response.status_code == 200:
        with  open(f"{path}/page_{index}.png", "wb") as f:
            shutil.copyfileobj(response.raw, f)

def select_episode(url_split, index):
    url_split[-1] = f"{index}.{url_split[-1].split('.')[-1]}"

    url = ""
    for element in url_split:
        url += element+"/"
    
    finale = ""
    for i in range(len(url)):
        if(i < len(url)-1):
            finale += url[i]
    
    return finale

def count_pages(img):
    url_fot = img
    sp = url_fot.split("/")
    response = requests.get(select_episode(sp,1) ,stream = True)
    np = 0
    i = 1 
    while response.status_code == 200:
        np+=1
        response = requests.get(select_episode(sp,i) ,stream = True)
        i+=1

    return np
    


def download(name , chapter , img ):
    if not os.path.exists(name+"_"+chapter):
        os.mkdir(name+"_"+chapter)

    url_fot = img
    sp = url_fot.split("/")
    response = requests.get(select_episode(sp,1) ,stream = True)

    total = count_pages(img)

    i = 1
    while True:
        if response.status_code == 200:
            response = requests.get(select_episode(sp,i) ,stream = True)        
            progress_bar(i , total, "Downloading:")
            download_page(response, name+"_"+chapter ,i)
            i+=1
        else: 
            print()
            break
        
    if not os.path.exists(f"manga/{name}"):
        os.mkdir(f"manga/{name}")

    file_name = f"manga/{name}/{chapter}.pdf"
    
    create_pdf(name+"_"+chapter,file_name)
    
    toast = Notification(app_id = "Manga",
                    title= "Manga scaricato",
                    msg = name+"_"+chapter+" scaricato",
                    duration = "long")
    toast.show()

    shutil.rmtree(name+"_"+chapter)#cancella

def main():

    lista_manga = []

    while len(lista_manga) < 1:

        name = input("Cerca manga: ")
        lista_manga = cerca(name)
        
        for i in range(len(lista_manga)):
            manga = lista_manga[i]
            for title in manga:
                print(f"{i} : {title}")
        print()
        
        number = int(input("selezionare manga: "))

        manga_sel = lista_manga[number]

        for link in manga_sel:
            manga_name = link
            link = manga_sel[link]

        capitoli = sel_cap(link)
        capitolo = ""

        com = ""
        number_cap = 0
        while com != "n":
            if number_cap+1 >= 0 and number_cap-1 < len(capitoli):
                
                if capitolo == "":
                    number_cap = input(f"inserire capitolo , [r] scaricare manga in range , range(0-{len(capitoli)-1}) : ")
                    if number_cap != "r":
                        number_cap = int(number_cap)
                        capitolo = capitoli[-number_cap-1]
                        manga_name = remove_non_alp(manga_name)
                        img = get_fot(capitolo)
                        download(manga_name , f"capitolo_{number_cap}", img)
                        print(colorama.Fore.RESET)
                    else:
                        inizio = int(input("inserire inizio range: "))
                        fine = int(input("inserire fine range: "))
                        for i in range(inizio,fine+1):
                            number_cap = i
                            capitolo = capitoli[-number_cap-1]
                            manga_name = remove_non_alp(manga_name)
                            img = get_fot(capitolo)
                            download(manga_name , f"capitolo_{number_cap}", img)
                        print(colorama.Fore.RESET)


                com = input("\n[p] per scaricare un altro capitolo \n[n] per cercare manga \n[a] per aprire capitolo \n[q] per uscire \ninserisci: ")
                if com == "p":
                    capitolo = ""
                if com == "n":
                    lista_manga = []
                if com == "a":
                    file_name = f"manga/{manga_name}/capitolo_{number_cap}.pdf"
                    open_pdf(file_name)
                if com == "q":
                    quit()
            else:
                print("non trovato")
                break

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        quit()