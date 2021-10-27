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


def XMJointMirror():
    joints = pm.ls(sl=True)
    torename = list()

    for jnt in joints:
        print(jnt)
        mirrorJoints = pm.mirrorJoint(jnt, mirrorBehavior=True, myz=True)
        torename.append(mirrorJoints)
    pm.select(torename)
    XMRenameEntry()
    XMSearchReplace("_bjnt1","_bjnt")
    XMSearchReplace("_jnt1", "_jnt")




def XMSearchReplace(s=None,r=None):
    selected = pm.ls(sl=True)
    if s == None:
        search = XMRenameWindow.searchField.getText()
        replace = XMRenameWindow.replaceField.getText()
    else:
        search = s
        replace = r
    for sel in selected:
        objName = sel.name()
        sel.rename(str(objName).replace(search,replace))

def XMPrefixSuffix(type=None, tx=None):
    selected = pm.ls(sl=True)
    prefix = XMRenameWindow.prefixField.getText()
    suffix = XMRenameWindow.suffixField.getText()
    if tx != None:
        prefix = tx
        suffix = tx

    for sel in selected:
        objName = sel.name()
        if type == "prefix":
            sel.rename(prefix+objName)
        else:
            sel.rename(objName+suffix)

def XMenumerate():
    selected = pm.ls(sl=True)
    name = XMRenameWindow.enumField.getText()
    start = XMRenameWindow.enumStart.getValue()
    padding = XMRenameWindow.enumPadding.getValue() +1
    #todo fix double renaming adding to number
    for sel in selected:
        sel.rename(name+str(f'{start:{0}{padding}}') )
        start += 1
    start = XMRenameWindow.enumStart.getValue()


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
        self.Entryframe = pm.frameLayout(l="Entry Rename",mh=10, bgc=(0.5,0.2,0.2), cll=True)
        pm.button(l="new Entry",c="RenameEntry()")

        self.EntryRow = pm.rowColumnLayout(nc=2)
        pm.text(l="L")
        pm.text(l="R")

        pm.setParent(self.Entryframe)
        self.renameButton = pm.button(l="Entry Rename", c="XMRenameEntry()", en=False)
        pm.popupMenu(b=3)
        pm.menuItem(l="joint mirror entry", c="XMJointMirror()")

        # search and replace rename
        pm.setParent(self.menu)
        self.searchFrame = pm.frameLayout(l="Search and Replace",mh=10,bgc=(0.2,0.5,0.2), cll=True)
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="search:", al="left")
        self.searchField = pm.textField()
        pm.text(l="replace:", al="left")
        self.replaceField = pm.textField()
        pm.setParent(self.searchFrame)
        pm.button(l="Search Replace rename", c="XMSearchReplace()")
        pm.popupMenu(b=3)
        pm.menuItem(l="remove _bjnt", c="XMSearchReplace('_bjnt','')")

        # prefix suffix rename
        pm.setParent(self.menu)
        self.prefixlayout = pm.frameLayout(l="prefix suffix", mh=10, bgc=(0.2,0.2,0.5), cll=True)
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="prefix:")
        self.prefixField = pm.textField()
        pm.setParent(self.prefixlayout)
        pm.button(l="add prefix", c="XMPrefixSuffix(type='prefix')")
        pm.popupMenu(b=3)
        pm.menuItem(l="L_", c="XMPrefixSuffix(type='prefix',tx='L_')")
        pm.menuItem(l="R_", c="XMPrefixSuffix(type='prefix',tx='R_')")
        
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="suffix:")
        self.suffixField = pm.textField()
        pm.setParent(self.prefixlayout)
        pm.button(l="add suffix", c="XMPrefixSuffix(type='suffix')")
        pm.popupMenu(b=3)
        pm.menuItem(l="_bjnt", c="XMPrefixSuffix(type='suffir',tx='_bjnt')")
        pm.menuItem(l="_jnt", c="XMPrefixSuffix(type='suffir',tx='_jnt')")
        pm.menuItem(l="_ctrl", c="XMPrefixSuffix(type='suffir',tx='_ctrl')")
        pm.menuItem(l="_srtBuffer", c="XMPrefixSuffix(type='suffir',tx='_srtBuffer')")

        #enumaration rename
        pm.setParent(self.menu)
        self.enumLayout = pm.frameLayout(l="enumeration", mh=10, bgc=(0.2,0.5,0.5), cll=True)
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="rename")
        self.enumField = pm.textField()
        pm.setParent(self.enumLayout)
        pm.rowColumnLayout(nc=2)
        pm.text(l="start#")
        pm.text(l="padding")
        self.enumStart = pm.intField(v=1)
        self.enumPadding = pm.intField()
        pm.setParent(self.enumLayout)
        pm.button(l="enumerate", c="XMenumerate()")








        # display new window
        pm.showWindow()

XMRenameWindow = XMRenameWindows()
XMLoadEntry()
