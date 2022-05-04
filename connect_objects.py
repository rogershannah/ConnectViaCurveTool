# Maya tool which allows users to easily and quickly place objects in/around another object
# with a set radius and many other customizable parameters.

# Instructions: to run, navigate to execute_tool.py and run the file

from ctypes import c_uint16
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtUiTools import *
from PySide2.QtWidgets import *
from functools import partial
import maya.cmds as cmds
from maya import OpenMayaUI
from pathlib import Path
import math
from shiboken2 import wrapInstance
from random import randrange
import random

# keep track of transform settings created by user


class Transform():
    def __init__(self):
        self.connecting = None
        self.isPlane = False
        self.order = False
        self.axis = None
        self.height = 1
        self.extrudeVal = 0

# show gui window

def showWindow():
    # get this files location so we can find the .ui file in the /ui/ folder alongside it
    UI_FILE = str(Path(__file__).parent.resolve() / "gui.ui")
    loader = QUiLoader()
    file = QFile(UI_FILE)
    file.open(QFile.ReadOnly)

    # Get Maya main window to parent gui window to it
    mayaMainWindowPtr = OpenMayaUI.MQtUtil.mainWindow()
    mayaMainWindow = wrapInstance(int(mayaMainWindowPtr), QWidget)
    ui = loader.load(file, parentWidget=mayaMainWindow)
    file.close()

    ui.setParent(mayaMainWindow)
    ui.setWindowFlags(Qt.Window)
    ui.setWindowTitle('Connect Via Geometry')
    ui.setObjectName('Connect_Via_Geo')
    ui.setWindowFlags(Qt.Window | Qt.WindowStaysOnTopHint)

    t = Transform()  # transform attribute

    # function for the the selecting objects to connect button
    def select_objects_to_connect():
        # get selected object(s)
        selected = cmds.ls(sl=True, long=True) or []
        list_to_connect = []
        for item in cmds.ls(selected):
            list_to_connect.append(item)
        t.connecting = list_to_connect
        list_str = ""
        for item in list_to_connect:
            list_str += str(item)
            if(list_to_connect.index(item) < (len(list_to_connect) - 1)):
                list_str += ", "
        # show current selected objects as a list of text on gui
        ui.connecting_objs.setText(list_str)

    

    #toggle is curve is a plane
    def set_plane(c):
        t.isPlane = not t.isPlane

    #set number of times to duplicate
    def set_height(h):
        t.height = float(h)

    #set number of times to duplicate
    def set_num_extrude_val(v):
        t.extrudeVal = float(v)

       

    #snap to x side of object
    def set_X(x1):
        isChecked = ui.x_radio.isChecked()
        if isChecked:
            t.axis = "X"
            t.order = True

    #snap to y side of object
    def set_Y(y1):
        isChecked = ui.y_radio.isChecked()
        if isChecked:
            t.axis = "Y"
            t.order = True
      
    #snap to y side of object
    def set_Z(z1):
        isChecked = ui.z_radio.isChecked()
        if isChecked:
            t.axis = "Z"
            t.order = True


    # Python3 implementation of QuickSort
    # quicksort helper
    def partition(start, end, array, axis):

        # Initializing pivot's index to start
        pivot_index = start
        pivot = array[pivot_index][axis]

        # This loop runs till start pointer crosses end pointer
        # when it does, swap the pivot with element on end pointer
        while start < end:

            # Increment the start pointer till it finds an element greater than pivot
            while start < len(array) and array[start][axis] <= pivot:
                start += 1

            # Decrement the end pointer till it finds an
            # element less than pivot
            while array[end][axis] > pivot:
                end -= 1

            # If start and end have not crossed each other,
            # swap the numbers on start and end
            if(start < end):
                array[start], array[end] = array[end], array[start]

        # Swap pivot element with element on end pointer.
        # This puts pivot on its correct sorted place.
        array[end], array[pivot_index] = array[pivot_index], array[end]

        # Returning end pointer to divide the array into 2
        return end

    # quicksort main funtion

    def quick_sort(start, end, array, axis):

        if (start < end):

            # p is partitioning index, array[p]
            # is at right place
            p = partition(start, end, array, axis)

            # Sort elements before partition
            # and after partition
            quick_sort(start, p - 1, array, axis)
            quick_sort(p + 1, end, array, axis)

    # apply button clicked
    def apply():
        # User error handling
        if t.connecting == None:
            ui.warnings.setText(
                "<font color='red'>Warning:Please set at least 1 connecting object.</font>")
            return

        else:  # all proper fields have been set
            ui.warnings.setText("")

        
        selected_centers = [] #list of selected items to connect

        # draw a curve that runs through the pivot point of each object
        for obj in t.connecting:
                # Get the center of the bounding box of obj in world space and append to the list
            point = cmds.objectCenter(cmds.ls(obj)[0], gl=True)
            selected_centers.append(point)
        print(t.order)

        if t.order is True:
            print("hello")
            # sort based on selected axis
            if(t.axis == "X"):
                quick_sort(0, len(selected_centers) - 1, selected_centers, 0)
            elif(t.axis == "Y"):
                quick_sort(0, len(selected_centers) - 1, selected_centers, 1)
            elif(t.axis == "Z"):
                quick_sort(0, len(selected_centers) - 1, selected_centers, 2)
        print(selected_centers)


        #create the curve and it is selected
        c1 = cmds.curve(p =  selected_centers) 
        #center pivot
        center = cmds.objectCenter(c1, gl = True)
        cmds.xform(c1, pivots = center)


        if t.isPlane:
            #bevel curve and delete original
            b1 = cmds.bevel(c1, ch=True, rn=False, po=1, ns=1, js=True, ed=t.height)            
            cmds.delete(c1)
            if t.extrudeVal > 0:
                faceNum= cmds.polyEvaluate(f = True) - 1
                cmds.polyExtrudeFacet(b1[0] + '.f[0:'+ str(faceNum) +']', ch=True, kft=True, ltz=t.extrudeVal)

# Close dialog
    def close():
        ui.done(0)
        

    # connect buttons to functions
    ui.connecting_button.clicked.connect(partial(select_objects_to_connect))
    #ui.apply_button.clicked.connect(partial(apply))
    #ui.x_check.stateChanged.connect(partial(set_X))
    #ui.y_check.stateChanged.connect(partial(set_Y))
    #ui.z_check.stateChanged.connect(partial(set_Z))
    ui.apply_button.clicked.connect(partial(apply))
    ui.x_radio.toggled.connect(partial(set_X))
    ui.y_radio.toggled.connect(partial(set_Y))
    ui.z_radio.toggled.connect(partial(set_Z))
    ui.close_button.clicked.connect(partial(close))
    ui.plane_check.stateChanged.connect(partial(set_plane))
    ui.num_height.setValue(1.0)
    ui.num_height.setMinimum(0.001)
    ui.num_height.valueChanged.connect(partial(set_height))
    ui.num_extrudeVal.valueChanged.connect(partial(set_num_extrude_val))
    

    # show the QT ui
    ui.show()
    return ui


if __name__ == "__main__":
    window = showWindow()