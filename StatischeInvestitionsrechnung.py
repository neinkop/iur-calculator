class StatischeInvestitionsrechnung:
    def __init__(self, name, kzf, a0, l, t, bk, erlöse, kb_art, Fk, fk_zins):
        self.__name = name
        self.__kzf = kzf
        self.__anschaffungsauszahlung = a0
        self.__liquidationserlös = l
        self.__nutzungsdauer = t
        self.__betriebskosten = bk
        self.__Erlöse = erlöse
        self.__KB_Art = kb_art
        self.__Fremdkapital = Fk
        self.__Fk_zins = fk_zins

        self._Gewinn = int
        self._Amortisation = int
        self._GK_Rentabilität = int
        self._EK_Rentabilität = int
    
    def stat_Abschreibungen(self):
        """Berechnung der Abschreibungsauszahlung

        Returns:
            int: Abschreibungsauszahlung in Euro
        """
        return round((self.__anschaffungsauszahlung-self.__liquidationserlös)/self.__nutzungsdauer, 0)

    def stat_durchschn_Kapitalbindung(self):
        """Berechnung der durchschnittlichen Kapitalbindung

        Returns:
            int: durchschnittliche Kapitalbindung in Euro
        """
        if self.__KB_Art == 1:
            ergebnis = (self.__anschaffungsauszahlung+self.__liquidationserlös)/2
        elif self.__KB_Art == 2:
            ergebnis = (self.__anschaffungsauszahlung-self.__liquidationserlös)*((self.__nutzungsdauer+1)/(2*self.__nutzungsdauer))+self.__liquidationserlös
        return round(ergebnis, 0)

    def stat_kalk_Zinsen(self):
        """Berechnung kalkulatorische Zinsen

        Returns:
            int: kalkulatorische Zinsen in Euro
        """
        return round(self.__kzf*self.stat_durchschn_Kapitalbindung(), 0)
            
    def stat_Gewinn(self):
        """Berechnung durchschnittlicher Gewinn

        Returns:
            int: Gewinn in Euro
        """
        ergebnis = self.__Erlöse-(self.__betriebskosten + self.stat_kalk_Zinsen() + self.stat_Abschreibungen())
        return round(ergebnis, 0)
        
    def stat_Amortisation(self):
        """Berechnung statische Amortisationsdauer

        Returns:
            int: Amortisationsdauer in Jahren
        """
        ergebnis = self.__anschaffungsauszahlung/(self.stat_Gewinn() + self.stat_kalk_Zinsen() + self.stat_Abschreibungen())
        return round(ergebnis, 3)

    def stat_Rentabilität(self):
        """Berechnung GK-Rentabilität und EK-Rentabilität

        Returns:
            float: GK-Rentabilität, EK-Rentabilität (in Prozent)
        """
        GK_Rentabilität = (self.stat_Gewinn()+self.stat_kalk_Zinsen())/self.stat_durchschn_Kapitalbindung()
        if self.__Fremdkapital == 0:
            return round(GK_Rentabilität*100, 2), '- '
        else:
            EK_Rentabilität = (self.stat_Gewinn()+self.stat_kalk_Zinsen()-((self.__Fremdkapital/2)*self.__Fk_zins))/(self.stat_durchschn_Kapitalbindung()/2)
            return round(GK_Rentabilität*100, 2), round(EK_Rentabilität*100, 2)
    
    def print_Kennzahlen(self):
        """
        Ausgabe der berechneten Kennzahlen als formatierte Tabelle
        """
        print(f'\n{self.__name}: ')
        print(''+91*'-')
        print(f'{"Gewinn":^20} | {"Amortisation":^20} | {"EK-Rentabilität":^20} | {"GK-Rentabilität":^20}')
        print(91*'-')
        print(f'{self._Gewinn:^20} | {self._Amortisation:^20} | {self._EK_Rentabilität:^20} | {self._GK_Rentabilität:^20}')
        print(91*'-')
    
    def get_name(self):
        return self.__name