#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 17:38:45 2019

@author: carsonellsworth
"""

import json


class variable():
    def __init__(self,ID:int,domain:set,constraints:set):
        self.domain = domain
        self.ID = ID
        self.constraints = constraints
        
    def is_domain_empty(self):
        if(self.domain):
            return False
        return True
    
    def domain_size(self) -> int:
        return len(self.domain)
    
    def rmv_from_domain(self,item):
        try:
            self.domain.remove(item)
        except(KeyError):
            pass
            
    def add_constraints(self,item=None,lst=[]):
        if(item != None):
            self.constraints.add(item)
        if(len(lst) != 0):
            for x in lst:
                if(self.ID != x):
                    self.constraints.add(x)
                    
    def constraint_size(self) -> int:
        return len(self.constraints)
                    
    def __repr__(self):
        return "{} domain:{}".format(self.ID,
                                      #self.constraints, constr:[{}]
                                      self.domain
                                      )
    
    
        

def data_translator_map(f:str):
    csp_map={}
    with open(f,'r') as f:
        csp_map = json.load(f)
    return csp_map



def data_translator_sudoku(f:str):
    csp_sudo=[]
    with open(f,'r') as f:
        csp_sudo = json.load(f)
    print_sudoku(csp_sudo)
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
    
    
def num_zeroes(edges:list):
    counter = 0
    for l in edges:
        for item in l:
            if(item == 0):
                counter += 1
    return counter

    
def element_add(lst:list,val:int):
    l = lst.copy()
    for y in range(len(l)):
        l[y] += val
    return l

def setup_csp():
    
    map_color = data_translator_map('gcp.json')
    edges = map_color["edges"]
    num_points = map_color["num_points"]
    map_csp_domain = set(['r','g','b','y'])
    map_var_list = [variable(ID=x,
                             domain=map_csp_domain.copy(),
                             constraints=set([]).copy()
                             ) for x in range(num_points)]
    
    
    #####  adding the constraints for the map to each var  #####
    for map_var in map_var_list:
        for item in edges:
            if(item[0]==int(map_var.ID)):
                map_var.add_constraints(item[1])
    
    #print out the populated constraints
    for map_var in map_var_list:
        print(map_var.ID,map_var.constraints)
    ############################################################
    
    
    #suduko constraints are the row it is in and the colomn it is in
    sudoku = data_translator_sudoku("sudoku.json")
    #zeroes = num_zeroes(sudoku)  # useless atm
    sudo_csp_domain = set([1,2,3,4,5,6,7,8,9])
    sudo_var_list = [variable(ID=x,
                              domain=sudo_csp_domain.copy(),
                              constraints=set([])
                              ) for x in range(len(sudoku)**2)]
    counter = 0
    for x in range(len(sudoku)):
        for y in range(len(sudoku[0])):
            if (sudoku[x][y] != 0):
                sudo_var_list[counter].domain = set([sudoku[x][y]])
            counter+=1
    
    ######## PREPROCESSING FOR SUDOKU CONSTRAINT SETUP FOR A 9x9 board ########
    #0  1  2 |3  4  5 |6  7  8
    #9  10 11|12 13 14|15 16 17
    #18 19 20|21 22 23|24 25 26
    
    base_grid = [0,1,2,9,10,11,18,19,20] #0,3,6 #27,30,33 #54,57,60
    grid_incr = [0,3,6,27,30,33,54,57,60]
    base_column = [x for x in range(81) if x%9==0]
    base_row = [x for x in range(9)]
    
    
    for sudo_var in sudo_var_list:
        #grabs the row grid neighbors
        mod9 = sudo_var.ID%9
        mod3 = sudo_var.ID%3
        
        #column constraint passing
        for sudo_var2 in sudo_var_list:
            if(sudo_var is sudo_var2):
                continue
            if(sudo_var2.ID % 9 == mod9): 
                sudo_var.add_constraints(sudo_var2.ID)
                
        #grid constraint passing
        for x in grid_incr:
            l=element_add(base_grid,x)
            for x in l:
                if (sudo_var.ID == x):
                    sudo_var.add_constraints(lst=l)
        
        #row constraint passing
        if(sudo_var.ID < 9):
            #first row
            sudo_var.add_constraints(lst=base_row)
        elif(sudo_var.ID < 18):
            #second row
            sudo_var.add_constraints(lst=element_add(base_row,9))
            
        elif(sudo_var.ID < 27):
            #third row
            sudo_var.add_constraints(lst=element_add(base_row,18))
            
        elif(sudo_var.ID < 36):
            #fourth row
            sudo_var.add_constraints(lst=element_add(base_row,27))
            
        elif(sudo_var.ID < 45):
            #fifth row
            sudo_var.add_constraints(lst=element_add(base_row,36))
            
        elif(sudo_var.ID < 54):
            #sixth row
            sudo_var.add_constraints(lst=element_add(base_row,45))
            
        elif(sudo_var.ID < 63):
            #seventh row
            sudo_var.add_constraints(lst=element_add(base_row,54))
            
        elif(sudo_var.ID < 72):
            #eighth row
            sudo_var.add_constraints(lst=element_add(base_row,63))
            
        elif(sudo_var.ID < 81):
            #ninth row
            sudo_var.add_constraints(lst=element_add(base_row,72))
            
            
    #####################################################################    
        
    return (map_var_list,sudo_var_list)       
        
    
    
    
    
    
    
    
    
    
    
    