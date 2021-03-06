# -*- coding: utf-8 -*-
"""
Created on Tue Aug  1 13:21:35 2017

@author: web66492
"""

#8x8 grid like oxford chip buttons with column labels
#load exisiting ap?
#save map
#select all
#clear all
#4x4/6x6
#add in column and row selection from labels
#add a location dropdown

import wx
import itertools
from ca import caget, caput
import pv
import sys

class MappingFrame(wx.Frame):
    """ This window displays a set of buttons """
    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        #overly complicated layout solution

        panel = wx.Panel(self)
        mapping_sizer = wx.GridBagSizer(8, 8)
        sizer = wx.GridBagSizer(2,3)
        column_sizer = wx.GridBagSizer(1, 8)
        row_sizer = wx.GridBagSizer(8, 1)
        location_sizer=wx.BoxSizer(wx.HORIZONTAL)
        box_options_vertical = wx.BoxSizer(wx.VERTICAL)
        box_options_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        selecter_horizontal = wx.BoxSizer(wx.HORIZONTAL)
        loader = wx.BoxSizer(wx.HORIZONTAL)
        saver = wx.BoxSizer(wx.HORIZONTAL)

        rows = ['A','B','C','D','E','F','G','H']
        columns = list(range(1,9))
        button_names = list(itertools.product(rows,columns))
        print button_names
        button_labels = ['%s%s'%(label[0],label[1]) for label in button_names]
        print button_labels

        locations = ['SACLA','i24']
        self.location_label = wx.StaticText(self,-1,"Location: ",style=wx.ALIGN_CENTRE)
        self.location_choice = wx.ComboBox(self,value='SACLA',choices=locations)
        self.location_choice.Bind(wx.EVT_COMBOBOX, self.OnCombo)
	
        location_sizer.Add(self.location_label,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        location_sizer.Add(self.location_choice,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        box_options_vertical.Add(location_sizer,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        self.save_text = wx.TextCtrl(self)
        self.load_text = wx.TextCtrl(self)

        for i,label in enumerate(columns):
            btn = wx.ToggleButton(self, label=str(label),size=(40,40))
            btn.SetBackgroundColour('Light Grey')
            btn.Bind(wx.EVT_TOGGLEBUTTON, self.OnColumn)
            column_sizer.Add(btn, pos=(0,i), flag=wx.ALL|wx.ALIGN_CENTER, border=5)
            

        for i,label in enumerate(rows):
            btn = wx.ToggleButton(self, label=label,size=(40,40))
            btn.SetBackgroundColour('Light Grey')
            btn.Bind(wx.EVT_TOGGLEBUTTON, self.OnRow )
            row_sizer.Add(btn,pos=(i,0), flag=wx.ALL|wx.ALIGN_CENTER, border=5)
            

        self.btn_ids = {}
        self.btn_names = {}

        flip = True
        for x, column in enumerate(columns):
            for y,row in enumerate(rows):
                i=x*8+y
                if i%8 == 0 and flip == False:
                    flip = True
                    z = 8 - (y+1)
                elif i%8 == 0 and flip == True:
                    flip = False
                    z = y
                elif flip == False:
                    z = y
                elif flip == True:
                    z = 8 - (y+1)
                else:
                    print('something is wrong')
                    break
                button_name = str(row)+str(column)
                lab_num = x*8+z
                label='%02.d'%(lab_num+1)
                btn = wx.ToggleButton(self, -1, label=label, size=(40,40))
                btn.Bind(wx.EVT_TOGGLEBUTTON, self.OnToggleClick )
                self.btn_ids[label]=btn.GetId()
                self.btn_names[label] = button_name
                print (button_name,lab_num,i,x,y,z)
                mapping_sizer.Add(btn, pos=(y,x), flag=wx.ALL|wx.ALIGN_CENTER, border=5)
                self.ButtonValue = False


        load_btn = wx.Button(self, label='Load Map')
        load_btn.Bind(wx.EVT_BUTTON, self.OnLoad)
        loader.Add(self.load_text,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        loader.Add(load_btn,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        box_options_vertical.Add(loader,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)


        all_off = wx.Button(self, label='All Off')
        all_off.Bind(wx.EVT_BUTTON, self.OnAllOff)
        box_options_horizontal.Add(all_off,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)

        all_on = wx.Button(self, label='All On')
        all_on.Bind(wx.EVT_BUTTON, self.OnAllOn)
        box_options_horizontal.Add(all_on,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)

        selecter_1 = wx.Button(self, label='4x4')
        selecter_1.Bind(wx.EVT_BUTTON, self.On4x4)
        selecter_horizontal.Add(selecter_1,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)

        selecter_2 = wx.Button(self, label='6x6')
        selecter_2.Bind(wx.EVT_BUTTON, self.On6x6)
        selecter_horizontal.Add(selecter_2,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)

        box_options_vertical.Add(box_options_horizontal, 0, flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        box_options_vertical.Add(selecter_horizontal,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)

        save_btn = wx.Button(self, label='Save Map')
        save_btn.Bind(wx.EVT_BUTTON, self.OnSave)
        saver.Add(self.save_text,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        saver.Add(save_btn,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)
        box_options_vertical.Add(saver,0,flag=wx.ALL|wx.ALIGN_CENTER,border=10)

        sizer.Add(column_sizer, pos=(0,2), flag=wx.EXPAND)
        sizer.Add(mapping_sizer, pos=(1,2), flag=wx.EXPAND)
        sizer.Add(row_sizer,pos=(1,1), flag=wx.EXPAND)
        sizer.Add(box_options_vertical,pos=(1,0),flag=wx.EXPAND)
        self.SetSizerAndFit(sizer)
        self.Centre()

        self.load_stock_map('clear')

    def OnColumn(self, Event):
        btn = Event.GetEventObject()
        column = btn.GetLabel()
        end_val = int(column)*8+1
        start_val = end_val - 8
        if btn.GetValue():
            for i in range(start_val, end_val):
#                pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
#                caput(pvar, 1)
                btn_id = self.btn_ids['%02.d'%i]
                btn = self.FindWindowById(btn_id)
                btn.SetBackgroundColour('Red')
                btn.SetValue(True)
                btn.Update()
        else:
            for i in range(start_val, end_val):
#                pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
#                caput(pvar, 0)
                btn_id = self.btn_ids['%02.d'%i]
                btn = self.FindWindowById(btn_id)
                btn.SetBackgroundColour('white')
                btn.SetValue(False)
                btn.Update()

    def OnRow(self,Event):
	#set it to know if all on etc has been used
        btn = Event.GetEventObject()
        row = btn.GetLabel()
        print(row)
        labels = [row+str(num) for num in range(1,9)]
	block_dict = dict((v,k) for k, v in self.btn_names.iteritems())
	print block_dict
        #block_dict = {v: k for k, v in self.btn_names.iteritems()}
        if btn.GetValue():
            for label in labels:
                i = block_dict[label]
#                pvar = 'ME14E-MO-IOC-01:GP' + str(int(i) + 10)
#                caput(pvar, 1)
                btn_id = self.btn_ids[i]
                btn = self.FindWindowById(btn_id)
                btn.SetBackgroundColour('Red')
                btn.SetValue(True)
                print(i,1,btn.GetValue())
                btn.Update()
        else:
             for label in labels:
                i = block_dict[label]
#                pvar = 'ME14E-MO-IOC-01:GP' + str(int(i) + 10)
#                caput(pvar, 0)
                print(i,0,btn.GetValue())
                btn_id = self.btn_ids[i]
                btn = self.FindWindowById(btn_id)
                btn.SetBackgroundColour('white')
                btn.SetValue(False)
                print(i,0,btn.GetValue())
                btn.Update()

    def OnAllOn(self, event):
        self.load_stock_map('x88')

    def OnAllOff(self, event):
        self.load_stock_map('clear')

    def OnSave(self, event):
        print "In OnButton: Save Map"
        map_name = self.save_text.GetValue()+ '.map'
        litemap_name = self.save_text.GetValue()+ '.lite'
        location = self.location_choice.GetValue()
        if location == 'i24':
            litemap_path = '/dls_sw/i24/scripts/fastchips/litemaps/'
        else:
            litemap_path = '/localhome/local/Documents/sacla/parameter_files/'
        print '\n\nSaving', litemap_path + map_name
        f = open(litemap_path + map_name,'w')
        print 'Printing only blocks with block_val == 1'
        #for btn_id in self.btn_ids:
        #       btn_id = self.btn_ids[block_num]
        #       btn = self.FindWindowById(btn_id)
        #       if btn.GetValue():
        #               print btn_id, btn.GetValue()
        #       line = '%02dstatus    P3%02d1 \t%s\n' %(x, x, block_val)
        #       f.write(line)
        for x in range(1, 65):
            block_str = 'ME14E-MO-IOC-01:GP%i' %(x+10)
            block_val = caget(block_str)
            if block_val == 1:
                print block_str, block_val
            line = '%02dstatus    P3%02d1 \t%s\n' %(x, x, block_val)
            f.write(line)
        f.close()
        f = open(litemap_path+litemap_name,'w')
        print '\n\nSaving', litemap_path + litemap_name
        #for btn_id in self.btn_ids:
        #       btn_id = self.btn_ids[block_num]
        #       btn = self.FindWindowById(btn_id)
        #       block_value = btn.GetValue()
        #       block_name = self.btn_names['%02.d'%btn_id]
        #       line = '%s	%s\n'%(block_name,block_val)
        #       f.write(line)
        for x in range(1, 65):
            block_str = 'ME14E-MO-IOC-01:GP%i' %(x+10)
            block_val = caget(block_str)
            block_name = self.btn_names['%02.d'%x]
            line = '%s	%s\n'%(block_name,block_val)
            f.write(line)
        f.close()
        print 10*'Done '
        return 0

    def OnLoad(self, event):
        print "In OnButton: Load Map"
        self.load_stock_map('clear')
	block_dict = dict((v,k) for k, v in self.btn_names.iteritems())
	print block_dict
        #block_dict = {v: k for k, v in self.btn_names.iteritems()}
        
        location = self.location_choice.GetValue()
        if location =='i24':
            litemap_path = '/dls_sw/i24/scripts/fastchips/litemaps/'
        else:
            litemap_path = '/localhome/local/Documents/sacla/parameter_files/'
            
        litemap_fid = self.load_text.GetValue()+ '.lite'
        print 'opening', litemap_path + litemap_fid
        f = open(litemap_path + litemap_fid, 'r')

        print 'please wait, loading LITE map'
        for line in f.readlines():
            entry = line.split()
            block_name = entry[0]
            yesno = entry[1]
            block_num = block_dict[block_name]
            pvar = 'ME14E-MO-IOC-01:GP' + str(int(block_num) + 10)
            print block_name, yesno, pvar, block_num
#            caput(pvar, yesno)
            btn_id = self.btn_ids[block_num]
            btn = self.FindWindowById(btn_id)
            if int(yesno) == 1:
		    print btn.GetValue()
		    btn.SetBackgroundColour('Red')
		    btn.SetValue(True)
		    print btn.GetValue()
		    btn.Update()
            else:
                print btn.GetValue()
                btn.SetBackgroundColour('White')
                btn.SetValue(False)
                print btn.GetValue()
            btn.Update()
        print 10*'Done '

    def On4x4(self, event):
        print "In OnButton: 4x4"
        self.load_stock_map('x44')

    def On6x6(self, event):
        print "In OnButton: 6x6"
        self.load_stock_map('x66')

    def OnToggleClick(self,Event):
        btn = Event.GetEventObject()
        print btn.GetValue()
        label = int(btn.GetLabel())
        print label, self.btn_names[btn.GetLabel()]
        if btn.GetValue():
            btn.SetBackgroundColour('Red')
            pvar = 'ME14E-MO-IOC-01:GP' + str(label + 10)
            caput(pvar, 1)
            print btn.GetValue(),True
        else:
            btn.SetBackgroundColour('White')
            pvar = 'ME14E-MO-IOC-01:GP' + str(label + 10)
            caput(pvar, 0)
            print btn.GetValue(), False

    def OnCombo(self, Event):
        combo = Event.GetEventObject()
        combo.SetLabel("selected "+ combo.GetValue() +" from Combobox")
        print combo.GetLabel()

    def load_stock_map(self,map_choice):
        print 'Please wait, adjusting lite map'
        #
        r33 = [19,18,17,26,31,32,33,24,25]
        r55 = [9,10,11,12,13,16,27,30,41,40,39,38,37,34,23,20] + r33
        r77 = [7,6,5,4,3,2,1,14,15,28,29,42,43,44,45,46,47,48,49,36,35,22,21,8] + r55
        #
        x22 = [28,29,36,37]
        h33 = [3,2,1,6,7,8,9,4,5]
        x33 = [31,32,33,40,51,50,49,42,41]
        x55 = [25,24,23,22,21,34,39,52,57,58,59,60,61,48,43,30] + x33
        x77 = [11,12,13,14,15,16,17,20,35,38,53,56,71,70,69,68,67,66,65,62,47,44,29,26] + x55
        x99 = [9,8,7,6,5,4,3,2,1,18,19,36,37,54,55,72,73,74,75,76,77,78,79,80,81,64,63,46,45,28,27,10] + x77
        x44 = [22,21,20,19,30,35,46,45,44,43,38,27,28,29,36,37]
        x49 = [x+1 for x in range(49)]
        x66 = [10,11,12,13,14,15,18,31,34,47,50,51,52,53,54,55,42,39,26,23] + x44
        x88 = [8,7,6,5,4,3,2,1,16,17,32,33,48,49,64,63,62,61,60,59,58,57,56,41,40,25,24,9] + x66

        map_dict = {}
        map_dict['clear']= []
        #
        map_dict['r33'] = r33
        map_dict['r55'] = r55
        map_dict['r77'] = r77
        #
        map_dict['h33'] = h33
        #
        map_dict['x22'] = x22
        map_dict['x33'] = x33
        map_dict['x44'] = x44
        map_dict['x49'] = x49
        map_dict['x55'] = x55
        map_dict['x66'] = x66
        map_dict['x77'] = x77
        map_dict['x88'] = x88
        map_dict['x99'] = x99
        print 'Clearing'
        for i in range(1, 65):
#            pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
#            caput(pvar, 0)
            btn_id = self.btn_ids['%02.d'%i]
            btn = self.FindWindowById(btn_id)
            btn.SetBackgroundColour('White')
            btn.SetValue(False)
            btn.Update()
            sys.stdout.write('.')
            sys.stdout.flush()
        print '\nmap cleared'
        print 'loading map_choice', map_choice
        for i in map_dict[map_choice]:
#            pvar = 'ME14E-MO-IOC-01:GP' + str(i + 10)
#            caput(pvar, 1)
            btn_id = self.btn_ids['%02.d'%i]
            btn = self.FindWindowById(btn_id)
            btn.SetBackgroundColour('Red')
            btn.SetValue(True)
            btn.Update()
            sys.stdout.write('.')
            sys.stdout.flush()
        print 10*'Done '

class MyApp(wx.App):
    def OnInit(self):
        frame = MappingFrame(None, -1, 'Mapping Lite Pi')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()

