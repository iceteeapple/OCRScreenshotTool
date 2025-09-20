import os
import shutil
import cv2
import pytesseract
import datetime
from pytesseract import Output
from reportlab.pdfgen import canvas
from PIL import Image
#hallo
def copy_to_dynamic_folder(imagepath, folder_name,nameliststring,namelist, text_data, textFile):
    try:
        target_folder = os.path.join(Zielordner, folder_name)
        os.makedirs(target_folder, exist_ok=True)  # Ordner erstellen, wenn er noch nicht existiert
        imagepath = markfile(imagepath, nameliststring) 
    except Exception as e: print("Beim markieren des Bildes ist ein Fehler aufgetreten.\n Exception: \n", e)    
    try:
        shutil.copy(imagepath, target_folder)    
        filename = os.path.basename(imagepath)
    except Exception as e: print("Beim kopieren des Bildes("+imagepath+ ") in den ZielOrdner("+ target_folder +") ist ein Fehler aufgetreten\n Exception: \n", e )

    try:
        if textFile:
            pdfpathpart = os.path.join(target_folder,filename)
            pdfpath = pdfpathpart + '.pdf'
            
            img = Image.open(imagepath)
            img_width, img_height = img.size 

            img_height = img_height *1.6
            img_width = img_width *1.6
            # PDF erstellen
            c = canvas.Canvas(pdfpath, pagesize=(img_width, img_height))
            c.drawImage(imagepath, 0, 0, width=img_width , height=img_height)
            c.setKeywords(namelist)
            # Text und Positionen einfügen
            for i, word in enumerate(text_data['text']):
                if word.strip():  # Ignoriere leere Wörter
                    x = text_data['left'][i]
                    y = img_height - text_data['top'][i]  # Koordinaten umkehren, da y bei reportlab von unten nach oben wächst
                    
                    
                    c.setFont("Helvetica", 0.1)
                    c.drawString(x, y, word)
            c.save()
    
            print(imagepath + " -> " + folder_name)
    except Exception as e: print("Beim erstellen der PDF für "+ pdfpath + "ist ein Fehler aufgetreten\n Exception: \n", e)           
    return imagepath
def erstelleOrdner():
    try:
        # Pfad zur Textdatei
        dateipfad = 'erweiterung.txt'

        # Verzeichnis, in dem die Ordner erstellt werden sollen
        zielverzeichnis = 'Zielordner/'

        # Erstelle das Zielverzeichnis, falls es nicht existiert
        if not os.path.exists(zielverzeichnis):
            os.makedirs(zielverzeichnis)

        # Lese die Wörter aus der Textdatei
        with open(dateipfad, 'r', encoding='utf-8') as datei:
            woerter = datei.read().splitlines()

        # Erstelle für jedes Wort einen Ordner
        for wort in woerter:
            ordnerpfad = os.path.join(zielverzeichnis, wort)
            if not os.path.exists(ordnerpfad):
                os.makedirs(ordnerpfad)
                print(f'Ordner "{wort}" wurde erstellt.')
            else:
                print(f'Ordner "{wort}" existiert bereits.')
    
        print('Ordner erstellt!')
    except Exception as e: print("eim Anlegen neuer Ordner ist ein Fehler aufgetreten \n Exception: \n", e)

def markfile(imagepath,folder_name):
    filename, file_extension = os.path.splitext(imagepath)
    lastTwoLetters = filename[-2:]

    if str(lastTwoLetters) != markierung:
        filename, file_extension = os.path.splitext(imagepath)
        newfilename = filename +"_"+ folder_name+ markierung
        os.rename(imagepath, newfilename + file_extension)
        imagepath = os.path.join(newfilename + file_extension) 
    return imagepath

def isnotmarkedbool(imagepath):
     filename, file_extension = os.path.splitext(imagepath)
     lastTwoLetters = filename[-2:]
     if(lastTwoLetters == ("_S")):
        return False
     else:
         return True
     
# Ordner definieren
BilderOrdner = "BilderOrdner/"  # Pfad zu dem Ordner mit den Bilddateien
Zielordner = "Zielordner/"
bool = input("Möchtest du zu den im ZielOrdner liegenden Usernamen-Ordner weitere hinzufügen? Dann gib j ein und drücke Enter: ")
if bool == "j":
    print("Leg auf der Ordnerebene dieses Skripts eine Datei 'erweiterung.txt' an schreibe die Ordner, die du zusätzlich erstellen möchtest, untereinander in die Liste.")
    input("Drücke Enter, wenn du die Liste erstellt hast.")
    erstelleOrdner()

textFilebool = input("Möchtest du, dass neben deinen sortierten Bildern PDF-Dateien liegen, in welchen der Textinhalt des Bildes gespeichert ist? Dann gebe 'j' ein und drücke Enter: \n")
if textFilebool == 'j':
    textFile = True
else:
    textFile=False

markierung = "_S"

# Unterstützte Bildformate
image_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')

wordlist = [name for name in os.listdir(Zielordner) if os.path.isdir(os.path.join(Zielordner, name))]
print(wordlist)
with open('wordlist.txt', 'w') as file:
    # Durch die Liste iterieren und jedes Wort in eine neue Zeile schreiben
    for word in wordlist:
        file.write(word + '\n')

wordlist_path = 'wordlist.txt'
search_terms = wordlist
# Tesseract-Optionen setzen, um die Wortliste zu nutzen
#myconfigs = []
# myconfigs.append(f'-l deu+eng --user-words {wordlist_path} --oem 1 --psm 11 -c load_system_dawg=false -c load_freq_dawg=false -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789._')
#myconfigs.append(f'-l deu+eng --user-words {wordlist_path} --oem 3 --psm 11 -c load_system_dawg=false -c load_freq_dawg=false -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789._')
#myconfigs.append(f'-l deu+eng --user-words {wordlist_path} --oem 3 --psm 3 -c load_system_dawg=false -c load_freq_dawg=false -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789._')
config = f'-l deu+eng --user-words {wordlist_path} --oem 3 --psm 11 -c load_system_dawg=false -c load_freq_dawg=false -c tessedit_char_whitelist=abcdefghijklmnopqrstuvwxyz0123456789._'
i = 0
contrastconfigs = [2,4]
brightnessconfigs = [7,30]
# scaleconfig = [180,160,180]
print(datetime.datetime.now())

for cconfig in contrastconfigs:   
    # Durch alle Bilddateien im Ordner durchlaufen
    for image_file in sorted(os.listdir(BilderOrdner)):
        if image_file.lower().endswith(image_formats) and isnotmarkedbool(image_file):
           
            try:
                imagepath = os.path.join(BilderOrdner, image_file)

                img = cv2.imread(imagepath)

                scale_percent = 160      
                width = int(img.shape[1] * scale_percent / 100)
                height = int(img.shape[0] * scale_percent / 100)
            
                # Dsize
                dsize = (width, height)
                img = cv2.resize(img,dsize)

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                image = gray

                invert = cv2.bitwise_not(gray)
                image = invert

                alpha = contrastconfigs[i] # Contrast control
                beta = brightnessconfigs[i]   # Brightness control
                adjusted = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
                img = adjusted   
            except Exception as e: print("Beim Vorberiten von " + imagepath + " ist ein Fehler aufgetreten das Bild wird Übersprungen.\n Exception: \n", e)

    

            namelist = []
            try:
                textInPicture = pytesseract.image_to_string(img, config=config)  
                for term in search_terms:
                    if term in textInPicture:
                        namelist.append(term)
                        data = pytesseract.image_to_data(img,output_type=Output.DICT)
                    # imagepath = copy_to_dynamic_folder(imagepath, term, data, textFile)
                        # Tesseract OCR durchführen
                

                invert = cv2.bitwise_not(img)
                img = invert

                textInPicture = pytesseract.image_to_string(img, config=config)                            

                for term in search_terms:
                    if (term in textInPicture) and (term not in namelist):
                        namelist.append(term)
                        data = pytesseract.image_to_data(img,output_type=Output.DICT)
                    #  imagepath = copy_to_dynamic_folder(imagepath, term, data, textFile )
                nameliststring = ""
                for name in namelist:
                    nameliststring = nameliststring + "-" + name
                for term in namelist:
                    if term != "":
                        imagepath = copy_to_dynamic_folder(imagepath, term, nameliststring, namelist, data, textFile)
            except Exception as e: print("Beim durchsuchen des Bildes ist ein Fehler aufgetreten. \n Exception: \n", e)             
        


    i = i+1
    print("Vorgang " ,i, " abgeschlossen.") 

print(datetime.datetime.now())    
print("Bilder wurden sortiert :)")
