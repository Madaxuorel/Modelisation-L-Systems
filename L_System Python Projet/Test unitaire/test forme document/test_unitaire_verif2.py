import os

defs = ['axiome', 'regles','angle','taille','niveau']

def removen(data):
    for a in range(0,len(data)):
        if '\n' in data:
            data.remove('\n')
    pass
    return data

def verification2(path):
    f=open(path,'r')
    data = f.readlines()
    data = removen(data)
    
   
    for elem in data:
        if elem.startswith('"a=') or elem.startswith('"b='):
            pass
        else:
            if elem.split(' ')[0] in defs:
                pass
            else:
                
                return False
    return True

path = input('Rentrez le chemin absolu de l endroit ou est votre fichier settings\n')
path = os.path.join(path)
with open(path,'r') as f:
    if(verification2(path)):
        input('document correct')
    else:
        input('document incorrect')