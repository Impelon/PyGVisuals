# Datei:   avlbaum.py
# Version: 1.1
# Datum:   30.03.2006
# Autor:   Th. Beyer

class AVLKnoten:
    def __init__(self, typ="atomar"):
        self.inhalt=None
        self.typ=typ
        self.links=None
        self.rechts=None
        self.hoehe=0
        self.balance=0

    def setzeInhalt(self, i):
        self.inhalt=i

    def holeInhalt(self):
        return self.inhalt

    def holeWert(self):
        if self.typ=="atomar":
            return self.inhalt
        else:
            try:
                return self.inhalt.holeWert()
            except:
                return None

    def setzeLinks(self, k):
        self.links=k

    def holeLinks(self):
        return self.links
    
    def setzeRechts(self, k):
        self.rechts=k

    def holeRechts(self):
        return self.rechts

    def holeKHoehe(self):
        self.bestimmeKHoehe()
        return self.hoehe

    def holeKBalance(self):
        self.bestimmeKBalance()
        return self.balance

    def bestimmeKHoehe(self):
        if self.links==None:
            klh=-1
        else:
            klh=self.links.holeKHoehe()
        if self.rechts==None:
            krh=-1
        else:
            krh=self.rechts.holeKHoehe()
        self.hoehe=max(klh,krh)+1

    def bestimmeKBalance(self):
        if self.links==None:
            hlinks=-1
        else:
            hlinks=self.links.holeKHoehe()
        
        if self.rechts==None:
            hrechts=-1
        else:
            hrechts=self.rechts.holeKHoehe()
        self.balance=hlinks-hrechts
        


class AVLBaum:
    def __init__(self):
        self.root=None

    def holeHoehe(self, kbaum=None):
        if self.root==None:
            print "Baum ist leer!"
            return None
        if kbaum==None:
            kbaum=self.root
        if kbaum.holeLinks()==None and kbaum.holeRechts()==None:
            return 0
        elif kbaum.holeLinks()==None:
            return 1+self.holeHoehe(kbaum.holeRechts())
        elif kbaum.holeRechts()==None:
            return 1+self.holeHoehe(kbaum.holeLinks())
        else:
            return 1+max(self.holeHoehe(kbaum.holeLinks()),self.holeHoehe(kbaum.holeRechts()))
        
    def einfuegen(self, inhalt, typ="atomar"):
        einKnoten = AVLKnoten(typ)
        einKnoten.setzeInhalt(inhalt)
        self.einfuegenKnoten(einKnoten)

    def einfuegenKnoten(self, knoten, kbaum=None, vg=None):
        #Fuegt den Knoten/Teilbaum knoten in den Teilbaum kbaum mit Vorgaenger vg ein;
        #hat kbaum den Wert None, beginnt der Vorgang an der Wurzel (root);
        #am Ende wird die Methode ausbalancieren aufgerufen
        if kbaum == None:
            if self.root == None:
                self.root = knoten
                return
            kbaum = self.root
        if knoten == None:
            return
        if knoten.holeWert() >= kbaum.holeWert():
            if kbaum.holeRechts() != None:
                self.einfuegenKnoten(knoten, kbaum.holeRechts(), kbaum)
            else:
                kbaum.setzeRechts(knoten)
        else:
            if kbaum.holeLinks() != None:
                self.einfuegenKnoten(knoten, kbaum.holeLinks(), kbaum)
            else:
                kbaum.setzeLinks(knoten)
        self.ausbalancieren(kbaum, vg)

    def loeschen(self, wert, kbaum=None, vg=None):
        if kbaum == None:
            if self.root == None:
                print "Baum ist leer!"
                return
            kbaum = self.root
        if wert > kbaum.holeWert():
            if kbaum.holeRechts() != None:
                self.loeschen(wert, kbaum.holeRechts(), kbaum)
        elif wert < kbaum.holeWert():
            if kbaum.holeLinks() != None:
                self.loeschen(wert, kbaum.holeLinks(), kbaum)
        else:
            puffer = kbaum
            if kbaum.holeLinks() != None:
                kbaum = kbaum.holeLinks()
                while kbaum.holeRechts() != None:
                    if kbaum.holeRechts().holeRechts() == None:
                        rechts = kbaum.holeRechts()
                        kbaum.setzeRechts(kbaum.holeRechts().holeLinks())
                        kbaum = rechts
                        break
                    kbaum = kbaum.holeRechts()
                else:
                    puffer.setzeLinks(kbaum.holeLinks())
                kbaum.setzeLinks(puffer.holeLinks())
                kbaum.setzeRechts(puffer.holeRechts())
            elif kbaum.holeRechts() != None:
                kbaum = kbaum.holeRechts()
            else:
                kbaum = None
            if vg != None:
                if puffer.holeWert() > vg.holeWert():
                    vg.setzeRechts(kbaum)
                else:
                    vg.setzeLinks(kbaum)
            else:
                self.root = kbaum
        self.ausbalancieren(kbaum, vg)

    def ausbalancieren(self, kbaum, vg):
        #bestimmt fuer kbaum die Balance und stoesst im Fall der Unausgeglichenheit
        #die entsprechende(n) Rotation(en) an
        if kbaum == None:
            return
        balance = kbaum.holeKBalance()
        if balance > 1:
            #rechtsRotationen
            links = kbaum.holeLinks()
            if links.holeKBalance() <= 0:
                print "dpR"
                self.doppeltRechtsRotation(kbaum, vg)
            else:
                print "eR"
                self.einfachRechtsRotation(kbaum, vg)
        elif balance < -1:
            #linksRotationen
            rechts = kbaum.holeRechts()
            if rechts.holeKBalance() >= 0:
                print "dpL"
                self.doppeltLinksRotation(kbaum, vg)
            else:
                print "eL"
                self.einfachLinksRotation(kbaum, vg)
    
    def einfachLinksRotation(self, kbaum, vg):
        if kbaum == None:
            if self.root == None:
                print "Baum ist leer!"
                return
            kbaum = self.root
        rechts = kbaum.holeRechts()
        rlinks = rechts.holeLinks()
        rechts.setzeLinks(kbaum)
        kbaum.setzeRechts(rlinks)
        if vg != None:
            if rechts.holeWert() < vg.holeWert():
                vg.setzeLinks(rechts)
            else:
                vg.setzeRechts(rechts)
        else:
            self.root = rechts

    def einfachRechtsRotation(self, kbaum, vg):
        if kbaum == None:
            if self.root == None:
                print "Baum ist leer!"
                return
            kbaum = self.root
        links = kbaum.holeLinks()
        lrechts = links.holeRechts()
        links.setzeRechts(kbaum)
        kbaum.setzeLinks(lrechts)
        if vg != None:
            if links.holeWert() < vg.holeWert():
                vg.setzeLinks(links)
            else:
                vg.setzeRechts(links)
        else:
            self.root = links

    def doppeltLinksRotation(self, kbaum, vg):
        if kbaum == None:
            if self.root == None:
                print "Baum ist leer!"
                return
            kbaum = self.root
        rechts = kbaum.holeRechts()
        self.einfachRechtsRotation(rechts, kbaum)
        self.einfachLinksRotation(kbaum, vg)
            
    def doppeltRechtsRotation(self, kbaum, vg):
        if kbaum == None:
            if self.root == None:
                print "Baum ist leer!"
                return
            kbaum = self.root
        links = kbaum.holeLinks()
        
        self.einfachLinksRotation(links, kbaum)
        self.einfachRechtsRotation(kbaum, vg)
    
    def traversieren(self, order="pre", kbaum=None):
        if self.root==None:
            print "Baum ist leer!"
        else:
            if kbaum==None:
                kbaum=self.root
            erg=[]
            if order=="pre":
                erg=erg+[(kbaum.holeInhalt(),kbaum.holeKHoehe())]
                if kbaum.holeLinks()<>None:
                    erg=erg+(self.traversieren(order,kbaum.holeLinks()))
                if kbaum.holeRechts()<>None:
                    erg=erg+(self.traversieren(order,kbaum.holeRechts()))
            elif order=="in":
                if kbaum.holeLinks()<>None:
                    erg=erg+self.traversieren(order,kbaum.holeLinks())
                erg=erg+[(kbaum.holeInhalt(),kbaum.holeKHoehe())]
                if kbaum.holeRechts()<>None:
                    erg=erg+self.traversieren(order,kbaum.holeRechts())
            else:
                if kbaum.holeLinks()<>None:
                    erg=erg+self.traversieren(order,kbaum.holeLinks())
                if kbaum.holeRechts()<>None:
                    erg=erg+self.traversieren(order,kbaum.holeRechts())
                erg=erg+[(kbaum.holeInhalt(),kbaum.holeKHoehe())]
                
            return erg
        
    def leeren(self):
        self.root=None
        
    def suchen(self, wert, kbaum=None):
        if self.root==None:
            print "Baum ist leer!"
            return None
        else:
            if kbaum==None:
                kbaum=self.root

            if wert==kbaum.holeWert():
                return kbaum.holeInhalt()
            elif wert<kbaum.holeWert():
                if kbaum.holeLinks()<>None:
                    return self.suchen(wert, kbaum.holeLinks())
                else:
                    return None
                    print "Element nicht gefunden!"
                    
            else:
                if kbaum.holeRechts()<>None:
                    return self.suchen(wert ,kbaum.holeRechts())
                else:
                    return None
                    print "Element nicht gefunden!"

    def holeTiefe(self, knoten, kbaum=None, h = 1):
        if self.root==None:
            print "Baum ist leer!"
            return 0
        else:
            if kbaum==None:
                kbaum=self.root
            if knoten is kbaum:
                return h
            elif knoten.holeWert()<kbaum.holeWert():
                if kbaum.holeLinks()!=None:
                    return self.holeTiefe(knoten, kbaum.holeLinks(), h + 1)
                else:
                    return 0
                    print "Element nicht gefunden!"
                    
            elif knoten.holeWert()>kbaum.holeWert():
                if kbaum.holeRechts()!=None:
                    return self.holeTiefe(knoten, kbaum.holeRechts(), h + 1)
                else:
                    return 0
                    print "Element nicht gefunden!"
            else:
                if kbaum.holeLinks()!=None:
                    t = self.holeTiefe(knoten, kbaum.holeLinks(), h + 1)
                    if t == 0:
                        if kbaum.holeRechts()!=None:
                            return self.holeTiefe(knoten, kbaum.holeRechts(), h + 1)
                    return t
        return h

