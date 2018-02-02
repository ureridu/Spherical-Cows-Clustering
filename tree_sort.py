# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 03:02:57 2018

@author: Ureridu
"""
import time

class BST():
    first_node = None
    node_ref = {}

    def __init__(self, node=None, name=None):
        ''' The tree can be initialized to a list, a starting node, or nothing at all '''
        if type(node) == list:
            for i, n in enumerate(node):
                if name:
                    self.add_node(n, name[i])
                else:
                    self.add_node(n)
        else:
            if node:
                node = self.__tree_node__(self, node, name)
            self.first_node = node

    ''' This function iterates through the tree- left to right, and builds a sorted list '''
    def __recursive_search__(self, node, sorted_list):
        if node.left:
            sorted_list = self.__recursive_search__(node.left, sorted_list)
        sorted_list.append(node)
        if node.right:
            sorted_list = self.__recursive_search__(node.right, sorted_list)
        return sorted_list

    ''' Sometimes a tree has just gotta grow '''
    def add_node(self, new_node, name=None):
        new_node = self.__tree_node__(self, new_node, name)

        ''' Check if tree is empty, if not we will move through the tree, otherwise we now have node #1, WHOOOO.
            This is necessary as we allow for the initialization of an empty tree '''
        if self.first_node:
            node = self.first_node
            ''' Create recursive loop- every iteration we will move deeper into the tree, until the proper location is found
                At every step we will check if the new node is less than or greater than and equal to the current node,
                this determines if we move left or right.  Once an empty slot is found, we add the new node and exit the loop.'''
            while 1:
                # Move Left
                if new_node.value < node.value:
                    if node.left:
                        node = node.left
                    else:
                        node.left = new_node
                        new_node.parent = node
                        break
                # Move Right
                else:
                    if node.right:
                        node = node.right
                    else:
                        node.right = new_node
                        new_node.parent = node
                        break

        else:
            self.first_node = new_node

    ''' This function is used to delete nodes.  Basic form is that we connect the left child node to the appropriate
    leg of the parent, and set right child node to the furthest right leg of the left child- Thus removing the node from the tree '''
    def snip_node(self, node):
        if node.left:
            ' Only real difference is which leg of the parent we connect to '
            if node.value < node.parent.value:
                node.parent.left = node.left
            else:
                node.parent.right = node.left
            ' update the parent of the replacement node '
            node.left.parent = node.parent
            ' And run down the right leg until we find the end.  Then we dump the old right leg there'
            sub_node = node.left
            while sub_node.right:
                sub_node = sub_node.right

            sub_node.right = node.right

        else:
            ''' If there is not left node, life is great. We just snip out the node and shift the right node up
                no need to for any other shifting '''
            if node.value < node.parent.value:
                node.parent.left = node.right
            else:
                node.parent.right = node.right
            node.right.parent = node.parent

            del self.node_ref[node.name]
            del node

    ''' Sometimes it's just nice to have an ordered list. For, like, iterating and stuff
    a start node can be specified, allowing for partial lists'''
    def listify(self, start_node=None):
        if not start_node:
            start_node = self.first_node
        sorted_list = self.__recursive_search__(start_node, [])
        return sorted_list

    ''' This is the node class. Nodes have it. Are it. Truth
    Implemented as a sub-class of the tree because all nodes should belong to a tree
    The intent is that this class will only be called within methods of the tree
    future editions may enforce this.
    
    Node can be either a value only, or a value & name pairing '''
    class __tree_node__:
        def __init__(self, tree, node, name=None, parent=None, left=None, right=None):
            try:
                node = int(node)
            except:
                raise TypeError('Node Value must be int, or int convertible')
                  
            self.value = node       # This is the actual integer value of the node
            self.left = left        # A node instance whose value is less than that of the node's can go here
            self.right = right      # ditto, but greater than or equal to.
            self.parent = parent    # the parent node, used for snipping nodes from the tree
            self.name = name        # used to reference the node via the node reference dictionary
            
            ' update node ref with new node'
            tree.node_ref[name] = self

        ''' Returns a count of children in the node.  Can be used to determine if a node is full, half full or empty '''
        def child_count(self):
            count = 0
            if self.left:
                count += 1
            if self.right:
                count += 1
            return count
        
        





#
#test = {}
#ar = [ 8, 5, 9, 2, 3, 1, 0, 0, 4, 7, 23, 3, 75, 54, 98, 6, -3, 1000, -2]
#nr = ['node_'+str(x) for x in ar]
#'      -3, -2, 0, 0, 1, 2, 3, 3, 4, 5, 6, 7, 8, 9, 23, 54, 75, 98, 1000 '
#
#tree = BST(ar, nr)
#l = tree.listify()
#
#print(l[4].value)
#print(l[4].parent.value)
#tree.snip_node(l[4])
#tree.snip_node(l[5])
#tree.snip_node(l[9])
#print(l[4].value)
#print(l[4].parent.left.value)
#
#
#l = tree.listify()
#out = [x.value for x in l]
#print(out)




#node = None
#sub_dict=test
#for i in ar[:]:
#    sub_dict=test
#    node = None
#    print(i)
#    if sub_dict != {}:
#        while 1:
#            print(sub_dict)
#            if sub_dict != {}:
#                print("not empty")
#                depth = sorted(list(sub_dict.keys()))
#                left_child = depth[0]
#                print('i is ', i, 'left_child is ', left_child, 'node is', node)
#
#                if len(depth) == 2:
#                    print('depth is 2')
#                    right_child = depth[1]
#                    if i < node:
#                        print('left_child')
#                        sub_dict = sub_dict[left_child]
#                        node = left_child
#                    else:
#                        sub_dict = sub_dict[right_child]
#                        node = right_child
#                        
#                elif not node:
#                    print('right_child')
#                    if len(depth) == 1:
#                        sub_dict = sub_dict[left_child]
#                        node = left_child
#                else:
#                    if i > node:
#                        if left_child < node:
#                            sub_dict[i] = {}
#                            break
#                        else:
#                            sub_dict = sub_dict[left_child]
#                            node = left_child
#                    else:
#                        if left_child > node:
#                            sub_dict[i] = {}
#                            break
#                        else:
#                            sub_dict = sub_dict[left_child]
#                            node = left_child
#                        
#            else:
#                sub_dict[i] = {}
#                break
#    else:
#        sub_dict[i] = {}
#
#sub_dict = test
#out = []
#node = None
#print('\n\n\n')
#
#        
#def flatten(sub_dict, node, out):
#    keys = sorted(list(sub_dict.keys()))
#    print("keys", keys)
#    print("sub_dict", sub_dict)
#    if keys:
#        for key in keys:
#            print('key', key, 'node', node)
#            if node and node < key:
#                print('key', key, 'node', node)
#                print('type node', type(node))
#                print('out', out)
#                out.append(node)
#            print('out', out)
#            out, last = flatten(sub_dict[key], key, out)
#            print('last', last, 'key', key, 'node', node)
#            if last is not None and node is not None and node >= key and last <= key:
#                out.append(key)
#            print('key', key, 'out', out)
#            
#
#    else:
#        print('appending ', node)
#        out.append(node)
#        key = None
#        print('out', out)
#    
#    return out, key
#
#out = flatten(sub_dict, node, out)
        
            
