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
            self.root=Node(None, string)
            self._insert(self.root, string)
            print(self.print_tree())
            #self.Shannon(self.order)
            #print(self.reduced, self.created_nodes+1)
    
    order = ["A","B","C","D","E","F","G","H","I","J","K","L","M"]
    last_char = order[-1]
    second_to_last_char = order[-2]


    def _insert(self, parent, data):

        

        #if len(data)<=1:
         #  return

        if self.second_to_last_char not in data:
            #print(data)

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

       

        
                    
        #data_left = data[:len(data)//2]
        #data_right = data[len(data)//2:]
        data_left, data_right = self.Shannon(data)
        

        node = Node(parent, data_left)
        parent.left = node
        self._insert(node,node.data)

        node = Node(parent, data_right)
        parent.right = node
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


        print("data_left: ", data_left)
        print("data_right: ",data_right)
        print("\n")    

        if not data_left:   #keby to prefiltrovalo tak že by ostal prazdny retazec
            print("no data_left")
            if '!' in string:
                data_left = '1'
            else: 
                data_left = '0'
        
        if not data_right:
            print("no data_right")
            print(string)
            if '!' in string:
                data_right='1'
            else:
                data_right='0'

        print("filtered data_left: ", data_left)
        print("filtered data_right: ",data_right)
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
    string = "A.B.D.E.F.G.H.I.J.K.L.M+!A.B.!C.D.!E.F.!G.H.!I.J.!K.L.!M+!H.I.!J.K.!L.M+!A.B.C+A.!B.C.!D.E.F.G.!H.I.!J.K.!L.!M+!A.!B.!C.!D.!E.!F.!G.!H.!I.!J.!K.!L.!M"
    #string = [0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0,0,1,1,0,1,1,0,0]
    t = BDD(string)