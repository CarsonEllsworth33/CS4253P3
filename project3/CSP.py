#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from CSP_setup import setup_csp
from CSP_setup import variable
from random import randint as rdint
import math


def backtrack(assignment:set,csp:list,method = 0,fw_check = False,arc_con = False) -> list:
    '''
    csp is the list of variables that are to be selected
    method is the method type in which they are selected
        0:random #the default option
        1:minimum-remaining value
        2:minimum-remaining value together with degree
    also influences 
    '''
    #check to see if all values have assignment
    print(len(assignment))
    if(len(assignment)%10 == 0):
        print()
    if(len(assignment) == len(csp)):
        print(assignment)
        return True
    
    var = select_unassigned_variable(csp,assignment)
    bkp_domain = var.domain.copy()
    for value in order_domain_values(var,assignment,csp):
        cont = 0
        if(value_consistency(var,assignment,csp,value)):
            #add reduce domain single value and add to assignment
            
            var.domain = set([value])
            assignment.add(var)
            infer = inference(var,csp,value,assignment,fw_check)
            if(infer != False):
                #add inference to assignment
                result = backtrack(assignment,csp,method,fw_check,arc_con)
                if(result != False):
                    return result
                
         
                
        if(var in assignment):
            if(fw_check == True):
                for x in var.constraints:
                    c_var = grab_variable(x,csp)
                    if(c_var not in assignment):
                        c_var.domain = bkp_domain.copy()
            var.domain = bkp_domain.copy()
            #remove infrences
            assignment.remove(var)
    return False
        

def select_unassigned_variable(csp:list,assignment:set,method=0) -> variable:
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
        y = rdint(0,len(csp)-1) #rdint is inclusive, hence the -1
        var = csp[y]
        while(var in assignment):
            y = rdint(0,len(csp)-1) #rdint is inclusive, hence the -1
            var = csp[y]
        return var
    
    elif(method == 1):
        #1:minimum-remaining value
        least_domain = math.inf
        low_var = None
        for var in csp:
            if(var not in assignment):
                dm_size = var.domain_size()
                if(dm_size == 0):
                    return False
                if(dm_size < least_domain):
                    least_domain = dm_size
                    low_var = var
        return low_var
                
    elif(method == 2):
        #2:minimum-remaining value together with degree
        #the degree of the node works as a tie breaker, otherwise it works
        #just like minimum remaining value
        least_domain = math.inf
        low_var = None
        for var in csp:
            if(var not in assignment):
                dm_size = var.domain_size()
                if(dm_size == 0):
                    return False
                if(dm_size < least_domain):
                    least_domain = dm_size
                    low_var = var
                elif(dm_size == least_domain and var.constraint_size() > low_var.constraint_size()):
                    least_domain = dm_size
                    low_var = var
        return low_var
    
    
 
   
    
    
def value_consistency(var,assignment,csp,value):
    for x in var.constraints:
        constraint_var = grab_variable(x,csp)
        val_set = set([value])
        if(constraint_var.domain == val_set and constraint_var in assignment):
            return False
    return True    
    
    

    
    
    
    

def order_domain_values(var,assignment,csp):
    """
    The order in which the domain values should be tried as a feasable option
    """
    #right now it works only as just convert value and return
    #no special black magic yet
    return var.domain









def inference(var,csp,value,assignment,fw_check):
    if(fw_check == True):
        #do forward checking
        for x in var.constraints:
            c_var = grab_variable(x,csp)
            if(c_var not in assignment):
                c_var.domain -= set([value])
                if(not c_var.domain):
                    #c_var is empty
                    c_var.domain.add(value)
                    cont = 1
                    #continue to new value for loop
    else:
        #something something something arc-consistency 
        return True
    
    
    
    
    
    
    
    
def ac_3(csp:list,queue = set([])):
    #need to define what the arcs are for the problem and populate the queue:(set)
    
    while(queue):
        arc = queue.pop()
        X1 = arc[0]
        X2 = arc[1]
        if revise(csp,X1,X2):
            if (X1.domain_size() == 0):
                return False
            for Xk in X1.constraints:
                if(Xk is not X2):
                    queue.add((Xk,X1))
    return True








def revise(csp:list,X1:variable,X2:variable):
    revised = False
    for valueX1 in X1.domain:
        for valueX2 in X2.domain:
            if(valueX1 == valueX2):
                #domain allows for arcs where X1 and X2 can have same values 
                #they are removed
                X1.rmv_from_domain(valueX1)
                revised = True
                break
    return revised
    






def grab_variable(ID:int,csp:list) -> variable:
    for x in csp:
        if (x.ID == ID):
            return x





def p_constraints(csp:list):
    for x in range(len(csp)):
        print("{} CS: {}".format(map_var_list[x].ID,map_var_list[x].constraint_size()))
        
        
def all_diff(*args):
    for item in args:
        for other in args:
            if(item is not other):
                if(item == other):
                    return False
            else:
                pass
    return True            
    
        

if __name__ == "__main__":
    map_var_list,sudo_var_list = setup_csp()
    map_assignment = set([])
    backtrack(map_assignment,map_var_list,method=2,fw_check=True)
    print(len(map_assignment))
    
    
    
    
    
    sudo_assignment = set([])
    
    for x in sudo_var_list:
        if(x.domain_size() == 1):
            sudo_assignment.add(x)
    
    #backtrack(sudo_assignment,sudo_var_list,method=2,fw_check = True)
    
    