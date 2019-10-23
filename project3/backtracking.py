#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 04:20:39 2019
Working:
    All var choice cases are working along with fw_check
Errors and bugs:
    AC3 is popping off every constraint, need to figure out why, something to do with revise
    Sudoku is still failing every run
@author: carsonellsworth
"""
from csp2 import csp,var
from random import choice as rdch
import math

ac_count = 0

def backtracking(assignment,CSP:csp,method=0,fw_check=False,ac_3=False,count_lim=0):

    if (is_complete(assignment,CSP)):
        for key in assignment:
            v = assignment[key]
            print(v.ID,v.domain)
        print(len(assignment))
        return assignment
    v = select_unassigned_variable(CSP,assignment,method)
    #print("BT: var select:",v.ID,v.domain)
    if(type(v) == type(None)):
        print(CSP.varset)
        return "Failure"
    for value in order_domain_values(v,assignment,CSP):
        #print("BT: var ID: {} value: {} domain: {}\n".format(v.ID,value,v.domain))
        if is_consistent(value,v,assignment,CSP):
            v.domain = set([value])
            assignment[v.ID] = v
            infer = {}
            infer = inferences(infer,assignment,v,value,CSP,fw_check,ac_3,count_lim)
            if (infer != "Failure"):
                result = backtracking(assignment,CSP,method,fw_check,ac_3,count_lim)
                if(result != "Failure"):
                    return result
            if(v.ID in assignment):
                if(v.inferences):
                    for key in v.inferences:
                        inf_var = v.inferences[key]
                        inf_var.domain = CSP.domain.copy()
                    v.inferences.clear()
                v.domain = CSP.domain.copy()
                assignment.pop(v.ID)

    return "Failure"



def select_unassigned_variable(CSP:csp,assignment:set,method=0):
    """
    csp is the list of variables that are to be selected
    method is the method type in which they are selected
        0:random #the default option
        1:minimum-remaining value
        2:minimum-remaining value together with degree
    """
    if(method not in range(3)):
        return "method out of bounds"


    if(method == 0):
        key_lst = list(CSP.varset.keys())
        v = CSP.varset[rdch(key_lst)]
        #while variable not eligable for selection
        while(v.ID in assignment or len(v.domain) < 1):
            #keep guessing
            v = CSP.varset[rdch(list(CSP.varset.keys()))]
        return v

    elif(method == 1):
        #1:minimum-remaining value
        least_domain = math.inf
        low_var = None
        for variables in CSP.varset:
            v = CSP.varset[variables]
            if(v == None):
                print("Nonetype err:",CSP.varset)
            dm_size = len(v.domain)
            if(v.ID not in assignment and dm_size >= 1):

                if(dm_size < least_domain):
                    least_domain = dm_size
                    if(dm_size == 1):
                        return v
                    low_var = v
            if(dm_size == 0):
                return None
        return low_var

    elif(method == 2):
        #2:minimum-remaining value together with degree
        #the degree of the node works as a tie breaker, otherwise it works
        #just like minimum remaining value
        least_domain = math.inf
        low_var = None
        for variables in CSP.varset:
            v = CSP.varset[variables]
            if(v == None):
                print("Nonetype err:",CSP.varset)
            dm_size = len(v.domain)
            if(v.ID not in assignment and dm_size >= 1):

                if(dm_size < least_domain):
                    least_domain = dm_size
                    if(dm_size == 1):
                        return v
                    low_var = v
                elif(dm_size == least_domain and len(v.constraints) > len(low_var.constraints)):
                    least_domain = dm_size
                    low_var = v
            if(dm_size == 0):
                return None
        return low_var



def inferences(infer, assignment, var, value,CSP,fw_check,ac_3,count_lim):
    global ac_count
    if(ac_3 and ac_count < count_lim):
        #print("running AC3")
        print("CSP constraint:",CSP.constraint)
        ac3(CSP)
        print("CSP constraint:",CSP.constraint)
        redef_constraints(CSP)
        ac_count += 1
    if(fw_check):
        infer = forward_check(infer, assignment, var, value,CSP)
        return infer
    return True



def forward_check(infer:dict, assignment, var, value,CSP):
    #look at var constraints and reduce domain
    for _,con_id in var.constraints:

        if(con_id not in assignment):
            #grab constraint variable from var
            con_v = CSP.varset[con_id]
            if(var.domain <= con_v.domain):
                if(len(con_v.domain) > 1):
                    #take away var.value from domain
                    #print("FC: having {} take {} away from {} {}\n".format(var.ID,var.domain,con_v.ID,con_v.domain))
                    con_v.domain = con_v.domain - var.domain
                    infer[con_id] = con_v
                    var.inferences[con_id] = con_v
                else:
                    return "Failure"

    return infer



def ac3(CSP:csp):
    arcs = CSP.constraint
    while(arcs):
        x1,x2 = arcs.pop()
        X1 = CSP.varset[x1]
        X2 = CSP.varset[x2]
        #print("revising")
        if(revise(CSP,X1,X2)):
            if (len(X1.domain) <= 1):
                #X1.domain = CSP.domain.copy()
                return False

            for _,xk in X1.constraints - set([(X1.ID,X2.ID)]):
                #print("adding arc:",(xk,X1.ID))
                arcs.add((xk,X1.ID))
        else:
            #print("no revising needed")
            pass
    return True



def revise(CSP:csp,X1:var,X2:var):
    revised = False
    no_del = False
    removals = set([])
    #print(X1.ID,X1.domain,X2.ID,X2.domain)

    for d1 in X1.domain:

        for d2 in X2.domain:
            if((X1.ID,X2.ID) in X1.constraints and CSP.diff(d1,d2)):
                #print("{} is diff {}: {}".format(d1,d2,CSP.diff(d1,d2)))
                no_del = True
        if(not no_del):
            removals.add(d1)
            print("RV: var: {}'s removal set {}".format(X1.ID,removals))
            revised = True
    X1.domain = X1.domain - removals
    return revised






def order_domain_values(var,assignment,csp):
    """
    The order in which the domain values should be tried as a feasable option
    """
    #right now it works only as just convert value and return
    #no special black magic yet
    return var.domain


def redef_constraints(CSP:csp):
    for vkey in CSP.varset:
        v = CSP.varset[vkey]
        v.constraints.clear()
        for vid,oid in CSP.constraint:
            if(v.ID == vid):
                v.constraints.add((vid,oid))





def is_consistent(value,v,assignment,CSP:csp):
    #must look through constraints
    if(v.ID not in assignment):
        for ID,item in v.constraints:
            if(item in assignment):
                o = assignment[item]
                #print("IC: ID: {} {} | item {} {}".format(ID,value,item,o.domain))
                is_diff = CSP.diff(set([value]),o.domain)
                #print(is_diff)
                if(not is_diff):#item[1] is the key for var constraints
                    return False
        return True
    return False


def is_complete(assignment,CSP:csp):
    return set(assignment.keys()) == set(CSP.varset.keys())





def id_to_cell(ID:str):
    if (len(ID) != 2):
        return "Failure"
    return (ord(ID[0])-97)*9+int(ID[1])-1

def cell_to_id(cell:int):
    if(cell not in range(0,81)):
        return "Failure"
    id1 = cell % 9
    id0 = cell - id1

    return (chr(int(id0/9) + 97) + str(id1+1))

def sudoku_row(ID:str,sudo_col):
    #return row IDs
    tmp = []
    if (len(ID) != 2):
        return "Failure"
    for x in sudo_col:
        tmp.append(ID[0]+str(x))
    return tmp

def sudoku_column(ID:str,sudo_row):
    #return column IDs
    tmp = []
    if (len(ID) != 2):
        return "Failure"
    for x in sudo_row:
        tmp.append(x+ID[1])
    return tmp

def element_add(lst:list,val:int):
    l = lst.copy()
    for y in range(len(l)):
        if(type(l[y]) == str):
            l[y] = cell_to_id(id_to_cell(l[y])+val)
        else:
            l[y] += val
    return l




import json

def data_translator_map(f:str):
    csp_map={}
    with open(f,'r') as f:
        csp_map = json.load(f)
    return csp_map

def data_translator_sudoku(f:str):
    csp_sudo=[]
    with open(f,'r') as f:
        csp_sudo = json.load(f)
    return csp_sudo

def print_sudoku(sudoku_list:list):
    lister = ""
    counter = 0
    for x in sudoku_list:
        for y in range(len(x)):
            if (y%9==0):
                lister+='\n' + "|"+str(x[y])
            elif (y%3==0):
                lister+="|" + str(x[y])
            else:
                lister+=str(x[y])
        counter+=1
        if(counter%3 == 0):
            lister+='\n------------'
    print(lister)








if(__name__ =="__main__"):
    import sys , time
    bt_counter = 0
    old_recurse_depth_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(40000)
    map_color = data_translator_map('gcp.json')
    map_domain = set(['r','g','b','y'])
    map_varset = {}
    map_ass = {}
    for x in range(map_color["num_points"]):
       map_varset[x] = var(x,None,map_domain.copy())
    map_csp = csp(map_varset,map_domain,map_color["edges"])
    map_csp.create_var_constraint()

    sudoku_solver = data_translator_sudoku('sudoku.json') #the json sudoku list where 0 is a cell that needs to be filled
    sudoku_domain = set([x for x in range(1,10)]) #set of 1-9 that a variable is allowed to be
    sudo_varset = {} #the variable set in the csp
    sudo_ass = {} #the assignment set in csp

    sudo_row = ['a','b','c','d','e','f','g','h','i']
    sudo_col = [str(x) for x in range(1,10)]
    sudo_subgrid = ['a1','a2','a3','b1','b2','b3','c1','c2','c3']
    sudo_gridincr = [0,3,6,27,30,33,54,57,60]#sg 0,1,2,3,4,5,6,7,8

    #creating the variables with proper cell names a1-i9
    for letter in sudo_row:
        for num in sudo_col:
            sudo_varset[letter+num] = var(ID=letter+num,value = None,domain = sudoku_domain.copy())


    #already set variables
    c = 0
    zero_count=0
    for i in range(len(sudoku_solver)):
        for j in range(len(sudoku_solver)):
            #if the sudoku element is not zero then add them to the assignment set
            if(sudoku_solver[i][j] != 0):
                vid = cell_to_id(c) #variable ID
                v = sudo_varset[vid]
                v.domain.clear()
                v.domain = set([sudoku_solver[i][j]])
                sudo_ass[v.ID] = v
                #print("v {} domain:".format(v.ID),v.domain)
            else:
                zero_count+=1
            c += 1

    sudo_csp = csp(sudo_varset,sudoku_domain,None)
    #variable constraints
    for v in sudo_varset:
        #make the row constraints
        var = sudo_varset[v]
        for name in sudoku_row(var.ID,sudo_col):
            #name is an ID name for a variable
            if(var.ID == name or (var.ID,name) in var.constraints):
                pass
            else:
                var.constraints.add((var.ID,name))

        #make column constraints
        for name in sudoku_column(var.ID,sudo_row):
            #name is an ID name for a variable
            if(var.ID == name or (var.ID,name) in var.constraints):
                pass
            else:
                var.constraints.add((var.ID,name))

        #make grid constraints

        ##### ERROR IN SUBGRID CREATION #####


        #####################################
        for x in sudo_gridincr:
            l=element_add(sudo_subgrid,x)
            if(v in l):
                for item in l:
                    if(v != item):
                        var.constraints.add((v,item))






    ##### handle system parameters
    ac3_count_lim = int(sys.argv[4])
    fw_check = bool(int(sys.argv[3]))
    search_method=int(sys.argv[2])
    search_mtd =""
    if(search_method == 0):
        search_mtd = "random search"
    elif(search_method == 1):
        search_mtd = "MRV"
    else:
        search_mtd = "MRV w/ highest Degree"



    ################## Start Backtracking ###################
    if(sys.argv[1].upper()=='MAP'):
        f = open('proj3MAP.csv','a')
        start_time = time.time()
        print(backtracking(map_ass,map_csp,search_method,fw_check = fw_check,ac_3=True))
        end_time = time.time()
        fin_time = end_time - start_time
        f.write("{},s,{},search method,fw_checking,{},ac3_count_lim,{},initial nodes,{}\n".format(fin_time,search_mtd,fw_check,ac3_count_lim,map_color["num_points"]))
        f.close()
    else:
        f = open('proj3SUDO.csv','a')
        start_time = time.time()
        print(backtracking(sudo_ass,sudo_csp,search_method,fw_check=fw_check,ac_3=True))
        end_time = time.time()
        fin_time = end_time - start_time
        f.write("{},s,{},search method,fw_checking,{},ac3_count_lim,{},initial empty cells,{}\n".format(fin_time,search_mtd,fw_check,ac3_count_lim,zero_count))
        f.close()
        tmp = [sudo_ass[cell_to_id(x)].domain.pop() for x in range(len(sudo_ass))]

        counter = 0
        lstcounter = -1
        tmp1 = []
        for x in range(len(tmp)):
            if(counter%9==0):
                tmp1.append([])
                lstcounter+=1
            tmp1[lstcounter].append(tmp[x])
            counter+=1
        print_sudoku(tmp1)


    print("time taken to run {}".format(fin_time))








    sys.setrecursionlimit(old_recurse_depth_limit)
