# -*- coding: utf-8 -*-
"""
Created on Sun Jan 28 03:02:57 2018

@author: Ureridu
"""

l = [5, 3, 8, 7, 0, 0, 1, 2]

class BST:
    def __init__():
        self.tree = {}
        
    
    def add_node(node):
        pass
    
    def remove_node(node):
        pass
    
    
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 19 23:33:38 2017

@author: Ureridu
"""

a=2
d = {1: {2: 3, 4: {5: 7}}}


if a >= list(d.keys())[0]:
    print("asdf")


test = {}
ar = [ 8, 5, 9, 2, 3, 1, 0, 0, 4, 7, 23, 3, 75, 54, 98, 6, -1, 1000]
prev = None
inter=test
for i in ar[:]:
    inter=test
    prev = None
    print(i)
    if test != {}:
        while 1:
            print(inter)
            if inter != {}:
                print("not empty")
                depth = sorted(list(inter.keys()))
                left = depth[0]
                print('i is ', i, 'left is ', left, 'prev is', prev)

                if len(depth) == 2:
                    print('depth is 2')
                    right = depth[1]
                    if i < prev:
                        print('left')
                        inter = inter[left]
                        prev = left
                    else:
                        inter = inter[right]
                        prev = right
                        
                elif not prev:
                    print('right')
                    if len(depth) == 1:
                        inter = inter[left]
                        prev = left
                else:
                    if i > prev:
                        if left < prev:
                            inter[i] = {}
                            break
                        else:
                            inter = inter[left]
                            prev = left
                    else:
                        if left > prev:
                            inter[i] = {}
                            break
                        else:
                            inter = inter[left]
                            prev = left
                        
            else:
                inter[i] = {}
                break
    else:
        test[i] = {}

inter = test
out = []
prev = None
print('\n\n\n')

        
def flatten(inter, prev, out):
    keys = sorted(list(inter.keys()))
    print("keys", keys)
    print("inter", inter)
    if keys:
        for key in keys:
            print('key', key, 'prev', prev)
            if prev and prev < key:
                print('key', key, 'prev', prev)
                print('type prev', type(prev))
                print('out', out)
                out.append(prev)
            print('out', out)
            out, last = flatten(inter[key], key, out)
            print('last', last, 'key', key, 'prev', prev)
            if last is not None and prev is not None and prev >= key and last <= key:
                out.append(key)
            print('key', key, 'out', out)
            

    else:
        print('appending ', prev)
        out.append(prev)
        key = None
        print('out', out)
    
    return out, key

out = flatten(inter, prev, out)
        
            
