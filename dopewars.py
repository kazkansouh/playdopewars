#! /usr/bin/python

from state import State
import structure

from random import Random

from sys import stdin

def mklimit(x,y) :
    return { 'low' : x , 'high' : y }

limits = [ mklimit(2,18)
           , mklimit(18,54)
           , mklimit(4,9)
           , mklimit(10,25)
           , mklimit(1,7)
]

def items() :
    item = []
    r = Random()
    for limit in limits :
        item.append(r.randint(limit['low'],limit['high']))
    return item

variables = {
    'citem1' : 0, 'citem2' : 0, 'citem3' : 0, 'citem4' : 0, 'citem5' : 0,
    'iitem1' : 0, 'iitem2' : 0, 'iitem3' : 0, 'iitem4' : 0, 'iitem5' : 0,
    'vitem1' : 0, 'vitem2' : 0, 'vitem3' : 0, 'vitem4' : 0, 'vitem5' : 0,
    'money' : 0, 'item' : 0
}

def playgame(tree) :
    s = State()

    for v in variables :
        variables[v] = 0

    while not s.finished() :

        matrix = items()
        print matrix
        s.showinventory()
    
        variables['citem1'] = matrix[0]
        variables['citem2'] = matrix[1]
        variables['citem3'] = matrix[2]
        variables['citem4'] = matrix[3]
        variables['citem5'] = matrix[4]
        for item in s.bag :
            variables['iitem' + str(item + 1)] = s.bag[item]['amount']
            variables['vitem' + str(item + 1)] = int(s.bag[item]['value'])
        variables['money'] = s.money

        for item in range(0,len(matrix)) :
            variables['item'] = item
            result = structure.execCommand(tree, variables).split()
            if result[0] == "buy" :
                a = int(result[1])
                if a < 0 :
                    s.sell(item, a*-1, matrix)
                else :
                    s.buy(item, a, matrix)
            if result[0] == "sell" :
                a = int(result[1])
                if a > 0 :
                    s.sell(item, a, matrix)
                else :
                    s.buy(item, a*-1, matrix)

        s.endday()

    return s.money


def main() :

    r = Random()

    trees = []
    for i in range(1,25) :
        trees.append({'cmd': structure.generateCommand(r, variables.keys()) , 'score': 0})

    for i in range(1,4) :

        for tree in trees :
            try :
                score = playgame(tree['cmd'])
                print "tree scored: " + str(score)
                tree['score'] = score
            except ZeroDivisionError :
                print "tree failed"

        print "------------"
        print "best trees: "
        trees.sort(lambda x, y: cmp(y['score'],x['score']))
        print str(trees[0]['score']) + " and " + str(trees[1]['score'])

        tree1 = trees[0]['cmd']
        tree2 = trees[1]['cmd']
        tree3 = trees[2]['cmd']
        tree4 = trees[3]['cmd']
        tree5 = trees[4]['cmd']

        trees = []

        for j in range(1,25) :
            trees.append({
                'cmd': structure.crossCommand(r, tree1, tree2) ,
                'score': 0})
            trees.append({
                'cmd': structure.crossCommand(r, tree2, tree1) ,
                'score': 0})
            trees.append({
                'cmd': structure.crossCommand(r, tree3, tree4) ,
                'score': 0})
            trees.append({
                'cmd': structure.crossCommand(r, tree3, tree4) ,
                'score': 0})
            trees.append({
                'cmd': structure.crossCommand(r, tree5, tree1) ,
                'score': 0})
            trees.append({
                'cmd': structure.crossCommand(r, tree1, tree5) ,
                'score': 0})



#     s = State()


#     tree = 

# #    trees = []

#     while not s.finished() :
#         # iterate over table, for each item decide on action (buy,
#         # sell, none)
#         matrix = items()

#         print matrix
#         s.showinventory()

#         for item in range(0,len(matrix)) :
#             # decide, given inputs
#             print "item: " + str(item)
#             print "action? [b/s/n]"
#             l = stdin.readline()
#             if l.strip() == "b" :
#                 print "how much?"
#                 a = stdin.readline()
#                 s.buy(item, int(a), matrix)
#             elif l.strip() == "s" :
#                 print "how much?"
#                 a = stdin.readline()
#                 s.sell(item, int(a), matrix)
#             else :
#                 print "skip"

#         s.endday()

if __name__ == "__main__":
    main()
