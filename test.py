from wolextract import Scrap,books
import random
from assgnopts import Assgn

lang = 1
book = random.choice(books[lang])
with open('random.txt', 'wb') as f:
    for x in books:
        pt = Scrap(lang,book,999,0)
        pt = pt[0]+"\n"+pt[1]
        f.write(pt.encode(encoding='UTF-8',errors='strict'))
        f.write("\n")