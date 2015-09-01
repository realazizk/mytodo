#!/usr/bin/env python2
#Copyright (C) 2015 Mohamed Aziz knani

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>

import time
import wx
import tools
import sys
from datetime import datetime, timedelta

class mytodoGui(wx.Frame):

  CONNECT_DATA = wx.NewId()
  NEW          = wx.NewId()
  UN_DONE      = wx.NewId()
  UPDATE       = wx.NewId()
  DELETE       = wx.NewId()
  def __init__(self, *args, **kwargs):
    super(mytodoGui, self).__init__(*args, **kwargs)
    panel = wx.Panel(self)
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    self.user, self.sock  = tools.initall()
    self.user = tools.connectuser(self.user, self.sock)
    self.clie = tools.Client(self.sock, self.user['user'],
                           self.user['token'])
    #print out
    self.listctrl = wx.ListCtrl(panel, 2, style=wx.LC_REPORT)
    hbox.Add(self.listctrl, 1, wx.EXPAND | wx.ALL, 20)
    btnPanel = wx.Panel(panel, -1)
    vbox = wx.BoxSizer(wx.VERTICAL)
    new = wx.Button(btnPanel, self.NEW, 'New', size=(90, 30))
    ren = wx.Button(btnPanel, self.UN_DONE, '(Un)Done', size=(90, 30))
    dlt = wx.Button(btnPanel, self.DELETE, 'Delete', size=(90, 30))
    clr = wx.Button(btnPanel, self.UPDATE, 'Update', size=(90, 30))
    status = self.CreateStatusBar()
    menubar = wx.MenuBar()
    connectmenu = wx.Menu()

    self.il = wx.ImageList(24,24, True)
    for name in [tools.currdir('close.png'), tools.currdir('done.png')]:
      bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
      self.il.Add(bmp)

    self.listctrl.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

    connectmenu.Append(self.CONNECT_DATA, 'Connect', 'Connect to a mytodo server')

    menubar.Append(connectmenu, 'Options')
    self.SetMenuBar(menubar)
    self.listctrl.SetImageList(self.il, wx.IMAGE_LIST_SMALL)

    self.Bind(wx.EVT_MENU, self.ConnectMenu, id=self.CONNECT_DATA)
    self.Bind(wx.EVT_BUTTON, self.Add, id=self.NEW)
    self.Bind(wx.EVT_BUTTON, self.Undone, id=self.UN_DONE)
    self.Bind(wx.EVT_BUTTON, self.Reload, id=self.UPDATE)
    self.Bind(wx.EVT_BUTTON, self.Delete, id=self.DELETE)

    vbox.Add((-1, 20))
    vbox.Add(new)
    vbox.Add(ren, 0, wx.TOP, 5)
    vbox.Add(dlt, 0, wx.TOP, 5)
    vbox.Add(clr, 0, wx.TOP, 5)
    btnPanel.SetSizer(vbox)
    hbox.Add(btnPanel, 0.6, wx.EXPAND | wx.RIGHT, 20)
    panel.SetSizer(hbox)
    self.Reload()

  def ConnectMenu(self, e):
    print 'hello'

  def Add(self, e):
    text = wx.GetTextFromUser('Enter your TODO', 'Insert Dialog')
    if text != '':
      self.clie(text)
    self.Reload()

  def Reload(self, e=1):
    self.listctrl.ClearAll()
    self.listctrl.InsertColumn(0, "Text")
    self.listctrl.InsertColumn(1, "Date")
    out = self.clie.listall()
    self.out = out
    for i, e in enumerate(out):

      #parsed = datetime.today() - timedelta(e[4])
      parsed = time.strptime(e[4], "%Y/%m/%d %H:%M:%S")
      d = (datetime.today() - datetime(parsed.tm_year, parsed.tm_mon, parsed.tm_mday)).days
      dayz = str(d)+' days ago' if d else 'today'
      #self.listctrl.Append( [e[2], time.strftime('%A %B %Y', parsed)] )
      img_id = 1 if e[3] else 0
      index = self.listctrl.InsertStringItem(sys.maxint, e[2], img_id)
      self.listctrl.SetStringItem(index, 1, dayz)
    #print self.il.GetImageCount()

    for i in range(2):
      self.listctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)

  def Undone(self, e):
    me = self.listctrl.GetFirstSelected()
    if self.out[me][3]:
      self.clie.undone(me)
    else :
      self.clie.done(me)
    self.Reload()

  def Delete(self, e):
    me = self.listctrl.GetFirstSelected()
    if self.onExclamation(1):
      self.clie.remove(me)
      self.Reload()
  def onExclamation(self, event):
      msg = "Are you sure you want to delete the todo ?"
      return self.showMessageDlg(msg, "Question",
                          wx.YES_NO|wx.YES_DEFAULT|wx.ICON_QUESTION)

  def showMessageDlg(self, msg, title, style):
      dlg = wx.MessageDialog(parent=None, message=msg,
                              caption=title, style=style)
      if dlg.ShowModal() == wx.ID_YES:
        dlg.Destroy()
        return True
      dlg.Destroy()
      return False

if __name__ == '__main__':
  app = wx.App()
  mytg = mytodoGui(None, -1, 'mytodo')
  mytg.Show()
  app.MainLoop()

