
from collections import deque

fin = open("input_AFD.txt", "r")
fout = open("output_AFD_minimal.txt", "w")

'''
inputul este de forma:
5       - nr stari
10      - numar tranzitii, urmate de acel numar de tranzitii
0 2 a   - tranzitii cu cate un caracter pe linie (daca sunt mai multe, se trec separat)
0 1 b
1 3 a
1 0 b
2 4 a
2 3 b
3 3 a
3 3 b
4 2 a
4 1 b
0       - stare initiala
2       - numar stari finale
0 4     - stari finale

output-ul generat este de aceeasi forma
'''


def tranzitie_cod(tranzitii_stare, simboluri, partitii, partitie_curenta):
    cod = []
    for s in simboluri:
        if s in tranzitii_stare:
            cod.append(partitii[tranzitii_stare[s]])
        else:
            cod.append(-1)
    cod.append(partitie_curenta)
    return tuple(cod)


def Minimizare(partitii, nr_partitii, nr_stari, tranzitii, simboluri):
    minimal = False
    while not minimal:
        partitii_noi = partitii.copy()
        part_dif = []
        for i in range(nr_partitii):
            for j in range(nr_stari):
                if partitii[j] == i:
                    cod = tranzitie_cod(tranzitii[j], simboluri, partitii, i)
                    if cod not in part_dif:
                        part_dif.append(cod)
                    partitii_noi[j] = part_dif.index(cod);
        for i in range(len(partitii_noi)):
            partitii[i] = partitii_noi[i]
        if max(partitii) + 1 == nr_partitii:
            minimal = True
        nr_partitii = max(partitii) + 1


simboluri = []  # numar simboluri
nr_stari = int(fin.readline())  # numar total stari
nr_tranzitii = int(fin.readline())  # numar total tranzitii
tranzitii = list()  # tranzitiile dintre stari
tranzitii_inverse = list()
for i in range(nr_stari):
    tranzitii.append(dict())
    tranzitii_inverse.append(dict())
for i in range(nr_tranzitii):
    aux = [x for x in fin.readline().split()]
    tranzitii[int(aux[0])][aux[2]] = int(aux[1])
    if aux[2] not in tranzitii_inverse[int(aux[1])]:
        tranzitii_inverse[int(aux[1])][aux[2]] = list()
    tranzitii_inverse[int(aux[1])][aux[2]].append(int(aux[0]))
    if aux[2] not in simboluri:
        simboluri.append(aux[2])
si = int(fin.readline())  # stare initiala
nr_sf = int(fin.readline())  # numar stari finale
sf = [int(x) for x in fin.readline().split()]  # stari finale

partitii = [-1] * nr_stari

# eliminare stari izolate
coada = deque([si])
partitii[si] = 0
while coada:
    stare_curenta = coada.popleft()
    for s in simboluri:
        if s in tranzitii[stare_curenta] and partitii[tranzitii[stare_curenta][s]] == -1:
            partitii[tranzitii[stare_curenta][s]] = 0
            coada.append(tranzitii[stare_curenta][s])

# eliminare stari ce nu duc in stari finale
coada = deque([])
for stare_finala in sf:
    if partitii[stare_finala] == 0:
        partitii[stare_finala] = 1
        coada.append(stare_finala)

while coada:
    stare_curenta = coada.popleft()
    for s in simboluri:
        if s in tranzitii_inverse[stare_curenta]:
            for pred in tranzitii_inverse[stare_curenta][s]:
                if partitii[pred] == 0:
                    partitii[pred] = 1
                    coada.append(pred)

# pregatire partitii dupa verificari (-1 inseamna stare eliminata)
for i in range(nr_stari):
    if partitii[i] == 1:
        partitii[i] = 0
    else:
        partitii[i] = -1

partitii_generate = [False] * 2
for i in range(nr_stari):
    if partitii[i] != -1:
        if i in sf:
            partitii[i] = 1
            partitii_generate[1] = True
        else:
            partitii[i] = 0
            partitii_generate[0] = True
    elif i in sf:
        nr_sf -= 1
        sf.remove(i)

if not partitii_generate[1]:  # daca nu avem stari finale, AFD-ul este invalid
    print("AFD MINIMAL INVALID, NU EXISTA STARI FINALE")
elif not partitii_generate[0]:  # daca nu avem stari non-finale avem doar o singura multime
    for i in range(nr_stari):
        if partitii[i] == 1:
            partitii[i] = 0

Minimizare(partitii, max(partitii) + 1, nr_stari, tranzitii, simboluri)
nr_stari_nou = max(partitii) + 1

partitii_afisate = [False] * nr_stari_nou
nr_tranzitii_nou = 0
tranzitii_noi = ''
i = 0
for i in range(nr_stari):
    if partitii[i] != -1:
        if not partitii_afisate[partitii[i]]:
            partitii_afisate[partitii[i]] = True
            for s in simboluri:
                if s in tranzitii[i] and partitii[tranzitii[i][s]] != -1:
                    tranzitii_noi += str(partitii[i]) + ' ' + str(partitii[tranzitii[i][s]]) + ' ' + s + '\n'
                    nr_tranzitii_nou += 1
    i += 1

fout.write(str(nr_stari_nou) + '\n' + str(nr_tranzitii_nou) + '\n')
fout.write(tranzitii_noi)
fout.write(str(partitii[si]) + '\n')
stari_finale = set()
for i in range(nr_sf):
    stari_finale.add(partitii[sf[i]])
fout.write(str(len(stari_finale)) + '\n')
for x in stari_finale:
    fout.write(str(x) + ' ')
