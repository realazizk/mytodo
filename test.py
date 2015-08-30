import wx
import sys, glob

class DemoFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1,"wx.ListCtrl in wx.LC_ICON mode",size=(600,400))

        il = wx.ImageList(24,24, True)
        for name in glob.glob("*.png"):
            bmp = wx.Bitmap(name, wx.BITMAP_TYPE_PNG)
            il_max = il.Add(bmp)

        self.list = wx.ListCtrl(self, -1, style=wx.LC_ICON | wx.LC_AUTOARRANGE)

        self.list.AssignImageList(il, wx.IMAGE_LIST_NORMAL)

        for x in range(25):
            img = x % (il_max+1)
            self.list.InsertImageStringItem(x, "This is item %02d" % x, img)

app = wx.PySimpleApp()
frame = DemoFrame()
frame.Show()
app.MainLoop()
