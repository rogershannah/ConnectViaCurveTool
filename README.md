# ConnectViaCurveTool

A Maya tool written in Python3 using maya.cmds that allows users to create a curve, a plane, or a poly object based off of the position of a selected group of objects.

![image](https://user-images.githubusercontent.com/43558247/166718242-3edb3509-d18f-4446-b971-7ae784e52f5d.png)



https://github.com/rogershannah/ConnectViaCurveTool/assets/43558247/d4fd6630-8d83-467a-8a46-9ee0265c32ec



## Installation and Use
1. Download the files in zip folder

 ![image](https://user-images.githubusercontent.com/43558247/167177306-5ab39e56-b74f-4053-b145-b50ae849affc.png)
 
2. Extract the miles and move them drag into the scripts Maya folder (ex. `...\maya\2022\scripts`)
3. Open "execute_tool.py" in the Maya script editor and run the script ![image](https://user-images.githubusercontent.com/43558247/167178537-72ccf865-25b9-426c-bdac-55db39bf828f.png)
  a. ctrl + Enter to run
4. Select a group of objects to base the curve on
5. Optionally: 

  a. Sort the objects based on their X, Y, or Z value
  
  b. convert the curve to a plane
  
  c. adjust the plane's size (default is 1, minimum is .001)
  
  d. add a plane depth to convert the plane to a poly object
