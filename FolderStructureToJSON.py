__author__ = 'Petriau'
#import Tkinter, Tkconstants, tkFileDialog
import os

## Aim: create a nested JSON based on the folder structure of a given root directory

JsonDict = {}

## Step one, create a list of all the folders under a root
def insertIntoDataStruct(name, value, aDict):
    if not name in aDict:
        aDict[name] = value
    else:
        aDict[name].append(value)

def renameFolders(rootDir, nameFrom, nameTo):
    global JsonDict
    try:
        folderList = []
        dirsChecked = 0
        dirsChanged = 0
        dirlist = os.walk(rootDir)
        for root, dirs, files in dirlist:
            dirsChecked += 1

            folderList.append(root)

            #print root
            #find the string until the rightmost backslash
            # for letterIndex in range(len(root)-1, 1, -1):
            #     if root[letterIndex] == "\\":
            #         existing = root[(letterIndex + 1):]
            #         if existing == nameFrom:
            #             target = root.replace(existing, nameTo)
            #             changedFolders.append("From " + root + "\n")
            #             changedFolders.append("To " + target + "\n")
            #             #print target
            #             #os.rename(root, target)
            #             dirsChanged += 1
            #         break

        # Write log
        Resultfile = open(rootDir + "/FolderNameChangeLog.csv", 'w')
        for line in folderList:
            Resultfile.write(line)

        print folderList
        print folderList[3][:-2]
        sortedFolders = sorted(folderList)
        print sortedFolders

        # json structure
        # {
        # "name" : "flare",
        # "children": [
        # {
        # "name" : "cluster",
        # "children" : [
        # {"name": "aname", "size" : 0}
        # ]

        # innermost children are held in curly brackets
        # then square brackets
        # outermost are curly brackets

        # order and split folder strings
        for dir in folderList:
            leftSide = ""
            rightSide = ""
            for letterIndex in range(len(dir)-1, 1, -1):
                 if dir[letterIndex] == "\\":
                    leftSide = dir[:letterIndex]
                    rightSide = dir[(letterIndex + 1):]
                    insertIntoDataStruct(leftSide, rightSide, JsonDict)
                    print "left: %s | right: %s" % (leftSide, rightSide)
                    break


        print JsonDict

        # Show results
        print "\n"
        print "I have scanned %s folders and changed %s of them." % (dirsChecked, dirsChanged)
        print "\n"
        print "A log of the folders changed has been written to the root folder %s" % rootDir
        print "\n"
        print "----------------------------------------------------"
        print "Folder renaming complete."
        print "Goodbye."
        print "----------------------------------------------------"
        return

    # Handle errors
    except ValueError:
        print "Value error."
    except IOError:
        print "Cannot access a file. Perhaps somebody is in the log file %s/FolderNameChangeLog.csv?" % rootDir
    #except:
    #    print "Error - Something unexpected happened with %s. Not all the folders have been changed." % root

renameFolders("H:\\Tests", "1_2", "goodname")






### GUI ###
#
# class TkFileDialog(Tkinter.Frame):
#     #InputFile = "G:\\Database_Team\\Regular Imports\\Fulfillment Agency\\Valldata\\Housefiles\\Weekly\\20140220\\Valldata_Organisation_Relationship.csv"
#     def __init__(self, root):
#         rootDir = ""
#         r = Tkinter.StringVar()
#         r.set("No Folder Selected")
#         nameFrom = Tkinter.StringVar()
#         nameTo = Tkinter.StringVar()
#         nameFrom.set("")
#         nameTo.set("")
#         print "----------------------------------------------------"
#         print ("Folder Renamer - Petri Autio 2014")
#         print "----------------------------------------------------"
#         print "\nSelect the root directory, then write the current "
#         print "folder name and finally the desired folder name and"
#         print "I will rename all such folders under the root.\n"
#         print "----------------------------------------------------"
#
#         def getDir():
#             global rootDir
#
#             rootDir = str(tkFileDialog.askdirectory(initialdir="C:\\test\\"))
#             r.set(rootDir)
#             print "Root set to %s" % rootDir
#
#         def process():
#             global rootDir
#             nameFrom = T3.get()
#             nameTo = T4.get()
#
#             print ("Converting folders under " + rootDir + " called " + str(nameFrom) + " to folders called " + str(nameTo)) + "."
#             print "----------------------------------------------------"
#
#             renameFolders(rootDir, nameFrom, nameTo)
#
#         Tkinter.Frame.__init__(self, root)
#         button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 20}
#         text_opt = {'fill' : Tkconstants.NONE, 'padx': 1, 'pady':1}
#
#         L2 = Tkinter.Label(self, textvariable=r)
#         Tkinter.Button(self, text='Choose Root Folder', command=getDir).pack(fill = Tkinter.X)
#         L1 = Tkinter.Label(self, text="Current Folder:")
#         L1.pack(fill = Tkinter.X)
#         L2.pack(fill = Tkinter.X)
#         L3 = Tkinter.Label(self, text="Current Folder Name")
#         L3.pack( fill = Tkinter.X)
#         T3 = Tkinter.Entry(self, bd=5)
#         T3.pack( fill = Tkinter.X)
#         L4 = Tkinter.Label(self, text="Desired Folder Name")
#         L4.pack( fill = Tkinter.X)
#         T4 = Tkinter.Entry(self, bd=5)
#         T4.pack( fill = Tkinter.X)
#
#         Tkinter.Button(self, text='Convert', command=process).pack(fill = Tkinter.X)
#
# if __name__=='__main__':
#   root = Tkinter.Tk()
#   root.wm_title("Folder Renamerer - Petri Autio 2014")
#   TkFileDialog(root).pack()
#  root.mainloop()