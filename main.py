from node import *
import os


### ALPHABET ###

def create_alphabet(text):
    """
    Creation de l'alphabet d'un texte, avec chaque caractère utilisé et sa fréquence.

    Parametres :
        text : chaine de caracteres correspondant au nom d'un fichier .txt
    
    Retourne :
        a : dictionnaire dont les clés sont les caractères présents dans
        le texte et qui stocke leur fréquence
    """
    
    f = open(text, 'r')
    a = {f.read(1) : 1} #initialise le dictionnaire avec le 1er caractère
    while True: 

        #lecture du fichier caractère par caractère
        char = f.read(1)
        if not char:
            #fin du texte
            break 

        else :
            #apparition d'un char deja dans le dict (augmentation de la fréquence)
            if char in a.keys():
                a[char]+=1

            #apparition d'un char pour la 1ere fois (initialisation dans le dict)
            else :
                a[char]=1
    
    f.close()
    return a

def sort_alphabet(a) :
    """
    Tri de l'alphabet obtenu precedemment par ordre croissant de frequence puis par ordre alhabetique.

    Parametres :
        a : dictionnaire dont les clés sont les caractères présents dans
        le texte et qui stocke leur fréquence (renvoye par la fonction ci dessus)
    
    Retourne :
        sorted_tab : liste de tuples, chaque tuple comprend un caractere puis sa frequence
        Cette liste est triee par frequence puis par ordre alhabetique

    """
    sorted_tab = sorted(a.items(), key=lambda x: (x[1],x[0]))
    return sorted_tab

def alphabet_file(text) :
    """
    Creation du fichier comprenant les caractères de l'alphabet et leur frequence

    Parametres :
        text : chaine de caracteres correspondant au nom d'un fichier .txt

    Pas de retour, creation d'un nouveau fichier

    """

    name = text.replace('.txt', '_freq.txt')
    f = open(name, 'w')
    alphabet = sort_alphabet(create_alphabet(text))
    f.write(str(len(alphabet))+"\n")
    for e in alphabet:
        f.write(f"{e[0]}  {e[1]} \n")
    f.close()


### ARBRE DE RECHERCHE ###

def treesList(alphabetList) : 
    """
    Creation d'une liste de noeuds basee sur la liste des caracteres de l'alphabet.

    Parametres:
        alphabetList : liste triee de tuples, chaque tuple comprend un caractere puis sa frequence
        (renvoyee par la fonction sort_alphabet)

    Retourne :
        res : liste de nodes

    """
    res = []
    for tab in alphabetList :
        # initialisation de chaque noeud : label = caractere / freq = frequence
        node = Node(tab[0], tab[1]) 
        res.append(node)
    return res

def insertNewTree(treesList, t):
    """
    Insertion d'un nouvel arbre/noeud dans la liste, en respectant le tri par fréquence

    Parametres:
        treesList : liste de nodes, correspondant a la racine d'arbres (renvoyee par la fonction treesList)
        t : Node,correspondant a la racine d'un arbre, pas a un caractere

    Pas de retour, treesList est modifiee directement

    """
    freq = t.getFreq()
    l = treesList

    # cas ou le nouveau noeud a la frequence la plus elevee
    if freq > l[len(l)-1].getFreq() :
        l.append(t)
    
    #cas ou le nouveau noeud doit etre insere au milieu du tableau
    else :
        for i in range(0,len(l)-1) :
            tree = l[i]
            nextTree = l[i+1]

            # insertion juste avant le noeud qui possede une freq egale ou superieure
            # pas besoin de tri alphabetique, le noeud t ne represente pas un caractere, seulement la racine d'un arbre
            if (tree.getFreq() < freq) and (nextTree.getFreq() >= freq) :
                l.insert(i+1, t)
    

def huffmanTree(treesList) :
    """
    Construction de l'arbre en utilisant l'algorithme de Huffman

    Parametres :
        treesList : liste de nodes, correspondant a la racine d'arbres (renvoyee par la fonction treesList)
    
    Pas de retour, treesList est modifiee directement

    """
    # repetition du processus jusqu'a obtemption d'un unique arbre
    while len(treesList)>1:
        t1 = treesList[0]
        t2 = treesList[1]
        freqT = t1.getFreq() + t2.getFreq()
        # creation d'un nouveau noeud, racine de l'arbre
        t = Node('noeud', freqT, t1, t2) # label = 'noeud' (pas un caractere), enfants = t1 et t2
        insertNewTree(treesList, t) # insertion de l'arbre a la bonne place dans la liste
        treesList.remove(t1)
        treesList.remove(t2)


### CODAGE ###

def attrBitToChar(root, res = {}, path = ""):
    """
    Parcours de l'arbre cree avec l'algorithme de Huffman, par recursivite
    
    Parametres :
        root : node, racine de l'arbre
        res : dictionnaire dont les clés sont les caractères et leurs valeurs le bit associe
        path : chaine de caracteres de 0 et de 1, représentant le parcours dans l'arbre
    
    Retourne :
        res : dictionnaire dont les clés sont les caractères et leurs valeurs le bit associe
            Le bit associe correspond au path, le chemin parcouru dans l'arbre

    """

    # verifie qu'il y a eu un deplacement 
    if root :
        # arrivee a une feuille (represente un caractere) : insertion dans la liste
        if root.isLeaf() :
            res[root.getLabel()] = path
            path = ""
        
        # parcours par recursivite, modification du path selon le chemin pris
        attrBitToChar(root.getLeftChild(), res, path + "0")
        attrBitToChar(root.getRightChild(), res, path + "1")
    return res

def compressionAlphabet(text) :
    """
    Creation d'un dictionnaire attribuant un bit a chaque caractere de l'alphabet

    Parametres : 
        text : chaine de caracteres correspondant au nom d'un fichier .txt
    
    Retourne :
        Dictionnaire dont les clés sont les caractères présents dans le fichier et leurs valeurs le bit associe
    """

    alphabet = sort_alphabet(create_alphabet(text))
    alphabet_file(text)
    l = treesList(alphabet)
    huffmanTree(l)
    return attrBitToChar(l[0])

def transcription(text) :
    """
    Creation du texte binaire base sur le fichier dont le nom est en paramètre

    Parametres : 
        text : chaine de caracteres correspondant au nom d'un fichier .txt
    
    Retourne :
        res : chaine de caracteres de 0 et 1 correspondant au texte du fichier
    """

    binTxt = ""
    f = open(text, 'r')
    charToBit = compressionAlphabet(text)
    lines = f.read().split("\n")
    for l in lines :
        for char in l :
            binTxt = binTxt + str(charToBit[char])


    f.close()
    return binTxt

def stringToBytes(string) :
    """
    Creation 

    Parametres : 
        text : chaine de caracteres correspondant au nom d'un fichier .txt
    
    Retourne :
        Dictionnaire dont les clés sont les caractères présents dans le fichier et leurs valeurs le bit associe
    """
    res = int(string, 2)
    length = (res.bit_length()+7) //8
    res = res.to_bytes(length, byteorder='big')
    return res

def compression(text) :
    """
    Creation du fichier compressé

    Parametres :
        text : chaine de caracteres correspondant au nom d'un fichier .txt

    Pas de retour, creation du fichier compressé du fichier en parametre

    """
    name = text.replace('.txt', '_comp.bin')
    fCompr = open(name, 'wb') 
    string = transcription(text)
    bits = stringToBytes(string)
    fCompr.write(bits)
    fCompr.close()


### TAUX DE COMPRESSION ###
    
def taux(fInit, fComp) :
    """
    Calcul du taux de compression obtenu 

    Parametres : 
        fInit : chaine de caracteres correspondant au nom du fichier avant compression
        fComp : chaine de caracteres correspondant au nom du fichier apres compression
    
    Retourne :
        Taux de compression obtenu

    """

    sizeInit = os.stat(fInit).st_size
    sizeComp = os.stat(fComp).st_size
    # tests :
    # print(f'Taille initiale : {sizeInit}')
    # print(f'Taille du fichier compressé : {sizeComp}')
    return (1-(sizeComp/sizeInit))


if __name__ == "__main__":
    file = "extraitalice.txt"
    compression(file)
    fileComp = file.replace('.txt', '_comp.bin')
    print(f'Taux de compression : {taux(file,fileComp)}')