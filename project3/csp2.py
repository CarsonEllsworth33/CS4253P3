#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 03:50:11 2019

@author: carsonellsworth
"""
class var():
    def __init__(self,ID,value,domain):
        self.ID = ID
        #self.value = value
        self.domain = domain
        self.constraints = set([])
        self.inferences = {}
        
    def __repr__(self):
        return "{}".format(self.domain)
    
        
class csp():
    def __init__(self,X:dict,D:set,C=None):
        self.varset = X
        self.domain = D
        self.constraint = set([])
        if(C == None):
            pass
        elif(C == "ddiff"):
            self.all_diff()
        else:
            self.map_edge_constraint(C)
        
    def all_diff(self):
        #tuple relation over the domain
        for x in self.domain:
            for y in self.domain:
                if (x is not y):
                    self.constraint.add((x,y))
                    
    def diff(self,i,j):
        boo = i != j
        #print("diff return: {}".format(boo))
        return boo
    
    def map_edge_constraint(self,C):
        for a,b in C:
            self.constraint.add((a,b))
            
    def create_var_constraint(self):
        for x in self.varset:
            for y in self.constraint:
                if(self.varset[x].ID == y[0]):
                    self.varset[x].constraints.add(y)


    def create_csp_constraint(self):
        for x in self.varset:
            for y in self.varset[x].constraints: #y is a tuple (X1.ID,X2.ID)
                if(y not in self.constraint):
                    self.constraint.add(y)




    