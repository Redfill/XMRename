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
            objName = sel.nodeName()
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
        objName = sel.nodeName()
        sel.rename(str(objName).replace(search,replace))

def XMPrefixSuffix(type=None, tx=None):
    selected = pm.ls(sl=True)
    if tx != None:
        prefix = tx
        suffix = tx
    else:
        prefix = XMRenameWindow.prefixField.getText()
        suffix = XMRenameWindow.suffixField.getText()
    for sel in selected:
        objName = sel.nodeName()
        if type == "prefix":
            sel.rename(prefix+objName)
            print(prefix)
            print(objName)
        else:
            sel.rename(objName+suffix)

def XMenumerate(name=None,start=None, padding=None):
    selected = pm.ls(sl=True)
    if name == None:
        name = XMRenameWindow.enumField.getText()
        start = XMRenameWindow.enumStart.getValue()
        padding = XMRenameWindow.enumPadding.getValue() +1
    else:
        name = name
        start = start
        padding = padding
    #todo fix double renaming adding to number
    for sel in selected:
        sel.rename(name+str(f'{start:{0}{padding}}') )
        start += 1

    #start = XMRenameWindow.enumStart.getValue()

def XMEndJnt():
    selected = pm.ls(sl=True)
    jnt = selected[0]
    endjnt = selected[1]

    endjnt.rename(str(jnt.nodeName().replace("_bjnt","").replace("_jnt","")+"End_jnt"))


def PopRenameInterpreter():
    win = XMPopRenameWindow
    txt = win.field.getText()
    commands = txt.split(",")
    print(commands)

    if commands[0] == "!":
        win.closewindow()
        return

    for c in commands:
        print("pass")
        if c[0] == "<":
            XMPrefixSuffix("suffix", c[1:])
            continue
        print("pass1")
        if c[0] == ">":
            XMPrefixSuffix("prefix", c[1:])
            continue
        print("pass2")
        if ":" in c:
            sr = c.split(":")
            XMSearchReplace(sr[0],sr[1])
            continue

        if "[" in c:
            e = c.split("[")
            print(e[1][:1])
            XMenumerate(e[0],1,str(e[1][:1]))
            continue


        print("pass3")
        sl= pm.ls(sl=True)
        for s in sl:
            pm.rename(s,c)

    pm.setFocus(win.field)





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
        pm.menuItem(l="bjnt to FkJnt", c="XMSearchReplace('_bjnt','_FkJnt')")
        pm.menuItem(l="bjnt to IkJnt", c="XMSearchReplace('_bjnt','_IkJnt')")


        # prefix suffix rename
        pm.setParent(self.menu)
        self.prefixlayout = pm.frameLayout(l="prefix suffix", mh=10, bgc=(0.2,0.2,0.5), cll=True)
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="prefix:")
        self.prefixField = pm.textField(ec="XMPrefixSuffix(type='prefix')")
        pm.setParent(self.prefixlayout)
        pm.button(l="add prefix", c="XMPrefixSuffix(type='prefix')")
        pm.popupMenu(b=3)
        pm.menuItem(l="L_", c="XMPrefixSuffix(type='prefix',tx='L_')")
        pm.menuItem(l="R_", c="XMPrefixSuffix(type='prefix',tx='R_')")
        
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="suffix:")
        self.suffixField = pm.textField(ec="XMPrefixSuffix(type='suffix')")
        pm.setParent(self.prefixlayout)
        pm.button(l="add suffix", c="XMPrefixSuffix(type='suffix')")
        pm.popupMenu(b=3)
        pm.menuItem(l="_bjnt", c="XMPrefixSuffix(type='suffir',tx='_bjnt')")
        pm.menuItem(l="_jnt", c="XMPrefixSuffix(type='suffir',tx='_jnt')")
        pm.menuItem(l="_ctrl", c="XMPrefixSuffix(type='suffir',tx='_ctrl')")
        pm.menuItem(l="_srtBuffer", c="XMPrefixSuffix(type='suffir',tx='_srtBuffer')")
        pm.menuItem(l="EndJnt", c="XMEndJnt()")

        #enumaration rename
        pm.setParent(self.menu)
        self.enumLayout = pm.frameLayout(l="enumeration", mh=10, bgc=(0.2,0.5,0.5), cll=True)
        pm.rowColumnLayout(nc=2, cw=[(1,60),(2,150)])
        pm.text(l="rename")
        self.enumField = pm.textField(ec="XMenumerate()")
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

class XMPopRenameWindows(object):
    def __init__(self):

        self.window = "XMPopRename"
        self.title = "XM Pop Rename"
        self.size = (300,50)

        # close old window is open
        if pm.window(self.window, exists=True):
            pm.deleteUI(self.window, window=True)

        # create new window
        self.window = pm.window(self.window, title=self.title, widthHeight=self.size,rtf=True, tb=False)
        pm.frameLayout(lv=False)
        self.field = pm.textField(w=300,h=50, ec="PopRenameInterpreter()", aie=True)
        # display new window
        pm.showWindow()

    def closewindow(self):
        pm.deleteUI(self.window, window=True)

XMRenameWindow = XMRenameWindows()
XMLoadEntry()

#XMPopRenameWindow = XMPopRenameWindows()
