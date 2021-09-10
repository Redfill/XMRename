import pymel.core as pm
import json
import os

class RenameEntry(object):
    entry = {}

    def __init__(self, L=None, R=None):
        pm.button(XMRenameWindow.renameButton, e=True, en=True)
        RenameEntry.entry["entry"+str(len(RenameEntry.entry))] = self
        if L!= None and R!= None:
            self.LEntry = L
            self.REntry = R
        else:
            self.LEntry = ""
            self.REntry = ""
        pm.setParent(XMRenameWindow.EntryRow)
        self.L = pm.textField(tx=self.LEntry)
        self.R = pm.textField(tx=self.REntry)

def XMRenameEntry():
    selected = pm.ls(sl=True)
    for sel in selected:
        for ent in RenameEntry.entry:
            L = RenameEntry.entry[ent].L.getText()
            R = RenameEntry.entry[ent].R.getText()
            objName = sel.name()
            sel.rename(str(objName).replace(L,R))
            if objName == sel.name():
                sel.rename(str(objName).replace(R, L))



def XMSaveEntry():
    file = pm.internalVar(usd=True) + "XMRename/"
    data = {}
    data['entries'] = []
    for ent in RenameEntry.entry:
        L = RenameEntry.entry[ent].L.getText()
        R = RenameEntry.entry[ent].R.getText()
        if L == '' and R == '':
            continue

        data['entries'].append({
            'L': L,
            'R': R
        })

    with open(file+'entry.json', 'w') as outfile:
        json.dump(data,outfile)

def XMLoadEntry():
    file = pm.internalVar(usd=True) + "XMRename/"
    if os.path.isdir(file):
        if os.path.exists(file+'entry.json') == False:
            return
    else:
        os.mkdir(file)
        return
    with open(file +'entry.json', 'r') as json_file:
        data = json.load(json_file)
        for p in data['entries']:
            RenameEntry(L = p['L'], R = p['R'])


def XMSearchReplace():
    selected = pm.ls(sl=True)
    for sel in selected:
        search = XMRenameWindow.searchField.getText()
        replace = XMRenameWindow.replaceField.getText()
        objName = sel.name()
        sel.rename(str(objName).replace(search,replace))


class XMRenameWindows(object):
    def __init__(self):

        self.window = "XMRename"
        self.title = "XM Rename"
        self.size = (200,400)

        # close old window is open
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)

        # create new window
        self.window = pm.window(self.window, title=self.title, widthHeight=self.size,rtf=True)

        self.menu = pm.menuBarLayout()
        pm.menu(l="edit")
        pm.menuItem(l="save entries",c="XMSaveEntry()")

        # entry based rename
        self.Entryframe = pm.frameLayout(l="Entry Rename",mh=10, bgc=(0.5,0.2,0.2))
        pm.button(l="new Entry",c="RenameEntry()")

        self.EntryRow = pm.rowColumnLayout(nc=2)
        pm.text(l="L")
        pm.text(l="R")

        pm.setParent(self.Entryframe)
        self.renameButton = pm.button(l="Entry Rename", c="XMRenameEntry()", en=False)

        # search and replace rename
        pm.setParent(self.menu)
        self.searchFrame = pm.frameLayout(l="Search and Replace",mh=10,bgc=(0.2,0.5,0.2))
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="search:", al="left")
        self.searchField = pm.textField()
        pm.text(l="replace:", al="left")
        self.replaceField = pm.textField()
        pm.setParent(self.searchFrame)
        pm.button(l="Search Replace rename", c="XMSearchReplace()")


        # display new window
        pm.showWindow()

XMRenameWindow = XMRenameWindows()
XMLoadEntry()
