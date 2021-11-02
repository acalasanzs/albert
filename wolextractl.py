import assgnopts
import random
from assgnopts import Assgn
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os

# span attrs={'class':'title ellipsized name'}
books = [['Génesis', 'Éxodo', 'Levítico', 'Números', 'Deuteronomio', 'Josué', 'Jueces', 'Rut', '1 Samuel', '2 Samuel', '1 Reyes', '2 Reyes', '1 Crónicas', '2 Crónicas', 'Esdras', 'Nehemías', 'Ester', 'Job', 'Salmos', 'Proverbios', 'Eclesiastés', 'El Cantar de los Cantares', 'Isaías', 'Jeremías', 'Lamentaciones', 'Ezequiel', 'Daniel', 'Oseas', 'Joel', 'Amós', 'Abdías', 'Jonás', 'Miqueas', 'Nahúm', 'Habacuc', 'Sofonías', 'Ageo', 'Zacarías', 'Malaquías', 'Mateo', 'Marcos', 'Lucas', 'Juan', 'Hechos', 'Romanos', '1 Corintios', '2 Corintios', 'Gálatas', 'Efesios', 'Filipenses', 'Colosenses', '1 Tesalonicenses', '2 Tesalonicenses', '1 Timoteo', '2 Timoteo', 'Tito', 'Filemón', 'Hebreos', 'Santiago', '1 Pedro', '2 Pedro', '1 Juan', '2 Juan', '3 Juan', 'Judas', 'Apocalipsis'],['Genesis', 'Exodus', 'Leviticus', 'Numbers', 'Deuteronomy', 'Joshua', 'Judges', 'Ruth', '1 Samuel', '2 Samuel', '1 Kings', '2 Kings', '1 Chronicles', '2 Chronicles', 'Ezra', 'Nehemiah', 'Esther', 'Job', 'Psalms', 'Proverbs', 'Ecclesiastes', 'Song of Solomon', 'Isaiah', 'Jeremiah', 'Lamentations', 'Ezekiel', 'Daniel', 'Hosea', 'Joel', 'Amos', 'Obadiah', 'Jonah', 'Micah', 'Nahum', 'Habakkuk', 'Zephaniah', 'Haggai', 'Zechariah', 'Malachi', 'Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation'],['Mateu', 'Marc', 'Lluc', 'Joan', 'Fets', 'Romans', '1 Corintis', '2 Corintis', 'Gàlates', 'Efesis', 'Filipencs', 'Colossencs', '1 Tessalonicencs', '2 Tessalonicencs', '1 Timoteu', '2 Timoteu', 'Titus', 'Filemó', 'Hebreus', 'Jaume', '1 Pere', '2 Pere', '1 Joan', '2 Joan', '3 Joan', 'Judes', 'Apocalipsi']]
url = ['https://wol.jw.org/es/wol/publication/r4/lp-s/nwt','https://wol.jw.org/en/wol/publication/r1/lp-e/nwt','https://wol.jw.org/cat/wol/publication/r55/lp-an/bi7']
indexname = ["Índices","Indexes","Índexs"]
def Inputs():
    language = Assgn(['Language (0 Spanish,1 English,2 Catalan)'],vals=range(3),rules=[True,False,True])
    language.input()
    language = language.ans

    cbook = Assgn(['Book'],vals=books[language])
    print(", ".join(cbook.vals))
    cbook.input()
    cbook = cbook.ans
    chapter = Assgn(["Chaper"],rules=[False,False,True])
    chapter.input()
    verse = Assgn(["Verse (if 0: random verse)"],rules=[True,False,True])
    verse.input()
    if verse.ans == 0:
        verse = 999
    else:
        verse = verse.ans
    return language, cbook, chapter.ans, verse
def DefaultInputs():
    language = 1
    cbook = "Proverbs"
    chapter = 11
    verse = 0
    return language, cbook, chapter, verse
def Scrap(language,cbook,chapter,verse=None):
    book_chosen = cbook
    chapter_chosen = chapter
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-notifications")
    options.add_argument("disable-infobars")
    # Crear una sesión de Chrome
    driver = webdriver.Chrome('/usr/local/bin/chromedriver',options=options)
    driver.implicitly_wait(30)
    driver.maximize_window()

    # Acceder a la aplicación web
    driver.get(url[language])
    driver.implicitly_wait(800)
    try:
        #Accept cookies
        driver.find_element(By.CSS_SELECTOR,".legal-notices-client--accept-button").click()
    except:
        pass #No cookies
    # Localizar cuadro de texto
    cbook = driver.find_element(By.XPATH, '//span[text()="{0}"]'.format(cbook))
    driver.execute_script("window.scrollBy(0,{0})".format(cbook.location["y"]+150))
    cbook.click()
    driver.implicitly_wait(1000)
    last = driver.find_elements(By.TAG_NAME,"li")
    lastest = max([int(i) if i.isnumeric() else 0 for i in [x.text for x in last]])
    if lastest < chapter:
        driver.quit()
        print(assgnopts.color.b.red,"Invalid chapter",assgnopts.color.end)
    chapter = driver.find_element(By.XPATH, '//*[text()="{0}"]'.format(str(chapter)))
    driver.execute_script("window.scrollBy(0,{0})".format(chapter.location["y"]-100))
    chapter.click()
    if language == 2:
        verses = driver.find_elements(By.CSS_SELECTOR,".tt")
    else:
        verses = driver.find_elements(By.CSS_SELECTOR,".vp")
    chosen = verse
    if verse is None:
        chosen = random.choice(range(chosen+1))
        chosen = verses[verse]
    else:
        chosen = verse if verse in list(range(chosen+1)) else random.choice(range(chosen+1))
        if chosen != verse:
            print(assgnopts.color.b.red,"Invalid verse, but random chosen instead",assgnopts.color.end)
        try:
            chosen = verses[verse-1]
        except IndexError:
            chosen = random.choice(verses)
        print(chosen.text)
    driver.execute_script("window.scrollBy(0,{0})".format(chosen.location["y"]-150))
    chosen.click()
    driver.implicitly_wait(30)
    nav = driver.find_element_by_class_name("navigationContents")
    indexes = nav.find_elements(By.XPATH, '//span[text()="{0}"]'.format(indexname[language]))
    availableI = []
    available = False
    available_chosen = None
    for j in indexes:
        availableI.append(j.find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_element(By.CLASS_NAME,"scalableui").text)
    for i in availableI:
        try:
            if int(i.split(":")[1]) == verse:
                available = True
                break
        except IndexError:
            if int(i.split(" ")[1]) == verse:
                available = True
                break
    if available:
        print(assgnopts.color.b.green,"Chosen verse is vailable on indices",assgnopts.color.end)
        available_chosen = book_chosen+" "+str(chapter_chosen)+":"+str(verse)
    else:
        print(assgnopts.color.b.purple,"Sorry, verse is not available on indeces",assgnopts.color.end)
        print(assgnopts.color.b.green,"We'll choose one random instead",assgnopts.color.end)
        for k in availableI:
            print(k)
        available_chosen = random.choice(availableI)
        try:
            print("Verse chosen:",int(available_chosen.split(":")[1]))
        except IndexError:
            print("Verse chosen:",int(available_chosen.split(" ")[1]))
    try:
        current_index = availableI.index(available_chosen)
    except:
        available_chosen = book_chosen+" "+str(verse)
        current_index = availableI.index(available_chosen)
    indexes[current_index].click()
    random_link = random.choice(indexes[current_index].find_element_by_xpath('..').find_element_by_xpath('..').find_element_by_xpath('..').find_elements(By.TAG_NAME,"a"))
    print(random_link.text)

    driver.get(random_link.get_attribute('href'))
    html = driver.page_source
    soup = BeautifulSoup(html)
    try:
        info = soup.find_all("p", {"class": "h1"})
        assert info.text is not None
        total = ""
        for element in info:
            total += element.text
        print(total)
        with open('info.txt', 'wb') as f:
            f.write(available_chosen.encode(encoding='UTF-8',errors='strict')+"\n".encode(encoding='UTF-8',errors='strict')+total.encode(encoding='UTF-8',errors='strict'))
        driver.quit()
    except:
        info = soup.find_all("p", {"class": "sb"})
        total = ""
        for element in info:
            total += element.text
        print(total)
        with open('info.txt', 'wb') as f:
            f.write(available_chosen.encode(encoding='UTF-8',errors='strict')+"\n".encode(encoding='UTF-8',errors='strict')+total.encode(encoding='UTF-8',errors='strict'))
        driver.quit()
if __name__ == "__main__":
    Scrap(*Inputs())
    os.system("pause")
    #Scrap(*DefaultInputs())