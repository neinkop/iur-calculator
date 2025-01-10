from DynamischeInvestitionsrechnung import *
from StatischeInvestitionsrechnung import *

dyn_ips = []
stat_ips = []

def zurueck_hauptmenu():
    option = str(input("Gebe z ein um zurück in Hauptmenü zu gelangen: "))
    if option == "z":
        start()

def dyn_cashflows(laufzeit):
    """Fragt den User nach Cashflows des Investitionsprojektes ab

    Args:
        laufzeit (type): Lauzeit des Investitionsprojektes

    Returns:
        list: Liste mit allen Cashflows je Jahr
    """
    jahr = 1 # Conuter
    cashflows = [float] * laufzeit # Deklarieren der Cashflow-List
    while (jahr <= laufzeit): # Algorithmus um für jedes Jahr einen Cashflow zu deklarieren
        cashflows[jahr-1] = float(input("Gebe den Cashflow des " + str(jahr) + ". Jahres ein: "))
        jahr = jahr + 1
    return cashflows

def dyn_abschreibung(laufzeit, anschaffungsauszahlung): 
    """Fragt den User nach Abschreibungen des Investitionsprojektes ab

    Args:
        laufzeit (type): Laufzeit des Investitionsprojektes
        anschaffungsauszahlung (type): Anschaffungsauszahlungen des Investitionsprojektes

    Returns:
        list: Liste mit allen Cashflows je Jahr
    """
    abschreibungen = [float] * laufzeit # Deklarieren der Liste mit allen Abschreibungswerten

    # Abfrage ob die Anschaffungskosten Linear abgeschrieben werden sollen
    abschreibung_input = str(input("Sollen die Anschaffungsauszahlungen linear abgeschrieben werden (ja): "))
    if abschreibung_input == "ja":
        jahr = 1
        while (jahr <= laufzeit):
            abschreibungen[jahr-1] = round(anschaffungsauszahlung/laufzeit, 2)
            jahr = jahr+1
    else:
        jahr = 1
        while (jahr <= laufzeit):
            abschreibungen[jahr-1] = round(float(input("Gebe die prozentuale Abschreibung des " + str(jahr) + ". Jahres ein (Beispiel: 0.05): ")), 2)
            jahr = jahr + 1
    return abschreibungen

def dyn_neues_projekt():
    """Fragt alle Daten des Users ab die zur berechnung des Dynamischen Investitionsprojektes benötigt werden

    Returns:
        DynamischeInvestitionsrechnung: Objekt der dynamischen Investitionsrechnung
    """
    # Abfrage des Projektnamens
    name = str(input("Gebe den Namen des Projektes ein: "))

    # Abfrage des Kalkulationszinsfußes
    kzf = float(input("Gebe den Kalkulationszinsfuß ein (Beispiel: 0.05 = 5%): "))
    while kzf > 1 or kzf <= 0:
        print("Der KZF darf nicht größer als 100% sein und muss über 0 liegen!")
        kzf = float(input("Gebe den Kalkulationszinsfuß ein (Beispiel: 0.05 = 5%): "))

    # Abfrage der Projektlaufzeit
    laufzeit = int(input("Gebe die Laufzeit des Projekts in ganzen Jahres ein: "))
    while laufzeit > 10 or laufzeit <= 0:
        print("Die Laufzeit darf nicht größer als 10 Jahre sein und muss über 0 liegen!")
        laufzeit = int(input("Gebe die Laufzeit des Projekts in ganzen Jahres ein: "))

    # Abfrage der Anschaffungsauszahlungen
    anschaffungsauszahlungen = float(input("Wie hoch sind die Anschaffungsauszahlungen: "))
    while anschaffungsauszahlungen <= 0:
        print("Die Anschaffungsauszahlungen dürfen nicht negativ oder gleich 0 sein!")
        anschaffungsauszahlungen = float(input("Wie hoch sind die Anschaffungsauszahlungen: "))
        
    # Abfrage der entscheidungsrelevanten Cashflows
    cashflows = dyn_cashflows(laufzeit)

    # Abfrage ob Etragssteuerzahlungen berücksichtigt werden sollen, deklalieren der Variablen
    steuern = False
    steuersatz = 0.0
    abschreibungen = []
    steuern_input = str(input("Sollen Ertragssteuern berücksichtigt werden (ja/nein): "))
    while steuern_input != "ja" and steuern_input != "nein":
        steuern_input = str(input("Sollen Ertragssteuern berücksichtigt werden (ja/nein): "))

    # Ausführen von Funktionen die nur Relevant sind für Projekte mit Steuerzahlungen
    if  steuern_input == "ja": 
        steuern = True
        abschreibungen = dyn_abschreibung(laufzeit, anschaffungsauszahlungen)
        steuersatz = float(input("Gebe den Ertragssteuersatz ein (Beispiel: 0.05): "))
    elif steuern_input == "nein":
        steuern = False

    # Deklarieren der Variablen        
    dynir = DynamischeInvestitionsrechnung(name, kzf, laufzeit, anschaffungsauszahlungen, cashflows, steuern, steuersatz, abschreibungen)

    # Berechnen der Kennzahlen
    print("Die Kennzahlen werden berechnet...")
    dynir.init()

    # Ausgabe der Berechneten Variablen
    print("--")
    print("Der Kapitalwert beträgt: " + str(dynir.kapitalwert()))
    print("Die Annuität beträgt: " + str(dynir.annuitaet()))
    print("Der Endwert beträgt: " + str(dynir.endwert()))
    print("Der Etragswert beträgt: " + str(dynir.etragswert()))
    print("Der Baldwin-Zinssatz beträgt: " + str(dynir.baldwin()) + "%")
    print("Der Interne Zinsfuß beträgt: " + str(dynir.izf()) + "%")
    print("Die dynamische Amortisationsdauer beträgt: " + str(dynir.amortisationsdauer()) + " Jahre")
    print("--")
    return dynir

def dyn_ir():
    """Führt den User durch das Menu der dynamischen Investitionsrechnung
    """
    # Ausgabe abhängig von der Anzahl der Projekte
    if len(dyn_ips) == 0:
        # Ausgabe wenn bisher keine Projekte angelegt wurden
        print("Derzeit sind keine Projekte angelegt.")
        print("1 - Neues Projekt anlegen")
        print("2 - Zurück zum Hauptmenu")

        # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
        option = int(input("Option: "))
        while option != 1 and option != 2:
            print("Nicht valide!")
            option = int(input("Option: "))

        if option == 1:
            dyn_ips.append(dyn_neues_projekt())
        elif option == 2:
            start()

    elif len(dyn_ips) > 0:
        print("Derzeit sind folgende Projekte angelegt:")

        count = 1
        for pr in dyn_ips:
            print(str(count) + " - " + pr.name())
            count = count + 1

        if int(len(dyn_ips)) > 1:
            # Ausgabe wenn mehr als ein Projekt existiert (Vergleichsfunktion!)
            print(str(len(dyn_ips)+1) + " - Projekte Vergleichen")
            print(str(len(dyn_ips)+2) + " - Neues Projekt anlegen")
            print(str(len(dyn_ips)+3) + " - Zurück ins Hauptmenu")
            print("")

            # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
            option = int(input("Wähle eine Option: "))
            while option > len(dyn_ips)+3 or option < 0:
                option = int(input("Wähle eine Option: "))

            if option == len(dyn_ips)+1:
                count = 1
                for pr in dyn_ips:
                    print(str(count) + " - " + pr.name())
                    count = count + 1

                # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
                projekt1 = int(input("Wähle das 1. Projekt: "))-1
                while projekt1 > len(dyn_ips)-1 or projekt1 < 0:
                    projekt1 = int(input("Wähle das 1. Projekt: "))-1

                # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
                projekt2 = int(input("Wähle das 2. Projekt: "))-1
                while projekt2 > (len(dyn_ips)-1) or projekt2 == projekt1 or projekt2 < 0:
                    projekt2 = int(input("Wähle das 2. Projekt: "))-1
                
                projekt1 = dyn_ips[projekt1]
                projekt2 = dyn_ips[projekt2]
                print("Projektvergleich: ")
                print(''+91*'-')
                print(f'{"Gewinn":^20} | {"Amortisation":^20} | {"EK-Rentabilität":^20} | {"GK-Rentabilität":^20}')
                print(91*'-')
                #print(f'{_Gewinn:^20} | {_Amortisation:^20} | {_EK_Rentabilität:^20} | {_GK_Rentabilität:^20}')
                print(91*'-')
                option = input("Tippe eine beliebige Taste um zurück ins Menu zugelangen: ")
            elif option == len(dyn_ips)+2:
                # Anlegen eines neuen Projektes
                dyn_ips.append(dyn_neues_projekt())
            elif option == len(dyn_ips)+3:
                # Zurück ins Hauptmenü
                start()
            elif 0  < option < int(len(dyn_ips))+1:
                dynir = dyn_ips[option-1]
        else: 
            # Ausgabe wenn nur ein Projekt angelegt wurde
            print(str(len(dyn_ips)+1) + " - Neues Projekt anlegen")
            print(str(len(dyn_ips)+2) + " - Zurück ins Hauptmenu")
            print("")

            # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
            option = int(input("Wähle eine Option: "))
            while option > len(dyn_ips)+2 or option < 0:
                option = int(input("Wähle eine Option: "))

            if option == len(dyn_ips)+1:
                # Anlegen eines neuen Projektes
                dyn_ips.append(dyn_neues_projekt())
            elif option == len(dyn_ips)+2:
                # Zurück ins Hauptmenü
                start()
            elif 0 < option < int(len(dyn_ips))+1:
                # Ausgabe des Projektes
                dynir = dyn_ips[option-1]
                print("--")
                print("Kapitalwert: " + str(dynir.kapitalwert()))
                print("Annuität: " + str(dynir.annuitaet()))
                print("Endwert: " + str(dynir.endwert()))
                print("Etragswert: " + str(dynir.etragswert()))
                print("Baldwin-Zinssatz: " + str(dynir.baldwin()) + "%")
                print("Interne Zinsfuß: " + str(dynir.izf()) + "%")
                print("Dynamische Amortisationsdauer: " + str(dynir.amortisationsdauer()) + " Jahre")
                print("--")
                dyn_ir()

    dyn_ir()

def stat_neues_projekt():
    """Fragt alle Daten des Users ab die zur berechnung des Statischen Investitionsprojektes benötigt werden

    Returns:
        StatischeInvestitionsrechnung: Objekt der statische Investitionsrechung
    """
    name = input('Gib den Namen des Projektes ein: ')
   
    #Abfrage Kalkulationszinsfuß
    kzf = float(input('Gebe den Kalkulationszinsfuß ein (Beispiel: 0.05 = 5%): '))
    while kzf > 1:
        print("Der KZF darf nicht größer als 100% sein!")
        kzf = float(input("Gebe den Kalkulationszinsfuß ein (Beispiel: 0.05 = 5%): "))
   
    #Abfrage Anschaffungsauszahlung    
    a0 = int(input('Wie hoch sind die Anschaffungskosten? -  '))
    while a0 < 0:
        print("Der Liquidationserlös darf nicht kleiner als 0 sein!")
        a0 = int(input('Wie hoch sind die Anschaffungskosten? -  '))
   
    #Abfrage Liquidationserlös
    l = int(input('Wie hoch ist der Liquidationserlös? (Wenn keiner vorhanden ist, 0 eintragen) - '))
    while l < 0:
        print("Der Liquidationserlös darf nicht kleiner als 0 sein!")
        l = int(input('Wie hoch ist der Liquidationserlös? (Wenn keiner vorhanden ist, 0 eintragen) - '))
   
    #Abfrage Laufzeit des Investitionsprojektes
    t = int(input("Gebe die Laufzeit des Projekts in ganzen Jahres ein: "))
    while t > 10:
        print("Die Laufzeit darf nicht größer als 10 Jahre sein!")
        t = int(input("Gebe die Laufzeit des Projekts in ganzen Jahres ein: "))
   
    #Abfrage Betriebskosten des IP (variable und fixe)
    bk = int(input('Wie hoch sind die Betriebskosten? (variable und fixe) - '))
    while bk < 0:
        print("Die Betriebskosten dürfen nicht kleiner als 0 sein!")
        bk = int(input('Wie hoch sind die Betriebskosten? (variable und fixe) - '))
        
    #Abfrage Umsatzerlös
    Erlöse = int(input('Wie hoch ist der Umsatzerlös? - '))
    while Erlöse < 0:
        print("Der Umsatzerlöse darf nicht kleiner als 0 sein!")
        Erlöse = int(input('Wie hoch ist der Umsatzerlös? - '))
        
    #Abfrage Art der durchschnittlichen Kapitalbindung
    KB_Art = int(input('Welche Art der durchschnittlichen Kapitalbindung soll bei der Berechnung verwendet werden? (1 - kontinuierliche Tilgung | 2 - Tilgung am Periodenende) - '))
    while 0 > KB_Art > 2:
        print("Ungültige Eingabe. Wähle eine der Optionen!")
        KB_Art = int(input('Welche Art der durchschnittlichen Kapitalbindung soll bei der Berechnung verwendet werden? (1 - kontinuierliche Tilgung | 2 - Tilgung am Periodenende) - '))
    
    #Abfrage Summe an aufgenommenem Fremdkapital
    Fk = int(input('Gib an wie viel Fremdkapital zur Fianzierung aufgenommen wurde (Wenn keins aufgenommen wurde, 0 eingeben) - '))
    while Fk < 0:
        print("Das Fremdkapital darf nicht kleiner als 0 sein!")
        Fk = int(input('Gib an wie viel Fremdkapital zur Fianzierung aufgenommen wurde (Wenn keins aufgenommen wurde, 0 eingeben) - '))
    
    #Abfrage Fremdkapitalzins
    if Fk != 0: 
        Fk_zins = float(input('Zu welchem Zinssatz wurde das Fremdkapital aufgenommen? (Beispiel: 0.05 = 5%) - '))
        while Fk_zins > 1:
            print("Der Zinssatz darf nicht größer als 100% sein!")
            Fk_zins = float(input('Zu welchem Zinssatz wurde das Fremdkapital aufgenommen? (Beispiel: 0.05 = 5%) - '))
        
    #Erzeugung neues Objekt der Klasse StatischeInvestitionsrechnung
    name = StatischeInvestitionsrechnung(name, kzf, a0, l, t, bk, Erlöse, KB_Art, Fk, Fk_zins)
    
    #Berechnung Kennzahlung und Speicherung als Attribute des erzeugten Objektes
    name._Gewinn = name.stat_Gewinn() 
    name._Amortisation = name.stat_Amortisation()
    name._GK_Rentabilität, name._EK_Rentabilität = name.stat_Rentabilität()
    
    #Ausgabe der Kennzahlen
    name.print_Kennzahlen()
    
    return name
    
def stat_ir():
    """Führt den User durch das Menu der dynamischen Investitionsrechnung
    """
    # Ausgabe abhängig von der Anzahl der Projekte
    if len(stat_ips) == 0:
        # Ausgabe wenn bisher keine Projekte angelegt wurden
        print("Derzeit sind keine Projekte angelegt.")
        print("1 - Neues Projekt anlegen")
        print("2 - Zurück zum Hauptmenu")
        
        # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
        option = int(input("Option: "))
        while option != 1 and option != 2:
            print("Nicht valide!")
            option = int(input("Option: "))

        if option == 1:
            stat_ips.append(stat_neues_projekt())
        elif option == 2:
            start()

    elif len(stat_ips) > 0:
        print("Derzeit sind folgende Projekte angelegt:")

        count = 1
        for pr in stat_ips:
            print(str(count) + " - " + str(pr.get_name()))
            count = count + 1
            
        if len(stat_ips) > 1:
            # Ausgabe wenn mehr als ein Projekt existiert (Vergleichsfunktion!)
            print(str(len(stat_ips)+1) + " - Projekte Vergleichen")
            print(str(len(stat_ips)+2) + " - Neues Projekt anlegen")
            print(str(len(stat_ips)+3) + " - Zurück ins Hauptmenu")
            print("")
            
            # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
            option = int(input("Wähle eine Option: "))
            while option > len(stat_ips)+3 or option < 0:
                option = int(input("Wähle eine Option: "))

            if option == len(stat_ips)+1:
                count = 1
                for pr in stat_ips:
                    print(str(count) + " - " + str(pr.get_name()))
                    count = count + 1
                
                # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
                projekt1 = int(input("Wähle das 1. Projekt: "))-1
                while projekt1 > len(stat_ips)-1 or projekt1 < 0:
                    projekt1 = int(input("Wähle das 1. Projekt: "))-1

                # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
                projekt2 = int(input("Wähle das 2. Projekt: "))-1
                while projekt2 > (len(stat_ips)-1) or projekt2 == projekt1 or projekt2 < 0:
                    projekt2 = int(input("Wähle das 2. Projekt: "))-1
                print("Projektvergleich: ")
                stat_ips[projekt1].print_Kennzahlen()
                print('')
                stat_ips[projekt2].print_Kennzahlen()
                option = input("Tippe eine Beliebige Taste um zurück ins Menu zugelangen: ")
            elif option == len(stat_ips)+2:
                # Anlegen eines neuen Projektes
                stat_ips.append(stat_neues_projekt())
            elif option == len(stat_ips)+3:
                # Zurück ins Hauptmenü
                start()
        else: 
            # Ausgabe wenn nur ein Projekt angelegt wurde
            print(str(len(stat_ips)+1) + " - Neues Projekt anlegen")
            print(str(len(stat_ips)+2) + " - Zurück ins Hauptmenu")
            print("")
            
            # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
            option = int(input("Wähle eine Option: "))
            while option > len(stat_ips)+2 or option < 0:
                option = int(input("Wähle eine Option: "))

            if option == len(stat_ips)+1:
                # Anlegen eines neuen Projektes
                stat_ips.append(stat_neues_projekt())
            elif option == len(stat_ips)+2:
                # Zurück ins Hauptmenü
                start()
            elif 0  < option < int(len(dyn_ips))+1:
                # Ausgabe des Projektes
                stat_ips[option-1].print_Kennzahlen()
                stat_ir()
    stat_ir()


    print("Wähle eine Option:")
    print("1 - Dynamische Investitionsrechnung")
    print("2 - Statische Investitionsrechnung")
    rechenart = int(input("Option: "))
    while rechenart != 1 and rechenart != 2:
        rechenart = int(input("Option: "))
    if rechenart == 1:
        print("Dynamische Investitionsrechnung ausgewählt \n")
        dyn_ir()

    elif rechenart == 2:
        print("Statische Investitionsrechnung ausgewählt \n")
        stat_ir()
        
        print ("Fehler! Option nicht gefunden.")
        start()

def start():
    """
    Auswahl zwischen dynamischer und statischer Investitionsrechnung, starten der jeweiligen Funktion
    """
    print("Wähle eine Option:")
    print("1 - Dynamische Investitionsrechnung")
    print("2 - Statische Investitionsrechnung")

    # Eingabe der Option, while-Schleife dient zur Fehlerbehandlung
    rechenart = int(input("Option: "))
    while rechenart != 1 and rechenart != 2:
        rechenart = int(input("Option: "))

    if rechenart == 1:
        print("Dynamische Investitionsrechnung ausgewählt \n")
        dyn_ir()

    elif rechenart == 2:
        print("Statische Investitionsrechnung ausgewählt \n")
        stat_ir()
        
        print ("Fehler! Option nicht gefunden.")
        start()

print("Willkommen beim IUR-Rechner!")
print()
print("### WICHTIG ###")
print("Dieses Programm darf nur von Personen genutzt werden die mind. 20 Vorlesungen") 
print("Interne Unternehmens und Investitionsrechnung besucht haben!")
print("### WICHTIG ###")
print()

# Aufrufen der Start-Funktion
start()