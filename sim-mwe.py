# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:27:44 2024

@author: willr
"""

import math
import matplotlib.pyplot as plt
import scipy.io as sio
from numpy import inf
import numpy as np
import matlab.engine
from scipy.integrate import odeint, solve_ivp

#start the MATLAb pairing
eng = matlab.engine.start_matlab()
matpre = sio.loadmat(r'C:\Users\willr\.spyder-py3\structpre.mat')

#COM in physical and virtual space
global xarr
xarr = []
global yarr
yarr = []
global vxarr
vxarr = []
global vyarr
vyarr = []

#################
#define functions
#################
def intensityVals(x,y,theta):
    #this function finds the intensity values on the left and right engines    
    xr = x+np.cos(theta+np.pi/2)*1e-6
    yr = y+np.sin(theta+np.pi/2)*1e-6
    
    xl = x+np.cos(theta-np.pi/2)*1e-6
    yl = y+np.sin(theta-np.pi/2)*1e-6

    leftI = arbitraryf(xl,yl)
    rightI = arbitraryf(xr,yr)

    intensities = [leftI,rightI]
    return intensities
    
def distToEnd(x,y):
    #this function applies a proportional distance metric in virtual space
    
    #load in the preverts.
    preverts = matpre['pstruct'][0][0][0]
    
    #get max values that aren't infinity or -infinity
    maxX = np.nanmax(np.real(preverts[preverts != (-np.inf and np.inf)]))
    maxY = np.max(np.imag(preverts))
    
    #target location is the center contour for this example, so @ (maxX,0.5*maxY)
    targetLoc = (maxX,.5*maxY)

    #calculate the distance to this point from the current x,y position
    dist = ((targetLoc[0] - x)**2 + (targetLoc[1] - y)**2)**.5

    return dist

def arbitraryf(x,y):
    #this function determines the intensity field. It can be a fxn. such as 
    #fisheye, GRIN, etc., or can index MATLAB to do a SC map.
    
    #fisheye
    #r = (x**2+y**2)**.5
    #I = 1/(1+r/.5)**2
    
    #grin
    #a = .1
    #r = ((y)**2)**.5
    #I = 2-1/(1-a*r**2/2)
    
    #SC map
    I = SCmapintens(x,y)
    
    return I
    
def SCmapintens(x,y):
    #this function talks to MATLAB to determine the intensity values due to
    #the mapping function
    
    #take coords. in physical space (x,y) and look them up in virtual space
    [x1,y1] = eng.evalinv_python(x,y,nargout=2)
    vxarr.append(x1)
    vyarr.append(y1)
    
    #take the magnitude of the derivative of the map and combine with the 
    #implemented metric to determine the intensity at a point
    [x1d,y1d] = eng.evaldiff_python(x1,y1,nargout=2)
    I = 1*abs(x1d+1j*y1d)
    #I = I*distToEnd(x1,y1)
    return I

#the fxn passed to odeint
def fpass(t,arr):
    #load in array. this should be pos in phys. space
    x,y,theta = arr
    xarr.append(x)
    yarr.append(y)

    #plot
    plt.scatter(x,y)
    
    #lookup the intensity values on the engines
    intens = intensityVals(x,y,theta)
    leftI = intens[0]
    rightI = intens[1]
    
    #update the integrator with new values corresponding to the intensities
    dx = np.cos(theta)*(leftI+rightI)/2
    dy = np.sin(theta)*(leftI+rightI)/2
    thetadot = (leftI-rightI)/(2e-6)

    retArr = [dx,dy,thetadot]
    
    return retArr

fig=plt.figure()

#initialize the robot position
initArray = [[2.8,1.4,math.radians(60)]]
t = [0. ,100]

#simulate using solve_ivp
for init in initArray:
    solu = solve_ivp(fpass, t, init,method='RK23',max_step=.25)
    plt.grid(False)
    
plt.show()
a = np.asarray([xarr,yarr])
#np.savetxt("posarr.csv",a,delimiter=",")
    
    
    
