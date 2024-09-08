import sys
import time
import random as r
from collections import deque
velicinaStranice = 64
velicinaAdrese = 1024
brojStranica = 16

def dohvatiPetiBit(n) :
  pretvoriUSesnestoBitne = format(n, '016b')
  petiBit = pretvoriUSesnestoBitne[-5]
  return int(petiBit)

def izracunajFizicku (n) :
  pretvoiUosamBitne = format(n, '08b')
  udecimalno = binToDec(pretvoiUosamBitne)
  return hex(udecimalno)
def decimalToBinary(n) :
  return bin(n).replace("0b", "")

def binToDec(n) :
  number = str(n)
  return int(number, 2)


argumenti = sys.argv

indexOf = argumenti.index("stranicenje.py")
brojProcesa = int(argumenti[indexOf + 1])
brojOkvira = int(argumenti[indexOf + 2])

diskLista = []
okvirLista = []
tablicaLista = []

for i in range(brojProcesa):
  listaDiskSejvaj = []
  for j in range(velicinaStranice):
    randomBroj = r.randint(1,50)
    listaDiskSejvaj.append(randomBroj)
  diskLista.append(listaDiskSejvaj)

for i in range(brojOkvira) :
  listaOkviraSejvaj = []
  for j in range(velicinaStranice):
    listaOkviraSejvaj.append(0)
  okvirLista.append(listaOkviraSejvaj)

for i in range(brojProcesa) :
  listaTablicaSejvaj = []
  for j in range(brojStranica) :
    listaTablicaSejvaj.append(0)
  tablicaLista.append(listaTablicaSejvaj)

i = 0
brojacOkvira = 0
fifo = deque()
while i < 5 :
  for p in range(brojProcesa) :
    print(diskLista)
    print(okvirLista)
    print(tablicaLista)
    print("---------------------------")
    #logickaAdresa = 0x01fe
    logickaAdresa = r.randint(0, 1023)

    binarnaLogickaAdresa = decimalToBinary(logickaAdresa)
    
    spremiZadnjihSestBinarnihLogickaAdresa = binarnaLogickaAdresa[-6:]
    prvaCetiriBinarnaLogickaAdresa = binarnaLogickaAdresa[:-6]

    dekadskiZadnjihSest = binToDec(spremiZadnjihSestBinarnihLogickaAdresa)
    dekadskiPrviCetiri = binToDec(prvaCetiriBinarnaLogickaAdresa)

    print("proces: " + str(p))
    print("\tlog. adresa: " + hex(logickaAdresa))
    
    procitajPodatakUTablici = tablicaLista[p][dekadskiPrviCetiri]
    
    randomBrojZaUpisatPrvo = r.randint(32, 64)
    #provjera prisutnosti podatka u tablici
    #ako udemo 32 je 5 bit pa preko njega smislit
    if procitajPodatakUTablici  != randomBrojZaUpisatPrvo:
      print("\tPromasaj!")
      if brojacOkvira < brojOkvira :
        print("\t\tdodijeljen okvir " + hex(brojacOkvira))
        
        tablicaLista[p][dekadskiPrviCetiri] = randomBrojZaUpisatPrvo
        okvirLista[brojacOkvira] = diskLista[p]
        brojacOkvira += 1
        fifo.append((p, dekadskiPrviCetiri))
      else :
        print("\t\tMemorija puna, pokretanje FIFO zamjene!")
        procesPovuci, vrijednostUtablici = fifo.popleft()
        indeksOkvira = okvirLista.index(diskLista[procesPovuci])
        tablicaLista[procesPovuci][vrijednostUtablici] = 0

        randomBrojZaUpisat = r.randint(32, 64)
        tablicaLista[p][dekadskiPrviCetiri] = randomBrojZaUpisat
        okvirLista[indeksOkvira] = diskLista[p]
        fifo.append((p, dekadskiPrviCetiri))
    else :
      print("\tPogodak!")
      print("\tStranica se nalazi u ramu!")
    
    fizickaAdresa = izracunajFizicku(dekadskiZadnjihSest)
    print("\tfiz. adresa: " + fizickaAdresa)
    print("\tsadrzaj adrese: " + str(diskLista[p][dekadskiZadnjihSest]))
    i += 1
    time.sleep(1)
    

