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
        pm.setParent(XMRenameWindow.row)
        self.L = pm.textField(tx=self.LEntry)
        self.R = pm.textField(tx=self.REntry)

def XMRename():
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


class XMRenameWindows(object):
    def __init__(self):

        self.window = "XMRename"
        self.title = "XM Rename"
        self.size = (500,200)

        # close old window is open
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)

        # create new window
        self.window = pm.window(self.window, title=self.title, widthHeight=self.size)

        pm.menuBarLayout()
        pm.menu(l="edit")
        pm.menuItem(l="save entries",c="XMSaveEntry()")

        self.frame = pm.frameLayout(l="rename")
        pm.button(l="new Entry",c="RenameEntry()")

        self.row = pm.rowColumnLayout(nc=2)
        pm.text(l="L")
        pm.text(l="R")

        pm.setParent(self.frame)
        self.renameButton = pm.button(l="rename", c="XMRename()", en=False)


        # display new window
        pm.showWindow()

XMRenameWindow = XMRenameWindows()
XMLoadEntry()
