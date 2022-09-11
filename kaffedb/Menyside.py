#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#Importerer nødvendige biblotek for å koble til databasefilen
import sqlite3

#Finner riktig dato for kaffesmaking
from datetime import date
today = date.today()
dagensdato = today.strftime("%d%m%Y")
print(dagensdato)

#Åpner databasefilen vår "KaffeDB.db"
data = sqlite3.connect('KaffeDB.db')
cursor = data.cursor()

#Funksjon for å utføre brukerhistorie 1
def brukerhistorie1():
    #Innlogget som bruker med brukerID = 4
    brukerID = 1
    print("\nDu har gjennomført en ny kaffesmaking og skal nå legge inn en vurdering!\n")

    cursor.execute("SELECT Brennerinavn FROM Kaffebrenneri")
    brenneriliste = cursor.fetchall() 

    #Skriver en liste med alle brennerinavnene4
    number = 0
    for i in brenneriliste: 
        print(number + 1, ": ", i[0])
        number += 1

    brenneriid = int(input("Velg brenneri: ")) #Input fra brukeren

    #Finner alle kaffene som er laget av brenneriet som brukeren har valgt
    cursor.execute('''
                    SELECT Kaffenavn, KaffeID FROM Kaffe
                    INNER JOIN Kaffebrenneri ON Kaffe.BrenneriID = Kaffebrenneri.BrenneriID
                    WHERE Kaffebrenneri.BrenneriID = :brenneriid''', {"brenneriid":brenneriid})
    kaffeliste = cursor.fetchall()

    print("")
    kaffeider = [] #Lager en liste som skal inneholde alle kaffeid-ene til kaffene fra valgt brenneri
    number = 0
    for i in kaffeliste: #Skriver ut en liste over alle kaffene som er tilknyttet brenneriet
        print(number + 1, ": ", i[0])
        kaffeider.append(i[1]) #Legger kaffeiden inn i listen
        number += 1

    kaffenr = int(input("Velg kaffe fra det valgte brenneriet: ")) #Kaffe-input fra bruker
    kaffeid = kaffeider[kaffenr-1] #Finner riktig kaffeID fra inputtet av brukeren
    
    poeng = int(input("Poeng: "))
    smaksnotat = input("Smaksnotat: ")  

    #Setter inn verdier i tabellen
    cursor.execute("INSERT INTO Kaffesmaking VALUES ('{}', '{}', '{}', '{}', '{}')".format(brukerID, kaffeid, smaksnotat, poeng, dagensdato))
    cursor.execute("SELECT * FROM Kaffesmaking")
    allerader = cursor.fetchall()

    for x in allerader: 
        print(x)  #Printer ut alle kaffesmaking-instanser slik at man kan se om den er blitt lagt inn


#Funksjon for å utføre brukerhistorie 2
def brukerhistorie2():
    cursor.execute('''SELECT Bruker.Navn, count(*) AS NrUnikeKaffer
                FROM Bruker 
                JOIN Kaffesmaking ON Bruker.BrukerID = Kaffesmaking.BrukerID
                JOIN Kaffe ON Kaffe.KaffeID = Kaffesmaking.KaffeID
                WHERE Kaffesmaking.Smaksdato LIKE "%2022"
                GROUP BY Bruker.BrukerID
                ORDER BY NrUnikeKaffer DESC
                ''')
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    print()

#Funksjon for å utføre brukerhistorie 3
def brukerhistorie3():
    cursor.execute('''SELECT Kaffebrenneri.Brennerinavn, Kaffe.Kaffenavn, Kaffe.Kilopris, round(avg(Poeng), 2)
        FROM Kaffe JOIN Kaffesmaking JOIN Kaffebrenneri
        WHERE Kaffe.kaffeID = Kaffesmaking.KaffeID AND Kaffebrenneri.BrenneriID = Kaffe.BrenneriID
        GROUP BY Kaffe.KaffeID 
        ORDER BY avg(Poeng)/Kaffe.Kilopris DESC''')

    rows = cursor.fetchall()

    for row in rows:
        print(row)
    print()


#Funksjon for å utføre brukerhistorie 4
def brukerhistorie4():
    search = input("\nSkriv inn et søkeord: ")
    search_upper = search.upper()

    cursor.execute('''
                    SELECT DISTINCT Kaffebrenneri.Brennerinavn, Kaffe.Kaffenavn FROM Kaffe
                    INNER JOIN Kaffebrenneri ON Kaffe.BrenneriID = Kaffebrenneri.BrenneriID
                    INNER JOIN Kaffesmaking ON Kaffe.KaffeID = Kaffesmaking.KaffeID
                    WHERE (UPPER(Kaffesmaking.Notat) LIKE ? OR
                    UPPER(Kaffe.Beskrivelse) LIKE ?)
                    ORDER BY Kaffebrenneri.Brennerinavn DESC, Kaffe.Kaffenavn DESC''', ("%" + search_upper + "%", "%" + search_upper + "%"))
    rows = cursor.fetchall()

    for row in rows:
        print(row)
    print()

#Funksjon for å utføre brukerhistorie 5
def brukerhistorie5():
    cursor.execute('''SELECT Kaffebrenneri.Brennerinavn, Kaffe.Kaffenavn
                    FROM Kaffebrenneri
                    JOIN Kaffe ON Kaffebrenneri.BrenneriID = Kaffe.BrenneriID
                    JOIN Parti ON Kaffe.PartiID = Parti.PartiID
                    JOIN Foredlingsmetode ON Foredlingsmetode.Fnavn = Parti.Fnavn
                    JOIN Kaffegard ON Kaffegard.GårdID = Parti.GårdID
                    WHERE Foredlingsmetode.Fnavn NOT LIKE "vasket" AND 
                    (Kaffegard.Land LIKE 'Rwanda' OR KaffeGard.Land LIKE 'Colombia') 
                    ORDER BY Brennerinavn ASC, Kaffenavn ASC
                    ''')

    rows = cursor.fetchall()

    for row in rows:
        print(row)
    print()


#Lager en meny slik at man kan printe ut svaret for de ulike brukerhistoriene
answer = True
print("Velkommen til menyen! Du kan velge mellom følgende alternativer:")
print ("""
        1. Brukerhistorie 1
        2. Brukerhistorie 2
        3. Brukerhistorie 3
        4. Brukerhistorie 4
        5. Brukerhistorie 5
        6. Exit
        """)

while answer:
    answer = input("Skriv inn tall på ønsket brukerhistorie (1-5) eller exit (6): ")

    if answer == "1": 
        brukerhistorie1()

    elif answer == "2":
        print("\nListe av navn på brukere som har smakt flest unike kaffer i 2022")
        brukerhistorie2()

    elif answer == "3":
        print("Liste med brennerinavn, kaffenavn, pris og gjennomsnittsscore kontra pris for hver kaffe).")
        brukerhistorie3()

    elif answer == "4":
        print("\nListe med brennerinavn og kaffenavn på kaffer som er blitt beskrevet med søkeordet")
        brukerhistorie4()

    elif answer == "5":
        print("Liste med brennerinavn og kaffenavn på kaffer som ikke er vasket og kommer fra enten Rwanda eller Colombia")
        brukerhistorie5()

    elif answer == "6":
        print("\nHadet!") 
        answer = None

    else:
        print("Det du skrev er ikke godkjent.") 

#Lukker databasen
data.commit()
data.close()