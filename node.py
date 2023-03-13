class Node : 
    
    def __init__(self, label, freq, leftChild = None, rightChild = None) :
        self.label = label
        self.freq = freq
        self.leftChild = leftChild
        self.rightChild = rightChild
        self.path = None

    def __str__(self) :
        return self.label + " : " + str(self.freq)
    
    def __repr__(self):
        return self.__str__()
    
    # getters

    def getLabel(self):
        return self.label
    
    def getFreq(self):
        return self.freq
    
    def getLeftChild(self) :
        return self.leftChild
    
    def getRightChild(self) : 
        return self.rightChild
    
    #setters
    
    def setLabel(self, string) : 
        self.label = string

    def setFreq(self, nb) :
        self.freq = nb
    
    def setLeftChild(self, other) : 
        self.leftChild = other

    def setRightChild(self, other) :
        self.rightChild = other

    def isLeaf(self) :
        return (self.leftChild == None and self.rightChild == None)