class DynamischeInvestitionsrechnung:
    def __init__(self, name, kzf, laufzeit, anschaffungskosten, cashflows, steuern=0, steuersatz=0, abschreibungen=0):
        self.ip_name = name
        self.kzf = float(kzf)
        self.laufzeit = int(laufzeit)
        self.anschaffungsauszahlungen = float(anschaffungskosten)
        self.cashflows = list(cashflows)
        self.steuern = bool(steuern)
        self.steuersatz = float(steuersatz)
        self.abschreibungen = list(abschreibungen)
        
        self.__kapitalwert = float
        self.__amortisationsdauer = float
        self.__izf = float
        self.__baldwin = float
        self.__etragswert = float
        self.__annuitaet = float
        self.__endwert = float

    def init(self):
        if self.steuern:
            self.kzf = self.kzf*(1-self.steuersatz)

            self.__kapitalwert = self.dyn_kapitalwert_ms()
            self.__amortisationsdauer = self.dyn_amortisationsdauer_ms()
            self.__izf = self.dyn_izf_ms()
        else:
            self.__kapitalwert =self.dyn_kapitalwert_os()
            self.__amortisationsdauer = self.dyn_amortisationsdauer_os()
            self.__izf = self.dyn_izf_os()

        self.__etragswert = self.__kapitalwert+self.anschaffungsauszahlungen
        self.__baldwin = self.dyn_baldwin()
        self.__annuitaet = self.dyn_annuitaet()
        self.__endwert = self.__kapitalwert*((1+self.kzf)**self.laufzeit)

    def dyn_barwert_os(self, jahr, cashflow, kzf):
        if kzf == None: kzf = self.kzf
        return cashflow/((1+kzf)**jahr)
    
    def dyn_barwert_ms(self, jahr, cashflow, abschreibung, kzf, restbuchwert=0):
        if kzf == None: kzf = self.kzf
        return(cashflow-self.steuersatz*(cashflow-abschreibung-restbuchwert))/((1+kzf)**jahr)
            
    def dyn_kapitalwert_os(self, kzf=None):
        if kzf == None: kzf = self.kzf

        kapitalwert = 0-self.anschaffungsauszahlungen
        jahr = 1
        for cashflow in self.cashflows:
            kapitalwert = kapitalwert + self.dyn_barwert_os(jahr, cashflow, kzf)
            jahr = jahr + 1
        return kapitalwert

    def dyn_kapitalwert_ms(self, kzf=None):
        if kzf == None: kzf = self.kzf
        kapitalwert = 0-self.anschaffungsauszahlungen
        restbuchwert = self.anschaffungsauszahlungen
        jahr = int(1)
        while jahr < self.laufzeit:
            cashflow = self.cashflows[jahr-1]
            abschreibung = self.abschreibungen[jahr-1]
            restbuchwert = restbuchwert - abschreibung
            kapitalwert = kapitalwert + self.dyn_barwert_ms(jahr, cashflow, abschreibung, kzf, restbuchwert)
            jahr = jahr+1
        
        kapitalwert = kapitalwert + (self.cashflows[jahr-1]-self.steuersatz*(self.cashflows[jahr-1]-self.abschreibungen[jahr-1]-restbuchwert))/((1+self.kzf)**jahr)
        
        return round(kapitalwert, 2)

    def dyn_annuitaet(self):
        return round(self.__kapitalwert*((((1+self.kzf)**self.laufzeit)*self.kzf)/(((1+self.kzf)**self.laufzeit)-1)), 2)

    def dyn_baldwin(self):
        return round(((
            (
            (self.__etragswert*((1+self.kzf)**self.laufzeit))
            /
            (self.anschaffungsauszahlungen)
            )**(1/self.laufzeit))
            -1)*100
            , 2)
   
    def dyn_ableitung_kapitalwert(self, kzf=None):
        if kzf == None: kzf = self.kzf
        kapitalwert = 0-self.anschaffungsauszahlungen
        jahr = 1
        for cashflow in self.cashflows:
            kapitalwert = kapitalwert + cashflow*(-jahr)*(1+kzf)**(-jahr-1)
            jahr = jahr +1
        return kapitalwert
    
    def dyn_izf_os(self):  
        kapitalwert = self.dyn_kapitalwert_os()
        if kapitalwert > 0:
            izf = self.kzf
        else:
            izf = 0.00
            
        while abs(self.dyn_kapitalwert_os(izf)) > 0.00001:
            izf = izf - (self.dyn_kapitalwert_os(izf))/(self.dyn_ableitung_kapitalwert(izf))
            
        return round(izf*100, 3)

    def dyn_izf_ms(self):
        izf = 0.0
        kapitalwert = self.dyn_kapitalwert_ms()
        if kapitalwert > 0:
            izf = self.kzf
        else:
            izf = 0.0

        while (abs(kapitalwert) > 0.0001):
            kapitalwert = round(self.dyn_kapitalwert_ms(round(izf, 6)),5)
            if kapitalwert < 0:
                izf = round(izf - 0.000001, 6)
            else:
                izf = round(izf + 0.000001, 6)

        return round(izf*100, 2)
    
    def dyn_amortisationsdauer_os (self):
        kum_cf = 0.0-self.anschaffungsauszahlungen
        jahr = 1
        while kum_cf < 0:
            kum_cf = kum_cf + self.dyn_barwert_os(jahr, self.cashflows[jahr-1], self.kzf)
            if kum_cf < 0: jahr+1

        ad_jahre = (jahr)+(
            (kum_cf-self.dyn_barwert_os(jahr, self.cashflows[jahr-1], self.kzf))*-1
            /
            self.dyn_barwert_os(jahr, self.cashflows[jahr-1], self.kzf)
            )
        return round(ad_jahre, 2)
    
    def dyn_amortisationsdauer_ms (self):
        kum_cf = 0.0-self.anschaffungsauszahlungen
        jahr = 1
        restbuchwert = self.anschaffungsauszahlungen
        letzter_barwert = 0.0
        while kum_cf < 0:
            if jahr == self.laufzeit: 
                letzter_barwert = self.dyn_barwert_ms(jahr, self.cashflows[jahr-1], self.abschreibungen[jahr-1], self.kzf, restbuchwert)
            else: 
                letzter_barwert = self.dyn_barwert_ms(jahr, self.cashflows[jahr-1], self.abschreibungen[jahr-1], self.kzf)
            kum_cf = kum_cf + letzter_barwert
            restbuchwert = restbuchwert - self.abschreibungen[jahr-1]
            if kum_cf < 0: jahr+1
            
        ad_jahre = (jahr)+(
            (kum_cf-letzter_barwert)*-1
            /
            letzter_barwert
            )
        return round(ad_jahre, 2)

    def kapitalwert(self):
        return round(self.__kapitalwert, 2)

    def amortisationsdauer(self):
        return round(self.__amortisationsdauer, 2)
    
    def izf(self):
        return round(self.__izf, 2)

    def etragswert(self):
        return round(self.__etragswert, 2)
    
    def annuitaet(self):
        return round(self.__annuitaet, 2)
    
    def baldwin(self):
        return round(self.__baldwin, 2)
    
    def endwert(self):
        return round(self.__endwert, 2)

    def name(self):
        return self.ip_name