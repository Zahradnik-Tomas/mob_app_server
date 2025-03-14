import sys

from db_lib import DB_handler


def clear():
    print("\033c", end='')


db = DB_handler()
cekajici = []
vzitZDB = True

while True:
    # clear()
    if vzitZDB:
        cekajici = db.VratCekajici()
        vzitZDB = False
    print("List čekajících:")
    for i in range(len(cekajici)):
        print(f"{i + 1} {cekajici[i][1]}")
    print("")
    print("r - načíst znovu")
    print("q - odejít")
    print("d - všechny smazat")
    print("e - smazat specifického (např. e 2 nebo e 2, 4, 5)")
    inp = input("číslo - potvrdit: ")
    if len(inp) == 0:
        continue
    if inp[0] == "r":
        vzitZDB = True
        continue
    elif inp[0] == "q":
        sys.exit()
    elif inp[0] == "d":
        db.SmazVsechnyCekajici()
        vzitZDB = True
        continue
    elif inp[0] == "e":
        temp = inp[1:]
        cisla = temp.split(",")
        for cislo in cisla:
            if cislo.replace(" ", "").isnumeric() and int(cislo) - 1 < len(cekajici):
                db.SmazCekajiciho(cekajici[int(cislo.replace(" ", "")) - 1][0])
                vzitZDB = True
        continue
    cisla = inp.split(",")
    for cislo in cisla:
        if cislo.replace(" ", "").isnumeric() and int(cislo) - 1 < len(cekajici):
            db.PotvrdCekajiciho(cekajici[int(cislo.replace(" ", "")) - 1][0])
            vzitZDB = True
