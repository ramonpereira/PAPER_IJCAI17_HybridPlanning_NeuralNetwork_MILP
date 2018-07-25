import random
import os
import json
import sys
import string
import unicodedata
from tqdm import tqdm
import pandas as pd

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from scipy.spatial import distance

from shapely.geometry import Point
from shapely.geometry import MultiPoint
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import box
from shapely.geometry.polygon import LinearRing
from descartes.patch import PolygonPatch

COLOR = {
    True:  '#6699cc',
    False: '#ff3333'
}

class DeterministicMazeRemaster(object):
    
    def __init__(self, setting):
        maze=setting.get('maze')
        self.maze=box(maze[0],maze[1],maze[2],maze[3])
        obstacles=setting.get('obstacles')
        self.obstacles=[]
        if obstacles:
            for coord in obstacles:
                self.obstacles.append(Polygon(coord))
        
        muds=setting.get('muds')
        self.muds=[]
        if muds:
            for coord in muds:
                self.muds.append(Polygon(coord))
        start_state=setting.get('start_state')
        self.start_state=Point(start_state)
        self.current_state=self.start_state
        goal_states=setting.get('goal_states')
        self.goal_states=[]
        for coord in goal_states:
            self.goal_states.append(Point(coord))
        self.action_range=setting.get('action_range')
        self.deadend_toleration=setting.get('deadend_toleration')
        self.injail=False
        self.inmud=False
        self.backup = {k:v for k, v in self.__dict__.items() if not (k.startswith('__') and k.endswith('__'))}
        
    def PlotMaze(self):
        fig = plt.figure(dpi=90)
        ax = fig.add_subplot(111)
        x, y = self.maze.exterior.xy
        ax.plot(x, y, 'o', color='#999999', zorder=1)
        patch = PolygonPatch(self.maze, facecolor='#6699cc', edgecolor='#6699cc', alpha=0.5, zorder=2)
        ax.add_patch(patch)
        if self.muds:
            for mud in self.muds:
                patch = PolygonPatch(mud, facecolor='#ff3333', edgecolor='#ff3333', alpha=0.5,hatch='\\', zorder=2)
                ax.add_patch(patch)
        if self.obstacles:
            for obstacles in self.obstacles:
                patch = PolygonPatch(obstacles, facecolor='#ffaabb', edgecolor='#ffaabb', alpha=0.5,hatch='\\', zorder=2)
                ax.add_patch(patch)
        plt.show()
        
    def Reset(self):
        backup=self.backup
        self.__dict__.update(backup)
        self.backup = backup
    
    def UpdateState(self,new_state):
        self.current_state = new_state
        
    def InJail(self):
        if self.injail == True:
            return 1
        else:
            return -1
    
    def InMud(self):
        for mud in self.muds:
            if mud.intersects(self.current_state):
                self.Inmud=True
                return 1
            else:
                self.Inmud=False
        return -1
    
    def GetCurrentState(self):
        return self.current_state.x, self.current_state.y, self.InJail(),self.InMud()
        
    def TakeAction(self,action):
        if not self.injail:
            proposal=Point((self.current_state.x+action[0],self.current_state.y+action[1]))
            #print proposal.x, proposal.y
            path=LineString([self.current_state, proposal])
            
            if self.obstacles:
                for obstacle in self.obstacles:
                    if obstacle.intersects(path):
                        self.injail=True
                        self.current_state=Point((-1,-1))
                        return
            if self.muds:
                for mud in self.muds:
                    if mud.intersects(path):
#                         print 'we are here'
                        path_inmud = mud.intersection(path)
                        coords = [path.coords[0],path.coords[1]]
                        for loc in path_inmud.coords:
                            if loc not in coords:
                                coords.append(loc)
                        coords.sort(key=lambda tup: tup[1]) 
                        p_in_mud=proposal.intersects(mud)
                        s_in_mud=self.current_state.intersects(mud)
                        if p_in_mud and not s_in_mud: 
#                             print 'current not in mud'
                            if coords.index((self.current_state.x,self.current_state.y))==0: 
                                x = coords[1][0]-coords[0][0]+0.5*(coords[-1][0]-coords[1][0])
                                y = coords[1][1]-coords[0][1]+0.5*(coords[-1][1]-coords[1][1])
                                proposal=Point((coords[0][0]+x,coords[0][1]+y))
                            else:
                                x = coords[1][0]-coords[-1][0]+0.5*(coords[0][0]-coords[1][0])
                                y = coords[1][1]-coords[-1][1]+0.5*(coords[0][1]-coords[1][1])
                                proposal=Point((coords[-1][0]+x,coords[-1][1]+y))
                        elif s_in_mud and not p_in_mud:
#                             print 'proposal not in mud'
                            if coords.index((self.current_state.x,self.current_state.y))==0: 
                                x = 0.5*(coords[1][0]-coords[0][0])+(coords[-1][0]-coords[1][0])
                                y = 0.5*(coords[1][1]-coords[0][1])+(coords[-1][1]-coords[1][1])
                                proposal=Point((coords[0][0]+x,coords[0][1]+y))
                            else:
                                x = 0.5*(coords[1][0]-coords[-1][0])+(coords[0][0]-coords[1][0])
                                y = 0.5*(coords[1][1]-coords[-1][1])+(coords[0][1]-coords[1][1])
                                proposal=Point((coords[-1][0]+x,coords[-1][1]+y))
                        else:
                            proposal=Point((self.current_state.x+action[0]*0.5,self.current_state.y+action[1]*0.5))
            
            path=LineString([self.current_state, proposal])
            bounds=LinearRing(self.maze.exterior.coords) 
            if bounds.intersects(path):
                onedge=bounds.intersection(path)
                if  type(onedge) is MultiPoint:
                    for point in onedge:
                        if not point.equals(self.current_state):
                            proposal=point
                elif type(onedge) is Point:
                    if not onedge.equals(self.current_state):
                        proposal=onedge
                    elif not self.maze.contains(proposal):
                        proposal=bounds.interpolate(bounds.project(proposal))
                        
            self.current_state=proposal
        else:
            self.deadend_toleration=self.deadend_toleration-1
        return self.GetCurrentState()
        
    def IfGameEnd(self):
        for goal in self.goal_states:
            if self.current_state.equals(goal):
                self.Reset()
        if (self.deadend_toleration == 0):
            self.Reset()
    
    def DeltaDistance(self,new_state,old_state):
        delta=[]
        delta.append(new_state[0]-old_state[0])
        delta.append(new_state[1]-old_state[1])
        if (new_state[2]==1):
            delta.append(1)
        else:
            delta.append(-1)
        if (new_state[3]==1):
            delta.append(1)
        else:
            delta.append(-1)
        return delta