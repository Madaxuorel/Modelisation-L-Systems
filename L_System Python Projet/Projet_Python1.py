import os
from sys import exit
from turtle import *

defs = ['axiome', 'regles','angle','taille','niveau']


def verification(path): # Première fonction pour vérifier le contenu du fichier
    f=open(path,'r')
    data = f.read().split()
    nombre = {i : data.count(i) for i in data} # dictionnaire avec nombre d'occurence de chaque def
    #le try permet de tester une condition, et si cette condition engendre une erreur de type precise (ici KeyError) il execute une autre condition. 
    #Il y a sortie d'erreur KeyError quand on essaie d'acceder à un element inexistant dans un dictionnaire.
    try:
        #any est une fonction qui renvoie True si au moins une element de l'iterable est vrai. Sinon, retourne False. Ici, l'iterable est 'i' parcourant une liste.
        if any(i > 1 for i in [nombre['axiome'], nombre['angle'], nombre['niveau'], nombre['taille'], nombre['regles']]):
            return False
    except KeyError :
        return False
        f.close
        
    return True

def readfile(f): #Fonction de lecture du fichier
    regles=[]
    data=f.readlines()
    data = sorted(data) #range les elements du fichier par ordre alphabetique, pour un lecture plus simple.
   
    data = removen(data) #enleve les '\n' de data
   
    options = {}
    if data[1].startswith('"b='): # Si il y a deux regles :
       regles.append(str(data[0]).split('=')[1].replace('\n','').replace("'","").replace('"','').replace(' ',''))#formatage de la premiere regle, on elve les \n, les ' et les espaces
       regles.append(str(data[1]).split('=')[1].replace('\n','').replace("'","").replace('"','').replace(' ',''))#formatage de la deuxième regle, on elve les \n, les ' et les espaces
       options['angle'] = str(str(data[2]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de l'angle, on elve les \n, les ' et les espaces
       options['axiome'] = str(str(data[3]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de l'axiome, on elve les \n, les ' et les espaces
       options['niveau'] = str(str(data[4]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage du niveau, on elve les \n, les ' et les espaces
       options['taille'] = str(str(data[6]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de la taille, on elve les \n, les ' et les espaces
    else: #Si il y a une regle
        regles.append(str(data[3]).split('=')[2].replace('\n','').replace("'","").replace('"','').replace(' ',''))#formatage de la premiere regle, on elve les \n, les ' et les espaces
        options['angle'] = str(str(data[0]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de l'angle, on elve les \n, les ' et les espaces
        options['axiome'] = str(str(data[1]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de l'axiome, on elve les \n, les ' et les espaces
        options['niveau'] = str(str(data[2]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage du niveau, on elve les \n, les ' et les espaces
        options['taille'] = str(str(data[4]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de la taille, on elve les \n, les ' et les espaces
    options['regles'] = "/".join(regles) #Si il y a deux regles, on les rassembles dans une case du dictionnaire en les séparants d'un / . Si il y a une seule regle, on la met dans la case du dico
    return options # on renvoie le dico

def verificationATN(dico): # Verification du contenu des définitions ATN (=Angle ,Taille , Niveau)
    for i in [dico['angle'],dico['taille']]:    #on teste d'abord si ce sont des réels pour l'angle et la taille
        try:
            float(i)
        except ValueError:
            print("L'angle ou la taille n'est pas valide , il faut que ce soit un nombre réel")
            return False                        # Sinon on retourne une erreur
    try:
        int(dico['niveau'])                     # Pour le niveau on vérifie que c'est un entier sinon on retourne une erreur
    except ValueError:
        print("Le niveau n'est pas valide , il faut que ce soit un entier")
        return False
                
    if (float(dico['angle']) > 360 or float(dico['angle']) < 0):   # On vérifie maintenant que ATN possèdent le bonne encadrement 
        print("Le contenu de l'ange n'est pas valide")
        return False                                               # Sinon on retourne erreur
    if (float(dico['taille'])<= 0 or float(dico['taille'])>50):
        print("Le contenu de taille n'est pas valide")
        return False
    if(int(dico['niveau']) < 0 or int(dico['niveau'])>100):
        print("Le contenu de niveau n'est pas valide")
        return False
    return True                                                    # Si le contenu est validé la fonction retourne vrai

def verificationAR(dico,regleEnA,regleEnB): # Verification du contenu de l'Axiome et des Règles
    valideA=['a','+','-','[',']','*']       # Liste de caractère autorisé dans les règles

    if(regleEnB!=''):               # Si il y a une deuxième règle en b , on ajoute l'élement b a la liste
        valideA.append('b')
        
    for i in dico['axiome']:    # On vérifie ensuite que l'axiome et les règles sont bien composé d'élement de la liste
        if(i not in valideA):   
            print("Le contenu de l'axiome n'est pas valide")
            return False        # Sinon on retourne une erreur
    for i in regleEnA:
         if(i not in valideA):
            print("Le contenu de la regles en a n'est pas valide")
            return False
    for i in regleEnB:
        if(i not in valideA):
            print("Le contenu de la regles en b n'est pas valide")
            return False
    
    return True


#Applique la regle a l'axiome donne pour passer au niveau superieur
def NiveauSuperieur(axiome, regleEnA, regleEnB, niveau):
    indexNiveau = 0
    #Si le niveau donne en fichier d'entree est 0, l'axiome iinitial ne change pas.
    if (niveau == 0) :
        return axiome
    #Boucle qui applique la regle a l'axiome jusqu'a ce que le niveau demande soit atteint.
    else :
        while indexNiveau < niveau :
            #axiome est une chaine de caracteres donc immuable. La liste listeAxiome permet de changer un symbole et de le remplacer par les ymboles de la regle.
            listeAxiome = list(axiome)
            for i in range(len(listeAxiome)) :
                if (listeAxiome[i] == 'a'):
                    listeAxiome[i] = regleEnA
                elif (listeAxiome[i] == 'b'):
                    listeAxiome[i] = regleEnB
            #une fois que les elements de la liste ont ete modifies, on reforme l'axiome avec la methode .join() .
            axiome = ''.join(listeAxiome)
            indexNiveau += 1
        return axiome

#Cette fonction renvoie les coordonnees (possition()) ainsi que l'orientation (heading()) de la tortue au moment ou elle est appelee.
def MemoriserPositionActuelle() :
    return position(), heading()

#Cette fonction renvoie le tuple retourPosition après avoir modifie les coordonnees et l'angle de la tortue.
def RetournerDernierePositionMemorisee(listePositions) :
    #la methode .pop() accede au dernier element de la liste (car aucun argument n'a ete donne) et le supprime de la liste
    retourPosition = listePositions.pop()
    pu()    #pu() car sinon la tortue trace un trait lors de son trajet.
    setposition(retourPosition[0])  #Definition du vecteur coordonnees de la tortue aux dernieres coordonnes memorisees dans le tuple retourPosition
    setheading(retourPosition[1])   #Definition de l'orientation de la tortue aux dernieres coordonnes memorisees dans le tuple retourPosition
    return retourPosition   #Retourner retourPosition ne sert qu'a l'ecriture du fichier de sortie


def EcrireFichierSortie(fichierSortie) :
    fichierSortie.write('from turtle import *\n')
    fichierSortie.write("color('black')\n")
    fichierSortie.write("speed(0)\n")
    return fichierSortie

#Dans la fonction Dessin, i parcourt l'axiome final et execute et ecrit dans un fichier fichierDeSortie les commandes correspondant au symbole sur lequel il se trouve.
def Dessin(axiome, regleEnA, regleEnB, niveau, angle, taille) :
    axiome = NiveauSuperieur(axiome, regleEnA, regleEnB, niveau)
    fichierSortie = open('fichierDeSortie.py', "w")
    EcrireFichierSortie(fichierSortie)
    listePositions = []
    for i in axiome:
        if (i == "a") :
            pd(), fd(taille)
            fichierSortie.write('pd(), fd({}) ;\n' .format(taille))
        elif (i == "b") :
            pu(), fd(taille)
            fichierSortie.write('pu(), fd({}) ;\n' .format(taille))
        elif (i == "+") :
            right(angle)
            fichierSortie.write('right({}) ;\n' .format(angle))   
        elif (i == "-") :
            left(angle)
            fichierSortie.write('left({}) ;\n' .format(angle))
        elif (i == "*") :
            right(180)
            fichierSortie.write('right(180) ;\n')
        elif (i == "[") :
            positionActuelle = MemoriserPositionActuelle()  #le tuple positionActuelle stocke le vecteur coordonnees et l'angle de la tortue.
            listePositions.append(positionActuelle) #liste qui stocke tous les tuples positionActuelle lorsque le symbole "[" est rencontre.
            fichierSortie.write("listePositions = {} ;\n" .format(listePositions))
        elif (i == "]") :
            retourPosition = RetournerDernierePositionMemorisee(listePositions) #Affectation de retourPosition pour utiliser cette valeur dans le .write() ci-dessous.
            fichierSortie.write('pu(), setposition({0}), setheading({1}) ;\n' .format(retourPosition[0], retourPosition[1]))
    update()
    fichierSortie.write("exitonclick()\nupdate()")
    fichierSortie.close(), exitonclick()
    

def removen(data):   # Fonction qui permet de supprimer les \n d'une liste
    for a in range(0,len(data)):
        if '\n' in data:
            data.remove('\n')
    pass
    return data

def verification2(path): # On vérifie que la forme du fichier est correct , cad ,qu'il n'y a pas de ligne inutiles
    f=open(path,'r')
    data = f.readlines()
    data = removen(data)

    for elem in data:   # On regarde si les ligne sont une des règles
        if elem.startswith('"a=') or elem.startswith('"b='):
            pass
        else:
            if elem.split(' ')[0] in defs:  # Et Si les lignes ne sont pas une des définitions ou règle , on retourne erreur
                pass
            else:
                return False
                
    return True

def main() :
    path = input("Rentrez le chemin absolu de l'endroit ou est votre fichier settings\n")
    path = os.path.join(path)
    with open(path,'r') as f:
        if(verification(path) and verification2(path)):
            options = readfile(f)
        else:
            input("La forme du fichier n'est pas correcte, appuyez sur entree pour quitter")
            exit(0)
            
        if '/' in options['regles']:
            regleEnA = options['regles'].split('/')[0]
            regleEnB = options['regles'].split('/')[1]
        else:
            regleEnA = options['regles']
            regleEnB = ''
        
        if(verificationATN(options) and verificationAR(options,regleEnA,regleEnB)):

            niveau = float(options['niveau'])
            axiome = options['axiome']
            angle = float(options['angle'])
            taille = float(options['taille'])

            tracer(0,0)
            Dessin(axiome, regleEnA, regleEnB, niveau, angle, taille)
        else:
            exit(0)
    return 0

main()