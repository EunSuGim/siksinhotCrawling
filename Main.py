#Main.py
from Search import *
from Parsing import *
from DBConnect import *

if __name__ == "__main__" :

    s = Search()
    p = Parsing()
    db = DBConnect()

    restaurantsInfo = s.searching()

    results = p.parsingInfo(restaurantsInfo)

    db.saveCsv(results)



