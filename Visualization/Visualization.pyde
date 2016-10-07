import sys
import os.path
sys.path.append(os.path.abspath(os.pardir))
from metrics import Euclidean 
from point import Point
from covertree import CoverTree
import random


ct=CoverTree(Euclidean())
path=os.path.abspath(os.path.join(os.pardir,'Tests','sample.txt'))
lastMouseX,lastMouseY,rotX,rotY,rotZ,diffX,diffY=0,0,0,0,0,0,0
isMouseReleased=True
scaleFactor=1
maxL, minL=20,-20
uncompLevels = dict()
showHierarchy, searchNN=False, False
currentLevel=maxL
levelScale=10
planeOffset=50
show2D=False
query=None
pts=[]

def setup():
    size(800, 700, P3D)
    rotX=rotY=0    
    ct.importFrom(path)    
    prevLevel = float('inf')
    uncompLevels[prevLevel] = {ct.levels[prevLevel].values()[0].point}
    for k1 in sorted({k for k in ct.levels if k != float('inf')}, reverse=True):            
        uncompLevels[k1] = uncompLevels[prevLevel] | {v.point for v in ct.levels[k1].values()}
        prevLevel = k1

def draw():
    global lastMouseX,lastMouseY,rotX,rotY,rotZ,diffX,diffY,isMouseReleased,scaleFactor,ct,showHierarchy,qury,searchNN
    background(255)
    lights()
    translate(width/2, height/2, 0)
    scale(scaleFactor)
    if show2D:
        level=currentLevel
        if currentLevel==maxL: level=float('inf')
        if currentLevel==minL: level=float('-inf')
        for p in uncompLevels[level]:
            noStroke()
            fill(128, 0, 0)
            pushMatrix()
            translate(p.pt[0], p.pt[1], 0)
            sphere(5)
            popMatrix()
    else:        
        if mousePressed:
            if isMouseReleased:
                lastMouseX=mouseX
                lastMouseY=mouseY
                isMouseReleased=False
            diffX+=mouseX-lastMouseX
            diffY+=mouseY-lastMouseY
            rotX=float(diffX)/width*2*PI
            rotY=float(diffY)/height*2*PI
            lastMouseX=mouseX
            lastMouseY=mouseY
        rotateX(-rotY)
        rotateY(rotX)
        rotateZ(rotZ)
        for l in ct.levels:
            for n in ct.levels[l].values():
                for ch in n.ch:                
                    if l==float('inf'): plevel=maxL
                    elif l==float('-inf'): plevel=minL
                    else: plevel=l
                    if ch.level==float('inf'): clevel=maxL
                    elif ch.level==float('-inf'): clevel=minL
                    else: clevel=ch.level
                    fill(0, 0, 0)
                    noStroke()
                    pushMatrix()
                    translate(n.point.pt[0], -plevel*levelScale,n.point.pt[1])
                    sphere(2)
                    popMatrix()
                    pushMatrix()
                    translate(ch.point.pt[0], -clevel*levelScale,ch.point.pt[1])
                    sphere(2)
                    popMatrix()                
                    stroke(0, 0, 0)
                    strokeWeight(2)
                    line(n.point.pt[0], -plevel*levelScale,n.point.pt[1], ch.point.pt[0], -clevel*levelScale,ch.point.pt[1])
        if showHierarchy:
            xcoords=[p.pt[0] for p in uncompLevels[float('-inf')]]
            ycoords=[p.pt[1] for p in uncompLevels[float('-inf')]]
            minx=min(xcoords)-planeOffset
            maxx=max(xcoords)+planeOffset
            miny=min(ycoords)-planeOffset
            maxy=max(ycoords)+planeOffset
            fill(220)
            beginShape()
            vertex(minx, -currentLevel*levelScale, miny)
            vertex(minx, -currentLevel*levelScale, maxy)
            vertex(maxx, -currentLevel*levelScale, maxy)
            vertex(maxx, -currentLevel*levelScale, miny)
            endShape(CLOSE)
            level=currentLevel
            if currentLevel==maxL: level=float('inf')
            if currentLevel==minL: level=float('-inf')
            for p in uncompLevels[level]:
                noStroke()
                fill(128, 0, 0)
                pushMatrix()
                translate(p.pt[0], -currentLevel*levelScale,p.pt[1])
                sphere(5)
                popMatrix()
        if searchNN:
            noStroke()
            fill(128, 0, 0)
            pushMatrix()
            translate(query.pt[0], -minL*levelScale,query.pt[1])
            sphere(5)
            popMatrix()
            prev=None
            for level in sorted(uncompLevels.keys()+[float('inf')], reverse=True):
                n=ct.restrictedNN(query,ct.root,level)
                fill(128, 0, 0)
                pushMatrix()
                translate(n.point.pt[0], -getlevel(level)*levelScale,n.point.pt[1])
                sphere(5)
                popMatrix()
                if prev is not None:
                    stroke(128, 0, 0)
                    strokeWeight(2)
                    line(n.point.pt[0], -getlevel(n.level)*levelScale,n.point.pt[1], prev.point.pt[0], -getlevel(prev.level)*levelScale,prev.point.pt[1])
                prev=n

def getlevel(level):
    if level == float('inf'): return maxL
    elif level == float('-inf'): return minL
    else: return level

def mouseWheel(e):
    global scaleFactor
    temp = scaleFactor-e.getAmount() / 50
    if temp<=0.01:
        return
    scaleFactor=temp

def mouseReleased():
    global isMouseReleased
    isMouseReleased=True

def keyPressed():
    global showHierarchy,currentLevel,ct,show2D
    if key=='h':
        showHierarchy=not showHierarchy
        currentLevel=maxL
        if not showHierarchy: show2D=False
    if key=='d':        
        if currentLevel==minL:
            currentLevel=maxL
        else:
            level=sorted(l for l in ct.levels if l<currentLevel ,reverse=True)[0]
            currentLevel=minL if level==float('-inf') else level
    if key=='u':
        if currentLevel==maxL:
            currentLevel=minL
        else:
            level=sorted(l for l in ct.levels if l>currentLevel)[0]
            currentLevel=maxL if level==float('inf') else level
    if key=='s':
        global searchNN,query
        searchNN=not searchNN
        query=Point([random.randint(-1000, 1000) for d in range(2)])
    if key=='2' and showHierarchy:
        show2D=not show2D
            
            