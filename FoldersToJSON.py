# Petri Autio 3/2014 - petriau@wateraid.org
import collections
import json
import os
import Tkinter, Tkconstants, tkFileDialog
# The aim is to traverse a folder structure and create a JSON file
# with the correct hierarchy to be used as input for a D3-library
# hierarchical tree visualisation
# TODO error logging
print 'Starting'
links = []

def buildLinks2(folderList):
    global links
    tempLinks = []
    d = 0
    lefts = []
    for dir in folderList:
        left = ""
        d += 1
        id = 0
        # find left sides, i.e. path up to current folder
        for letterIndex in range(len(dir)-1, -1, -1):
            if dir[letterIndex] == "|":
                left = dir[:letterIndex]
                add = True
                for l in range(0, len(lefts)):
                    if left == lefts[l][1]:
                        id = lefts[l][0] #ID for this dir
                        add = False
                        break
                if add:
                    lefts.append([str(len(lefts)), left])
                    id = len(lefts)
                break
        last = 0

    #cycle through once to establish all directories
    for dir in folderList:
        # three parts: c:\test\folder1\subfolder
        # we want to be able to break the directory down by folders
        # match it to the right folder id
        # append the folder and the folder right above it, including the correct IDs
        s = 0
        leftID = 0
        leftSide = ""
        rightID = 0
        child = ""
        n = 0 # count folder depth
        for index in range(len(dir)-1, 0, -1):
            if dir[index] == "|":
                n += 1
                leftSide = dir[:index]
                s = index
                # find the next child folder
                # child = index to next | or end of string
                # parent = index to previous | or end of string

                if n == 1:
                    child = dir[index+1:]
                else:
                    nextIndex = 0
                    for i in range(index + 1, len(dir)):
                        if dir[i] == "|":
                            nextIndex = i
                            break
                    child = dir[index+1:nextIndex]

                for i in range(0, len(lefts)):
                    if lefts[i][1] == leftSide:
                        #print leftSide
                        leftID = lefts[i][0]
                        #print id
                    if lefts[i][1] == leftSide + "|" + child:
                        rightID = lefts[i][0]

                # parent should be the folder right above the child, keep the right id though
                a = 0
                for i in range(index-1, 0, -1):
                    if dir[i] == "|":
                        a = i
                        break
                #print 'leftside ' + leftSide
                if a != 0:
                    fosterParent = dir[a+1:index]
                else:
                    fosterParent = dir[a:index]
                if fosterParent == "":
                    fosterParent = dir[:index]

                parent = str(leftID) + " " + fosterParent

                #print parent
                #parent = str(leftID) + " " + leftSide
                child = str(rightID) + " " + child
                #print 'parent ' + parent
                #print 'child ' + child
                tempLinks.append((parent, child))

    # the above means that for each folder structure with only one layer of subdirectories after it
    # we now have IDs
    # what we now want to ensure is that if the folder structure in a string matches what is in the array
    # then it gets assigned the correct id
    for l in tempLinks:
        if l not in links:
            links.append(l)

def getFolders(rootDir):
    print 'Getting folders'
    global links

    folderList = []
    dirsChecked = 0
    dirsChanged = 0
    dirlist = os.walk(rootDir)
    for root, dirs, files in dirlist:
        dirsChecked += 1
        #print root
        root = root.replace(rootDir, "")
        #print root
        folderList.append(root.replace("\\", "|"))
    sortedFolders = sorted(folderList)
    #print sortedFolders
    buildLinks2(sortedFolders)
    # json structure
    # {
    # "name" : "flare",
    # "children": [
    # {
    # "name" : "cluster",
    # "children" : [
    # {"name": "aname", "size" : 0}
    # ]
    
def makeJSON(location):
    global links
    name_to_node = {}
    root = {'name': 'Root', 'children': []}
    for parent, child in links:
        parent_node = name_to_node.get(parent)
        # show parent name only, not id
        if not parent_node:
            for i in range(0, len(parent)):
                if parent[i] == " ":
                    parentName = parent[i+1:]
                    break
            name_to_node[parent] = parent_node = {'name': parentName}
            root['children'].append(parent_node)
        # display only child name and not id
        for i in range(0, len(child)):
            if child[i] == " ":
                childName = child[i+1:]
                break
        name_to_node[child] = child_node = {'name': childName}
        parent_node.setdefault('children', []).append(child_node)

    Resultfile = open(location + "FolderTree.json", 'w')
    Resultfile.write(json.dumps(root, indent=4, sort_keys=True))
    Resultfile.close()

def mainWork():
    global rootDir
    print 'Getting ready to get folders'

    getFolders(rootDir)

    print 'Folders gotten'
    print 'Preparing JSON file'

    makeJSON(rootDir)

    print 'JSON file prepared in %s.' % rootDir
    print 'Goodbye'

rootDir = ""

class TkFileDialog(Tkinter.Frame):
    def __init__(self, root):

        print "----------------------------------------------------"
        print ("Folder Structure to JSON file - Petri Autio 2014")
        print "----------------------------------------------------"
        print "\nSelect the root directory, and the program will   "
        print "scan all the subfolders and create a JSON-file with "
        print "an suitable structure for a D3 visualisation.       "
        print "The original use case was for a hierarchical tree.\n"

        def getDir():
            global rootDir
            rootDir = str(tkFileDialog.askdirectory(initialdir="C:\\")) + "/"
            print "Root set to %s" % rootDir
        Tkinter.Frame.__init__(self, root)

        Tkinter.Button(self, text='Choose Root Folder', command=getDir).pack(fill = Tkinter.X)
        L1 = Tkinter.Label(self, text="---------")
        L1.pack(fill=Tkinter.X)
        Tkinter.Button(self, text='Run', command=mainWork).pack(fill = Tkinter.X)

if __name__=='__main__':
  root = Tkinter.Tk()
  root.wm_title("Folder Structure to JSON - Petri Autio 2014")
  TkFileDialog(root).pack()
  root.mainloop()