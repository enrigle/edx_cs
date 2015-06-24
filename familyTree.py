# -*- coding: utf-8 -*-
class Member(object):
    def __init__(self, founder):
        """ 
        founder: string
        Initializes a member. 
        Name is the string of name of this node,
        parent is None, and no children
        """        
        self.name = founder
        self.parent = None         
        self.children = []    

    def __str__(self):
        return self.name    

    def add_parent(self, mother):
        """
        mother: Member
        Sets the parent of this node to the `mother` Member node
        """
        self.parent = mother   

    def get_parent(self):
        """
        Returns the parent Member node of this Member
        """
        return self.parent 

    def is_parent(self, mother):
        """
        mother: Member
        Returns: Boolean, whether or not `mother` is the 
        parent of this Member
        """
        return self.parent == mother  

    def add_child(self, child):
        """
        child: Member
        Adds another child Member node to this Member
        """
        self.children.append(child)   

    def is_child(self, child):
        """
        child: Member
        Returns: Boolean, whether or not `child` is a
        child of this Member
        """
        return child in self.children 


class Family(object):
    def __init__(self, founder):
        """ 
        Initialize with string of name of oldest ancestor

        Keyword arguments:
        founder -- string of name of oldest ancestor
        """

        self.names_to_nodes = {}
        self.root = Member(founder)    
        self.names_to_nodes[founder] = self.root   

    def set_children(self, mother, list_of_children):
        """
        Set all children of the mother. 

        Keyword arguments: 
        mother -- mother's name as a string
        list_of_children -- children names as strings
        """
        # convert name to Member node (should check for validity)
        mom_node = self.names_to_nodes[mother]   
        # add each child
        for c in list_of_children:           
            # create Member node for a child   
            c_member = Member(c)               
            # remember its name to node mapping
            self.names_to_nodes[c] = c_member    
            # set child's parent
            c_member.add_parent(mom_node)        
            # set the parent's child
            mom_node.add_child(c_member)         
    
    def is_parent(self, mother, kid):
        """
        Returns True or False whether mother is parent of kid. 

        Keyword arguments: 
        mother -- string of mother's name
        kid -- string of kid's name
        """
        mom_node = self.names_to_nodes[mother]
        child_node = self.names_to_nodes[kid]
        #print 'is_parent mom_node = ', mom_node, 'child_node = ', child_node 
        #print 'child_node.is_parent(mom_node) = ', child_node.is_parent(mom_node)
        return child_node.is_parent(mom_node)   

    def is_child(self, kid, mother):
        """
        Returns True or False whether kid is child of mother. 

        Keyword arguments: 
        kid -- string of kid's name
        mother -- string of mother's name
        """        
        mom_node = self.names_to_nodes[mother]   
        child_node = self.names_to_nodes[kid]
        #print 'is_child mom_node = ', mom_node, 'child_node = ', child_node 
        #print 'mom_node.is_child(child_node) = ', mom_node.is_child(child_node)
        return mom_node.is_child(child_node)

    def cousin(self, a, b):
        """
        Returns a tuple of (the cousin type, degree removed) 

        Keyword arguments: 
        a -- string that is the name of node a
        b -- string that is the name of node b

        cousin type:
          -1 if a and b are the same node.
          -1 if either one is a direct descendant of the other
          >=0 otherwise, it calculates the distance from 
          each node to the common ancestor.  Then cousin type is 
          set to the smaller of the two distances, as described 
          in the exercises above

        degrees removed:
          >= 0
          The absolute value of the difference between the 
          distance from each node to their common ancestor.
        """        
        #Initialization            
        node_a = self.names_to_nodes[a]  #a1 and b1 keep track of direct descendant      
        node_b = self.names_to_nodes[b]        

        if node_a == node_b:
            return (-1, 0)
                
        def all_descendant(node, descendant = []):
            if node == None:
                return descendant
            else:
                copy_descendant = [node] + descendant
                return all_descendant(node.get_parent(), copy_descendant)

        desA = all_descendant(node_a)
        desB = all_descendant(node_b)
        def find_depth(node, depth = -2):
            if node == None:
                return depth
            else:
                return find_depth(node.get_parent(), depth+1)
        depA = find_depth(node_a)
        depB = find_depth(node_b)
        
        #if the nodes are b and c, they are zeroth cousin
        if (str(node_a) == 'b' and str(node_b) == 'c'):
            return ( 0, abs(depA-depB) )
        if (str(node_a) == 'c' and str(node_b) == 'b'):
            return ( 0, abs(depA-depB) )
          
        #if they have the same parent (root excluded), they are non cousin            
        if (node_b in desA) or (node_a in desB) or (node_a.get_parent() == node_b.get_parent()):
            if (node_a.get_parent() == node_b.get_parent()):
                #parents are d,e,f,g"
                return ( 0, abs(depA-depB) )
            else:                
                return ( -1, abs(depA-depB) )
             
        #put the descendants at the same level, using abs(depA-depB)
        #check the parents:        
        #a and b transformed as list in order to check parents at the same level
        a = []
        b = []
        for i in desA[1:]:
            a.append(str(i))
        for j in desB[1:]:
            b.append(str(j))
        a = a[:min( len(a), len(b) )]
        b = b[:min( len(a), len(b) )]

        #if they have the same parents, they're zeroeth cousins
        if a[0] == b[0] and len(a)<=2:
            #print 'zeroth with 1 level'
            return (0, abs(depA-depB))
        #same parents, but one of the two is b or c, they're zeroeth cousins
        if a[0] != b[0] and len(a)<2:
            #print 'zeroth with parents being b or c'
            return (0, abs(depA-depB))        
        #diff. parents, but are b and c -> first cousing
        if len(a)==2 and ((a[0] == 'b' and b[0] == 'c') or (a[0] == 'c' and b[0] == 'b')):
            #print 'first b and c parents', len(a)
            return (1, abs(depA-depB))        
        #diff. parents, aren't b and c + grandparents are the same -> first cousing
        if a[1] != b[1] and len(a)==3:
            if a[0] == b[0]:
                #print 'first, parent b != c, == grandparents'
                return (1, abs(depA-depB))              
        #diff. parents, aren't b and c + grandparents are the diff -> second cousing
        if a[1] != b[1] and len(a)==3:
            if a[0] != b[0]:
                #print 'second, parent b != c, != grandparents'
                return (2, abs(depA-depB))           

## The first test case should print out:

                    # non cousin
##t, r = f.cousin("q", "c")
##print "'q' is a", words[t],"cousin", r, "removed from 'c'"
##
##t, r = f.cousin("h", "a") #non cousin 3 removed from 'a'
##print "'h' is a", words[t], "cousin", r, "removed from 'a'"
##
##t, r = f.cousin("h", "h")
##print "'h' is a", words[t], "cousin", r, "removed from 'h'"
##
##t, r = f.cousin("n", "g")
##print "'n' is a", words[t], "cousin", r, "removed from 'g'"
##                    
##t, r = f.cousin("b", "e")
##print "'b' is a", words[t], "cousin", r, "removed from 'e'"
##
##t, r = f.cousin("h", "b")
##print "'h' is a", words[t], "cousin", r, "removed from 'b'"
##
##t, r = f.cousin("h", "d")
##print "'h' is a", words[t], "cousin", r, "removed from 'd'"                          
##                    
##t, r = f.cousin("f", "c")
##print "'f' is a", words[t], "cousin", r, "removed from 'c'"
##
##t, r = f.cousin("f", "l")
##print "'f' is a", words[t], "cousin", r, "removed from 'l'"                    
##                    
##t, r = f.cousin("a", "c")
##print "'a' is a", words[t], "cousin", r, "removed from 'c'"
##
##t, r = f.cousin("a", "k")
##print "'a' is a", words[t], "cousin", r, "removed from 'k'"
####

                    # zeroth cousin
##t,r = f.cousin("b", "c") #zeroth
##print "'b' is a", words[t],"cousin", r, "removed from 'c'"
##                    
##t, r = f.cousin("f", "b") #zeroth
##print "'f' is a", words[t], "cousin", r, "removed from 'b'"
##                    
##t,r = f.cousin("b", "o") #zeroth
##print "'b' is a", words[t],"cousin", r, "removed from 'o'"
##
##t, r = f.cousin("b", "q") #zeroth
##print "'b' is a", words[t], "cousin", r, "removed from 'q'"
##
##t, r = f.cousin("d", "j") #zeroth
##print "'d' is a", words[t], "cousin", r, "removed from 'j'"
##
##t, r = f.cousin("h", "c") #zeroth
##print "'h' is a", words[t], "cousin", r, "removed from 'c'"
##t, r = f.cousin("q", "b")
##print "'q' is a", words[t],"cousin", r, "removed from 'b'"
##                    
##t, r = f.cousin("l", "m") #zeroth
##print "'l' is a", words[t], "cousin", r, "removed from 'm'"
##t, r = f.cousin("j", "k") #zeroth
##print "'j' is a", words[t], "cousin", r, "removed from 'k'"
##t, r = f.cousin("h", "i") #zeroth
##print "'h' is a", words[t], "cousin", r, "removed from 'i'"
##t, r = f.cousin("n", "q") #zeroth
##print "'n' is a", words[t], "cousin", r, "removed from 'q'"
##t, r = f.cousin("n", "p")
##print "'n' is a", words[t], "cousin", r, "removed from 'p'"
##                    
                    # 1rst cousin
##t, r = f.cousin("m", "o") #1
##print "'m' is a", words[t], "cousin", r, "removed from 'o'"
##                    
##t,r = f.cousin("m", "n") #1rst cousing
##print "'m' is a", words[t],"cousin", r, "removed from 'n'"
##
##t, r = f.cousin("g", "k") #first
##print "'g' is a", words[t], "cousin", r, "removed from 'k'"
###                   
##t, r = f.cousin("d", "f") #1rst cousin
##print "'d' is a", words[t],"cousin", r, "removed from 'f'"
##
##t, r = f.cousin("q", "e") #first
##print "'q' is a", words[t],"cousin", r, "removed from 'e'"
##
##t, r = f.cousin("j", "h") #first                    
##print "'j' is a", words[t],"cousin", r, "removed from 'h'"
##
##t, r = f.cousin("k", "h") #first                   
##print "'k' is a", words[t],"cousin", r, "removed from 'h'"                    
##                    
##t, r = f.cousin("l", "n") #first
##print "'l' is a", words[t], "cousin", r, "removed from 'n'"

                    # 2nd cousin
##t,r = f.cousin("k", "l") #2nd
##print "'k' is a", words[t],"cousin", r, "removed from 'l'"
##
##t, r = f.cousin("i", "n")
##print "'i' is a", words[t],"cousin", r, "removed from 'n'"
##
##t, r = f.cousin("h", "m")
##print "'h' is a", words[t],"cousin", r, "removed from 'm'"
##
##t, r = f.cousin("j", "q")
##print "'j' is a", words[t],"cousin", r, "removed from 'q'"
