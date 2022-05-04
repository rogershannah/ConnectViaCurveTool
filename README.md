# ConnectViaCurveTool

A Maya tool written in Python3 using maya.cmds that allows users to create a curve, a plane, or a poly object based off of the position of a selected group of objects.

![image](https://user-images.githubusercontent.com/43558247/166712818-7f0fad80-68e2-460c-8c49-ab1bfd19383a.png)


## Installation and Use
1. Download the folder
2. Extract and drag into the scripts Maya folder
3. Open "execute_tool.py" in the Maya script editor and run the script
4. Select a group of objects to base the curve on
5. Optionally: 
  a. Sort the objects based on their X, Y, or Z value
  b. convert the curve to a plane
  c. adjust the plane's size (default is 1, minimum is .001)
  d. add a plane depth to convert the plane to a poly object
