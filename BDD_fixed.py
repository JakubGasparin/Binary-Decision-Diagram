from random import random, randrange
from re import search
import time

class Node:
    def __init__(self, parent, data):
        self.data = data
        self.parent = parent
        self.left = None
        self.right = None

        if parent is None:
            self.height = 1
        else:
            self.height = self.parent.height+1  


class BDD: 
    def __init__(self, string):
            creationTime = time.perf_counter()
            self.root=Node(None, string)
            self._insert(self.root, string)                  
             
            print(self.print_tree())
            testerTime = time.perf_counter()
            self._test_search()
            print("### Statistics ###")
            print(f"Creation and print time: {creationTime}")  
            print(f"Total created nodes: {self.totalCreatedNodes}")
            print(f"Created new nodes: {self.createdNewNodes}")
            print(f"Reduced nodes: {self.reducedNodes}")
            print(f"Total reduction: { round((self.reducedNodes * 100 / self.totalCreatedNodes), 2) } %")
            print(f"Valid nodes: {self.totalTrueNodes}")
            print(f"Validity check: { True if self.createdNewNodes + self.reducedNodes == self.totalCreatedNodes else False} [Created new nodes({self.createdNewNodes}) + Reduced nodes({self.reducedNodes}) = TotalCreatedNodes({self.totalCreatedNodes})]")
            print(f"Duration of test: {testerTime-creationTime} seconds")
            print(f"Total duration of program: {testerTime+creationTime}")
            print("##################")
            #self.Shannon(self.order)
            #print(self.reduced, self.created_nodes+1)
            
    #order = order._orderGenerator()

    
    order = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]
    
    search_order = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]

    last_char = order[-1]
    second_to_last_char = order[-2]
    root = None
    vector = None
    noOfVariables = 0
    uniqueNodeDict = {}
    createdNewNodes = 0
    reducedNodes = 0
    totalCreatedNodes = 0
    totalTrueNodes = 0


    def _test_search(self):
        count = 0
        index = 0
        check = False

        while count !=100000:
            index = 0
            check = False
            for i in self.order:
                self.search_order[index] = randrange(0,2)
                index = index + 1
            
            check = self._search(self.search_order)
            if check is True:
                self.totalTrueNodes = self.totalTrueNodes+1
            count = count + 1

            
            #print(self.search_order)

    
    def _search(self, search_order):
        temp = self.root

        for i in range(len(search_order)):
            if search_order[i] == '0':
                temp=temp.left
            else:
                temp = temp.right
            
            if temp is not None and (temp.data == '0' or temp.data == '1'):
                #print("Data: ")
                #print(temp.data)
                return True   

        return False


    def _getUniqueNode(self, node):
        #print("got here")
        if(node.height not in self.uniqueNodeDict.keys()):
            return None
        for n in self.uniqueNodeDict[node.height]:
            if(n.data == node.data):
                self.reducedNodes = self.reducedNodes +1
                return n
        return None
    
    def _addUniqueNode(self, node):
        #print("got here")
        if(node.height not in self.uniqueNodeDict.keys()):
            self.uniqueNodeDict[node.height] = []

        if(not self._exists(node)):
            self.uniqueNodeDict[node.height].append(node)
            self.createdNewNodes = self.createdNewNodes + 1
            return True, node
        return False, self._getUniqueNode(node)

    def _exists(self, node):
        #print("got here")
        if(node.height not in self.uniqueNodeDict.keys()):
            return False
        for temp in self.uniqueNodeDict[node.height]:
            if(temp.data == node.data):
                return True
        return False

    def _insert(self, parent, data):

        if self.second_to_last_char not in data:

            if data == '1':
                data_left = '1'
                data_right = '1'
                node = Node(parent, data_left)
                parent.left = node
                node = Node(parent, data_right)
                parent.right = node
                return
            
            if data == '0':
                data_left = '0'
                data_right = '0'
                node = Node(parent, data_left)
                parent.left = node
                node = Node(parent, data_right)
                parent.right = node
                return

            if '+' in data:
                if '!' in data:
                    data_left = '1'
                    data_right = '1'
                    node = Node(parent, data_left)
                    parent.left = node
                    node = Node(parent, data_right)
                    parent.right = node
                    return  

                if '!' not in data:
                    data_left = '0'
                    data_right = '0'
                    node = Node(parent, data_left)
                    parent.left = node
                    node = Node(parent, data_right)
                    parent.right = node
                    return  

            else:

                if '!' not in data:
                    data_left = '1'
                    data_right = '0'

                    node = Node(parent, data_left)
                    parent.left = node

                    node = Node(parent, data_right)
                    parent.right = node

                    return
                
                if '!' in data:
                    data_left = '0'
                    data_right = '1'

                    node = Node(parent, data_left)
                    parent.left = node

                    node = Node(parent, data_right)
                    parent.right = node

                    return

            return                   
    
        data_left, data_right = self.Shannon(data)        

        node = Node(parent, data_left)
        self.totalCreatedNodes = self.totalCreatedNodes + 1
        result, n = self._addUniqueNode(node)
        parent.left = node if result else n
        self._insert(node,node.data)

        node = Node(parent, data_right)
        self.totalCreatedNodes = self.totalCreatedNodes + 1
        result, n = self._addUniqueNode(node)
        parent.right = node if result else n
        self._insert(node,node.data)
    
    def Shannon(self, string):
        char = self.order[0]
        data_left=[]
        data_right=[]

        for i in self.order:
            if char in string:
                break
            else:
                char = i

        count = string.count('+')

        index = 0
        i = 0
        f = 0

        while i != count:
            temp = string.split('+',1)
            temp = temp[0]

            temp2=string.split('+',1)
            temp2=temp2[1]

            string = temp2

            temp=temp.lstrip()
            temp2=temp2.lstrip()
            string=string.lstrip()

            index = 0

            if char in temp:
                for f in temp:
                    if temp[index] == char and temp[index-1]!='!':
                        data_right.append(temp)
                        data_right.append('+')
                    
                    if temp[index] == char and temp[index-1]=='!':
                        data_left.append(temp)
                        data_left.append('+')

                    index = index + 1

            else:
                data_left.append(temp)
                data_left.append('+')
                data_right.append(temp)
                data_right.append('+')

            i=i+1

        index = 0

        if string.count(char)==0:
            data_left.append(string)
            data_left.append('+')
            data_right.append(string)
            data_right.append('+')
        
        for i in string:
            if string[index]==char and string[index-1]!='!':
                data_right.append(string)
            if string[index]==char and string[index-1]=='!':
                data_left.append(string)
            
            index = index + 1

        if data_left:
            if (data_left[-1]=='+'):
                data_left.pop()
        if data_right:
            if (data_right[-1]=='+'):
                data_right.pop()

        data_left=self.listToString(data_left)
        data_right=self.listToString(data_right)

        data_left=self.filter(data_left, char)
        data_right=self.filter(data_right, char)


       # print("data_left: ", data_left)
        #print("data_right: ",data_right)
        #print("\n")    

        if not data_left:   #keby to prefiltrovalo tak že by ostal prazdny retazec
            #print("no data_left")
            if '!' in string:
                data_left = '1'
            else: 
                data_left = '0'
        
        if not data_right:
            #print("no data_right")
           # print(string)
            if '!' in string:
                data_right='1'
            else:
                data_right='0'

        #print("filtered data_left: ", data_left)
        #print("filtered data_right: ",data_right)
        #print("\n")    

        return data_left, data_right

    def filter(self,string, char):
        string = (string.replace('!.', '', ))
        string = (string.replace('.!'+char, '', ))
        string = (string.replace('!'+char+'.', '', ))
        string = (string.replace(char+'.', '', ))
        string = (string.replace('.'+char, '', ))
        string = (string.replace(char, '', ))

        return string



    def listToString(self, string):

            str1 = ""

            for ele in string:
                str1+=ele
            return str1

    def preorder_print(self, start, traversal):
        if start: 
            traversal += (str(start.data) + " - ")
            #traversal += (str(start.data) + " " + "height: " + (str(start.height)) + " - ")
            traversal = self.preorder_print(start.left, traversal)
            traversal = self.preorder_print(start.right, traversal)
        
        return traversal
    
    def print_tree(self):
        return self.preorder_print(self.root, "")

if __name__ == "__main__":
    string = "A.!C+A.B.C+!A.B+!B.C"
    string = "A.B.D.E.F.G.H.I.J.K.L.M+A.B.D.E.F.G.H.I.J.K.L.M+!A.B.!C.D.!E.F.!G.H.!I.J.!K.L.!M+!H.I.!J.K.!L.M+!A.B.C+A.!B.C.!D.E.F.G.!H.I.!J.K.!L.!M+!A.!B.!C.!D.!E.!F.!G.!H.!I.!J.!K.!L.!M"
    
    #string = [0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0]
    t = BDD(string)