import os


def verificationAR(dico,regleEnA,regleEnB):
    valideA=['a','+','-','[',']']

    if(regleEnB!=''):
        valideA.append('b')
        
        for i in dico['axiome']:
            if(i not in valideA):
                print("Le contenu de l'axiome n'est pas valide")
                return False
        for i in regleEnA:
            if(i not in valideA):
                print("Le contenu de la regles en a n'est pas valide")
                return False
        for i in regleEnB:
            if(i not in valideA):
                print("Le contenu de la regles en b n'est pas valide")
                return False
    
    return True



def verificationATN(dico):
   
    for i in [dico['angle'],dico['taille']]:
        try:
            float(i)
        except ValueError:
            print(i,"L'angle ou la taille n'est pas valide , il faut que ce soit un nombre réel")
            return False
    
    try:
        int(dico['niveau'])
    except ValueError:
        print("Le niveau n'est pas valide , il faut que ce soit un entier")
        return False
                
    if (float(dico['angle']) > 360 or float(dico['angle']) < 0): # verif si lettre
        print("Le contenu de l'ange n'est pas valide")
        return False
    if (float(dico['taille'])<= 0 or float(dico['taille'])>50):
        print("Le contenu de taille n'est pas valide")
        return False
    if(int(dico['niveau']) < 0 or int(dico['niveau'])>100):
        print("Le contenu de niveau n'est pas valide")
        return False
    return True


def readfile(f):
    regles=[]
    data=f.readlines()
    data = sorted(data)
   
    for a in range(0,len(data)):
        if '\n' in data:
            data.remove('\n')
   
    options = {}
    if data[1].startswith('"b='):
       regles.append(str(data[0]).split('=')[1].replace('\n','').replace("'","").replace('"','').replace(' ',''))#formatage de la premiere regle
       regles.append(str(data[1]).split('=')[1].replace('\n','').replace("'","").replace('"','').replace(' ',''))#formatage de la deuxième regle
       options['angle'] = str(str(data[2]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de l'angle
       options['axiome'] = str(str(data[3]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de l'axiome
       options['niveau'] = str(str(data[4]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage du niveau
       options['taille'] = str(str(data[6]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')#formatage de la taille
    else:
        
        regles.append(str(data[3]).split('=')[2].replace('\n','').replace("'","").replace('"','').replace(' ',''))
        options['angle'] = str(str(data[0]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')
        options['axiome'] = str(str(data[1]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')
        options['niveau'] = str(str(data[2]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')
        options['taille'] = str(str(data[4]).split('=')[1].replace('\n','')).replace("'","").replace('"','').replace("'","").replace('"','').replace(' ','')
    options['regles'] = "/".join(regles)
    return options


path = input('Rentrez le chemin absolu de l endroit ou est votre fichier settings, ou le nom du fichier si il est dans le meme dossier que le programme\n')
with open(path,'r') as f:
    options = readfile(f)
    if '/' in options['regles']:
            regleEnA = options['regles'].split('/')[0]
            regleEnB = options['regles'].split('/')[1]
    else:
            regleEnA = options['regles']
            regleEnB = ''
            
    print(options)
    if verificationATN(options) and verificationAR(options, regleEnA,regleEnB):
        input('contenu correct')
    else:
        input('contenu incorrect')