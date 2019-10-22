#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 04:20:39 2019
Errors and bugs:
    running into set changing size during runtime, most likely due to a recursed variable says no bitch to our variable
@author: carsonellsworth
"""
from csp2 import *
from random import choice as rdch
import math
import threading

ac_flag = False

def backtracking(assignment,CSP:csp,method=0,fw_check=False,ac_3=False):
    #print(len(assignment))
    if (is_complete(assignment,CSP)):
        for key in assignment:
            v = assignment[key]
            print(v.ID,v.domain)
        print(len(assignment))
        return assignment
    v = select_unassigned_variable(CSP,assignment,method)
    #print("BT: var select:",v.ID,v.domain)
    if(type(v) == type(None)):      
        return "Failure"
    for value in order_domain_values(v,assignment,CSP):
        print("BT: var ID: {} value: {} domain: {}\n".format(v.ID,value,v.domain))
        if is_consistent(value,v,assignment,CSP):
            v.domain = set([value])
            assignment[v.ID] = v
            infer = {}
            infer = inferences(infer,assignment,v,value,CSP,fw_check,ac_3)
            #print(infer)
            if (infer != "Failure"):
                result = backtracking(assignment,CSP,method,fw_check,ac_3)
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
        #fw check is getting stuck in while loop
        while(v in assignment or len(v.domain) < 1):
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
    


def inferences(infer, assignment, var, value,CSP,fw_check,ac_3):
    global ac_flag
    if(ac_3 and ac_flag == False):
        #print("running AC3")
        ac3(CSP)
        redef_constraints(CSP)
        #print(CSP.constraint,'\n')
        for vkey in CSP.varset:
            print(CSP.varset[vkey].ID,CSP.varset[vkey].constraints,'\n')
        ac_flag = True
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
        if(revise(CSP,X1,X2)):
            if (len(X1.domain) == 1):
                return False
            
            for _,xk in X1.constraints - set([(X1.ID,X2.ID)]):
                arcs.add((xk,X1.ID))               
    return True
        


def revise(CSP:csp,X1:var,X2:var):
    revised = False
    no_del = False
    removals = set([])
    for d1 in X1.domain:
        for d2 in X2.domain:
            if((X1.ID,X2.ID) in X1.constraints and CSP.diff(d1,d2)):
                no_del = True
        if(no_del):
            removals.add(d1)
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
    
    
    #creating the variables with proper cell names a1-i9
    for letter in sudo_row:
        for num in sudo_col:
            sudo_varset[letter+num] = var(ID=letter+num,value = None,domain = sudoku_domain.copy())
    
    
    #already set variables
    c = 0
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
        for name in sudo_subgrid:
            grid_val = id_to_cell(v)
            if(grid_val < 9):
                if ((v,name) not in var.constraints):
                    var.constraints.add((v,name))
            elif(grid_val < 18):
                new_id = cell_to_id(id_to_cell(name) + 3)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
            elif(grid_val < 27):
                new_id = cell_to_id(id_to_cell(name) + 6)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
            elif(grid_val < 36):
                new_id = cell_to_id(id_to_cell(name) + 27)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
            elif(grid_val < 45):
                new_id = cell_to_id(id_to_cell(name) + 30)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
            elif(grid_val < 54):
                new_id = cell_to_id(id_to_cell(name) + 33)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
            elif(grid_val < 63):
                new_id = cell_to_id(id_to_cell(name) + 54)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
            elif(grid_val < 72):
                new_id = cell_to_id(id_to_cell(name) + 57)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
            elif(grid_val < 81):
                new_id = cell_to_id(id_to_cell(name) + 60)
                if ((v,new_id) not in var.constraints):
                    var.constraints.add((v,new_id))
        
    sudo_csp.create_csp_constraint()
    start_time = time.time()
    #print(map_csp.varset)
    #Flag to determine if ac_3 has ran already
    print(backtracking(map_ass,map_csp,2,fw_check = True,ac_3=False))
    end_time = time.time()
    fin_time = end_time - start_time
    #print("time taken to run {}".format(fin_time))
    #print(sudo_csp.varset)
    #print(backtracking(sudo_ass,sudo_csp,1,fw_check=False,ac_3=False))
    
    
    
    
    
    
    
    
    
    
    ################## Start Backtracking ###################
    #print(backtracking(sudo_ass,sudo_csp,1,fw_check = False))
    
    sys.setrecursionlimit(old_recurse_depth_limit)