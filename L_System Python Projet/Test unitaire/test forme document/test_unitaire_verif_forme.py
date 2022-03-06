import os


def verification(path):
    f=open(path,'r')
    data = f.read().split()
    print(data)
    nombre = {i : data.count(i) for i in data}
    print(nombre)
    try:
        if nombre['axiome'] > 1:
           print('ax')
           return False
    except KeyError :
        print('ax')
        return False
    
    try:
        if nombre['angle'] > 1:
           print('an')
           return False
    except KeyError :
        print('an')
        return False
    
    try:
        if nombre['niveau'] > 1:
           print('n')
           return False
    except KeyError :
        print('n')
        return False
    
    try:
        if nombre['taille'] > 1:
           print('t')
           return False
    except KeyError :
        print('t')
        return False
    
    try:
        if nombre['regles'] > 1:
           return False
    except KeyError : 
        return False
    f.close()
    return True


path = input('Rentrez le chemin absolu de l endroit ou est votre fichier settings, ou le nom du fichier si il est dans le meme dossier que le programme\n')
path = os.path.join(path)
with open(path,'r') as f:
    if(verification(path)):
        print('La forme du document est correcte')
    else:
        print('la forme du document est incorrecte')
        
input('fin')