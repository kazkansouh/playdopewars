#! /usr/bin/python

from state import State
import structure

from random import Random

import sys
import os

from joblib import Parallel, delayed
import multiprocessing
import threading

def mklimit(x,y) :
    return { 'low' : x , 'high' : y }

limits = [ mklimit(2,18)
#           , mklimit(18,54)
#           , mklimit(4,9)
#           , mklimit(10,25)
#           , mklimit(1,7)
]

def items(r) :
    item = []
    for limit in limits :
        item.append(r.randint(limit['low'],limit['high']))
    return item

# variables = {
#     'citem1' : 0, 'citem2' : 0, 'citem3' : 0, 'citem4' : 0, 'citem5' : 0,
#     'iitem1' : 0, 'iitem2' : 0, 'iitem3' : 0, 'iitem4' : 0, 'iitem5' : 0,
#     'vitem1' : 0, 'vitem2' : 0, 'vitem3' : 0, 'vitem4' : 0, 'vitem5' : 0,
#     'money' : 0, 'item' : 0
# }

variables = {
    'citem1' : 0,
    'iitem1' : 0,
    'vitem1' : 0,
    'money' : 0,
}

def playgame(tree) :
    s = State()
    r = Random(100)

    for v in variables :
        variables[v] = 0

    while not s.finished() :

        matrix = items(r)
        print matrix
        s.showinventory()
    
        variables['citem1'] = matrix[0]
        # variables['citem2'] = matrix[1]
        # variables['citem3'] = matrix[2]
        # variables['citem4'] = matrix[3]
        # variables['citem5'] = matrix[4]
        for item in s.bag :
            variables['iitem' + str(item + 1)] = s.bag[item]['amount']
            variables['vitem' + str(item + 1)] = int(s.bag[item]['value'])
        variables['money'] = s.money

        print variables

        for item in range(0,len(matrix)) :
            #variables['item'] = item
            result = structure.execCommand(tree, variables)
            print ">> " + result
            result = result.split()
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

trees = []

def playgame_main(t) :
    global trees
    try :
        trees[t]['score'] = 0
        trees[t]['score'] = playgame(trees[t]['cmd'])
        print "tree scored: " + str(trees[t]['score'])
    except ZeroDivisionError :
        print "tree failed"
    return (t,trees[t]['score'])

showtree = False
close = False

def thread_start() :
    global showtree
    global close
    while not close :
        print "waiting"
        if sys.stdin.readline().strip() == "close" :
            close = True
        else :
            showtree = True

def main() :
    r = Random()
    
    global trees
    global showtree
    global close

# uncomment the below code to run through a handmade tree

#    print structure.strCommand(structure.handmade)
#    playgame(structure.handmade)
#    return 1

# comment the following line to prevent boostrapping the process with
# a handcrafted structure
    trees.append({'cmd':structure.handmade,'score':0})

    for i in range(1,400) :
        trees.append({'cmd': structure.generateCommand(r, variables.keys()) , 'score': 0})

    print "Generated trees"

    cores = multiprocessing.cpu_count()
    null = open(os.devnull, 'w')
    stdout = sys.stdout

    thread = threading.Thread(target=thread_start)
    thread.start()

    for i in range(1,1000) :
        sys.stdout = null
        scores = Parallel(n_jobs=cores)(delayed(playgame_main)(j) for j in range(0,len(trees)))
        #for j in range(0,len(trees)) :
            #playgame_main(j)
        sys.stdout = stdout

        for x in scores :
            trees[x[0]]['score'] = x[1]

        print "------------"
        print str(i) + ") best trees: "
        trees.sort(lambda x, y: cmp(y['score'],x['score']))
        print str(trees[0]['score']) + " and " + str(trees[1]['score'])

        if showtree :
            print structure.strCommand(trees[0]['cmd'])
            showtree = False

        
        tree1 = trees[0]['cmd']
        tree2 = trees[1]['cmd']
        tree3 = trees[2]['cmd']
        tree4 = trees[3]['cmd']
        tree5 = trees[4]['cmd']

        trees = [ 
            trees[0], 
            trees[1],
        ]

        for j in range(1,100) :
            trees.append({ 
                'cmd' : structure.mutateCommand(r, variables.keys(), tree1),
                'score' : 0})
            trees.append({
                'cmd' : structure.mutateCommand(r, variables.keys(), tree2),
                'score' : 0})
            trees.append({
                'cmd' : structure.mutateCommand(r, variables.keys(), tree3),
                'score' : 0})
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

    print "------------"
    print structure.strCommand(trees[0]['cmd'])
    print "------------"
    playgame(trees[0]['cmd'])
    print "------------"

    close = True

if __name__ == "__main__":
    main()
