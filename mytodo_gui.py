#!/usr/bin/env python2

import time
import wx
import mytodo_cli
import sys

class mytodoGui(wx.Frame):

  CONNECT_DATA = wx.NewId()
  NEW          = wx.NewId()
  UN_DONE      = wx.NewId()
  UPDATE       = wx.NewId()
  def __init__(self, *args, **kwargs):
    super(mytodoGui, self).__init__(*args, **kwargs)
    panel = wx.Panel(self)
    hbox = wx.BoxSizer(wx.HORIZONTAL)
    self.user  = {
      'user'  : 'mohamed',
      'pass'  : 'root',
      'token' : ''
    }
    self.user = mytodo_cli.connectuser(self.user)

    #print out
    self.listctrl = wx.ListCtrl(panel, 2, style=wx.LC_REPORT)
    hbox.Add(self.listctrl, 1, wx.EXPAND | wx.ALL, 20)
    btnPanel = wx.Panel(panel, -1)
    vbox = wx.BoxSizer(wx.VERTICAL)
    new = wx.Button(btnPanel, self.NEW, 'New', size=(90, 30))
    ren = wx.Button(btnPanel, self.UN_DONE, '(Un)Done', size=(90, 30))
    dlt = wx.Button(btnPanel, wx.NewId(), 'Delete', size=(90, 30))
    clr = wx.Button(btnPanel, self.UPDATE, 'Update', size=(90, 30))
    status = self.CreateStatusBar()
    menubar = wx.MenuBar()
    connectmenu = wx.Menu()

    self.il = wx.ImageList(24,24, True)
    for name in ['close.png', 'done.png']:
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
      mytodo_cli.add(text, self.user['user'], self.user['token'])
    self.Reload()

  def Reload(self, e=1):
    self.listctrl.ClearAll()
    self.listctrl.InsertColumn(0, "Text")
    self.listctrl.InsertColumn(1, "Date")
    out = mytodo_cli.listall(self.user['user'], self.user['token'])
    self.out = out
    for i, e in enumerate(out):
      parsed = time.strptime(e[4], "%Y/%m/%d %H:%M:%S")
      #self.listctrl.Append( [e[2], time.strftime('%A %B %Y', parsed)] )
      img_id = 1 if e[3] else 0
      index = self.listctrl.InsertStringItem(sys.maxint, e[2], img_id)
      self.listctrl.SetStringItem(index, 1, time.strftime('%A %B %Y', parsed))
    #print self.il.GetImageCount()

    for i in range(2):
      self.listctrl.SetColumnWidth(i, wx.LIST_AUTOSIZE)

  def Undone(self, e):
    me = self.listctrl.GetFirstSelected()
    if self.out[me][3]:
      mytodo_cli.undone(me, self.user['user'], self.user['token'])
    else :mytodo_cli.done(me, self.user['user'], self.user['token'])
    self.Reload()

if __name__ == '__main__':
  app = wx.App()
  mytg = mytodoGui(None, -1, 'mytodo')
  mytg.Show()
  app.MainLoop()

