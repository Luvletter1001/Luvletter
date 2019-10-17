# -*- coding:utf-8 -*-
# @Time : 2019/10/15 19:38
# @Author : Chengyi Zhao
# @File : BookManage.py
# @Software: VisualStudio Code

import wx
import pymysql
import xlwt

class LibraryFrame(wx.Frame):

    def __init__(self, parent, title):
        '''
        初始化系统总体布局，包括各种控件
        '''

        # 生成一个宽为950，高为412的frame框
        wx.Frame.__init__(self, parent, title=title, size=(950, 415))

        # 定一个网格布局,两行一列
        self.main_layout = wx.BoxSizer(wx.VERTICAL)

        # 生成一个列表
        self.list = wx.ListCtrl(self, -1, size=(950, 300), style=wx.LC_REPORT |
                                wx.LC_HRULES | wx.LC_VRULES)  # | wx.LC_SINGLE_SEL
        # 列表有散列，分别是书名，ISBN，作者，出版社，出版时间，入库时间，库存量，借阅数
        self.list.InsertColumn(0, "书名")
        self.list.InsertColumn(1, "ISBN")
        self.list.InsertColumn(2, "作者")
        self.list.InsertColumn(3, "出版社")
        self.list.InsertColumn(4, "出版时间")
        self.list.InsertColumn(5, "入库时间")
        self.list.InsertColumn(6, "库存量")
        self.list.InsertColumn(7, "借阅数")
        # 设置各列的宽度
        self.list.SetColumnWidth(0, 210)  # 设置每一列的宽度
        # self.list.SetCharHeight(0, 120) 
        self.list.SetColumnWidth(1, 170)
        self.list.SetColumnWidth(2, 150)
        self.list.SetColumnWidth(3, 120)
        self.list.SetColumnWidth(4, 80)
        self.list.SetColumnWidth(5, 80)
        self.list.SetColumnWidth(6, 60)
        self.list.SetColumnWidth(7, 60)
        # 添加一组按钮，实现增删改查,用一个panel来管理该组按钮的布局
        self.panel = wx.Panel(self, pos=(0, 300), size=(950, 115))

        # 定义一组按钮
        add_button = wx.Button(self.panel, label="添加", pos=(
            100, 5), size=(60, 30))  # , size = (75, 30)
        del_button = wx.Button(self.panel, label="删除", pos=(
            300, 5), size=(60, 30))  # , size = (75, 30)
        update_button = wx.Button(self.panel, label="修改", pos=(
            500, 5), size=(60, 30))  # , size = (75, 30)
        query_button = wx.Button(self.panel, label="搜索", pos=(
            700, 5), size=(60, 30))  # , size = (75, 30)


        lend_button = wx.Button(self.panel, label="借书", pos=(
            100, 38), size=(60, 30))  # , size = (75, 30)
        back_button = wx.Button(self.panel, label="还书", pos=(
            300, 38), size=(60, 30))  # , size = (75, 30)
        count_button = wx.Button(self.panel, label="统计", pos=(
            500, 38), size=(60, 30))  # , size = (75, 30)
        out_button = wx.Button(self.panel, label="导出", pos=(
            700, 38), size=(60, 30))  # , size = (75, 30)
        # w为按钮绑定相应事件函数，第一个参数为默认参数，指明为按钮类事件，第二个为事件函数名，第三个为按钮名
        self.Bind(wx.EVT_BUTTON, self.addBook, add_button)
        self.Bind(wx.EVT_BUTTON, self.delBook, del_button)
        self.Bind(wx.EVT_BUTTON, self.updateBook, update_button)
        self.Bind(wx.EVT_BUTTON, self.queryBook, query_button)
        self.Bind(wx.EVT_BUTTON, self.lendBook, lend_button)
        self.Bind(wx.EVT_BUTTON, self.backBook, back_button)
        self.Bind(wx.EVT_BUTTON, self.countBook, count_button)
        self.Bind(wx.EVT_BUTTON, self.outBook, out_button)
        # 将列表和panel添加到主面板
        self.main_layout.Add(self.list, 3)
        self.main_layout.Add(self.panel, 1)

        self.SetSizer(self.main_layout)

        # 添加数据库操作对象
        # self.dbhelper = DBHelper()
        # datas = self.dbhelper.getAllBook()
        datas = self.getAllBook()

        for data in datas:
            index = self.list.InsertItem(
                self.list.GetItemCount(), str(data[0]))
            self.list.SetItem(index, 1, str(data[1]))
            self.list.SetItem(index, 2, str(data[2]))
            self.list.SetItem(index, 3, str(data[3]))
            self.list.SetItem(index, 4, str(data[4]))
            self.list.SetItem(index, 5, str(data[5]))
            self.list.SetItem(index, 6, str(data[6]))
            self.list.SetItem(index, 7, str(data[7]))
        self.Show()

    def getAllBook(self):
        '''返回数据库中，table1表中所有的物品信息'''
        sql = "select *from table1"
        cursor.execute(sql)
        # 获取查询结果
        rows = cursor.fetchall()
        list = []

        for item in rows:
            # bitem = (item[2], item[3], item[4], item[5], item[6], item[7])
            bitem = (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7])
            list.append(bitem)

        # conn.commit()
        # cursor.close()
        # conn.close()

        return list

    def deleteBook(self, DelName):
        '''根据物品名删除物品'''
        DelName = "'" + DelName + "'"
        cursor.execute("delete from table1 where BookName= %s" % DelName)

        db.commit()

    def addBook(self, evt):
        '''添加按钮，弹出添加物品框'''
        add_f = AddFrame(self, "添加物品窗口")
        add_f.Show(True)

    def delBook(self, evt):
        '''删除书籍按钮，先选中,然后删除'''
        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(
                self, message="未选中任何条目！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            DelName = self.list.GetItem(selectId, 0).Text  # 得到物品名
            self.list.DeleteItem(selectId)  # 先在listctrl中删除选中行
            print(DelName)
            DelName = str(DelName)
            self.deleteBook(DelName)

    def updateBook(self, evt):
        '''修改按钮响应事件，点击修改按钮，弹出修改框'''
        selectId = self.list.GetFirstSelected()
        if selectId == -1:
            warn = wx.MessageDialog(
                self, message="未选中任何条目！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            update_f = UpdateFrame(self, "修改物品窗口", selectId)
            update_f.Show(True)

    def getBookById(self, BookName):
        '''根据物品名来寻找物品信息'''
        BookName =  BookName.replace("'","")
        cursor = db.cursor()
        cursor.execute(
            "select BookName, ISBN, Author,Publish, PublishTime, StoreTime,Stock,LendNum  from table1  where BookName like '%%%%%s%%%%'" % BookName)  # 参数以元组形式给出
        row = cursor.fetchone()  # 取到第一个结果
        print(row)
        db.commit()
        cursor.close()
        # db.close()

        return row  # 返回该书本信息
 
    def queryBook(self, evt):
        '''查看按钮响应事件'''
        # selectId = self.list.GetFirstSelected()
        # if selectId == -1:
        #     warn = wx.MessageDialog(self, message = "未选中任何条目！！！", caption = "错误警告", style = wx.YES_DEFAULT | wx.ICON_ERROR)
        #     warn.ShowModal()                                                             #提示错误
        #     warn.Destroy()
        #     return
        # else:
        show_s = SearchFrame(self,"搜索框","seq")
        show_s.Show()
            #show_f = ShowFrame(self, "修改书籍窗口", selectId)
            #show_f.Show(True)
 
    def lendBook(self,evt):
        show_s = SearchFrame(self,"搜索框","lend")
        show_s.Show()
 
    def backBook(self, evt):
        show_s = SearchFrame(self,"搜索框","back")
        show_s.Show()

    def countBook(self,evt):
        sql = "select LendNum from table1"
        cursor.execute(sql)
        # 获取查询结果
        rows = cursor.fetchall()
        cnt = 0
        for i in range(0,len(rows)-1):
            print(i)
            print(rows[i][0])
            cnt = cnt + int(rows[i][0])
        warn = wx.MessageDialog(self, message="总图书借出数为%s"%(cnt), caption="借出数统计", style=wx.YES_DEFAULT | wx.ICON_ERROR)
        warn.ShowModal()  # 提示错误
        warn.Destroy()
    
    def outBook(self,evt):
        open_workbook=xlwt.Workbook()
        new_sheet=open_workbook.add_sheet('test',cell_overwrite_ok = True)
        title = ['书名','ISBN','作者','出版社','出版时间','入库时间','库存量','借阅数']
        i = 0
        for header in title:
            new_sheet.write(0,i,header)
            i+=1
        sql = "select *from table1"
        cursor.execute(sql)
        # 获取查询结果
        rows = cursor.fetchall()
        for row in range(1,len(rows)):
            for col in range(0,len(rows[row])):
                new_sheet.write(row,col,rows[row][col])
            row+=1
        col+=1
        open_workbook.save('图书馆统计.xls')
        out = wx.MessageDialog(
                self, message="导出成功，请到程序同文件夹下查看", caption="导出提示", style=wx.YES_DEFAULT | wx.ICON_ERROR)
        out.ShowModal()  # 提示错误
        out.Destroy()
class AddFrame(LibraryFrame):
    '''添加物品弹出的小窗口'''

    def __init__(self, parent, title):
        '''初始化该小窗口的布局'''

        self.mainframe = parent
        # 生成一个300*300的框
        wx.Frame.__init__(self, parent, title=title, size=(400, 280))

        self.panel = wx.Panel(self, pos=(0, 0), size=(400, 280))
        self.panel.SetBackgroundColour("#FFFFFF")  # 背景为白色

        # 三个编辑框，分别用来编辑书名，作者，书籍相关信息
        ItemClass_tip = wx.StaticText(
            self.panel, label="       书名:", pos=(5, 8), size=(65, 25))
        ItemClass_tip.SetBackgroundColour("#FFFFFF")
        ItemClass_text = wx.TextCtrl(self.panel, pos=(70, 5), size=(300, 25))
        self.BookName = ItemClass_text

        ItemName_tip = wx.StaticText(
            self.panel, label="       ISBN:", pos=(5, 38), size=(65, 25))
        ItemName_tip.SetBackgroundColour("#FFFFFF")
        ItemName_text = wx.TextCtrl(self.panel, pos=(70, 35), size=(300, 25))
        self.ISBN = ItemName_text

        Itemnum_tip = wx.StaticText(
            self.panel, label="        作者:", pos=(5, 68), size=(65, 25))
        Itemnum_tip.SetBackgroundColour("#FFFFFF")
        Itemnum_text = wx.TextCtrl(self.panel, pos=(70, 65), size=(300, 25))
        self.Author = Itemnum_text

        State_tip = wx.StaticText(
            self.panel, label="    出版社:", pos=(5, 98), size=(65, 25))
        State_tip.SetBackgroundColour("#FFFFFF")
        State_text = wx.TextCtrl(self.panel, pos=(70, 95), size=(300, 25))
        self.Publish = State_text

        Lender_tip = wx.StaticText(
            self.panel, label="出版时间:", pos=(5, 128), size=(65, 25))
        Lender_tip.SetBackgroundColour("#FFFFFF")
        Lender_text = wx.TextCtrl(self.panel, pos=(70, 125), size=(300, 25))
        self.PublishTime = Lender_text

        Charger_tip = wx.StaticText(
            self.panel, label="入库时间:", pos=(5, 158), size=(65, 25))
        Charger_tip.SetBackgroundColour("#FFFFFF")
        Charger_text = wx.TextCtrl(self.panel, pos=(70, 155), size=(300, 25))
        self.StoreTime = Charger_text
        
        Stock_tip = wx.StaticText(
            self.panel, label="    库存量:", pos=(5, 188), size=(65, 25))
        Stock_tip.SetBackgroundColour("#FFFFFF")
        Stock_text = wx.TextCtrl(self.panel, pos=(70, 185), size=(300, 25))
        self.Stock = Stock_text       
        
        save_button = wx.Button(self.panel, label="添加", pos=(160, 210))
        self.Bind(wx.EVT_BUTTON, self.saveItem, save_button)

        # 需要用到的数据库接口
        # self.dbhelper = DBHelper()

    def saveItem(self, evt):
        '''第一步：获取text中文本；第二步，连接数据库；第三步插入并获得主键；第四步添加到ListCtrl中'''
        BookName = self.BookName.    GetValue()
        ISBN = self.ISBN.GetValue()
        Author = self.Author. GetValue()
        Publish = self.Publish.GetValue()
        PublishTime = self.PublishTime.  GetValue()
        StoreTime = self.StoreTime. GetValue()
        Stock = self.Stock. GetValue()
        # item = [ItemClass, ItemName, Itemnum, Lender, Charger]
        # for index in range(len(item)):
        # 	item[index] = "'" + item[index] +"'"
        # 	print(item[index])

        if BookName == "" or ISBN == "" or Author == "" or Publish == "" or PublishTime == "":
            warn = wx.MessageDialog(
                self, message="所有信息不能为空！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
            BookName = "'" + BookName + "'"
            ISBN = "'" + ISBN + "'"
            Author = "'" + Author + "'"
            Publish = "'" + Publish + "'"
            PublishTime = "'" + PublishTime + "'"
            StoreTime = "'" + StoreTime + "'"
            Stock = "'" + Stock + "'"
            LendNum = 0
            print("开始插入到数据库中")
            cursor.execute("insert into table1(BookName, ISBN, Author,Publish, PublishTime, StoreTime,Stock,LendNum) values(%s, %s, %s, %s ,%s,%s,%s,%s)" % (
                BookName, ISBN, Author,Publish, PublishTime, StoreTime,Stock,LendNum))
            SearchFrame.feadback(self,"添加")
            # sql = "select *from table1"
            # cursor.execute(sql)
            # 获取查询结果

            # index = LibraryFrame.list.InsertItem(self.list.GetItemCount(),BookName)
            # LibraryFrame.__init__.list.SetItem(index, 1, ISBN)
            # for item in rows:
            #     bitem = (item[2], item[3], item[4], item[5], item[6], item[7])

            #     list.append(bitem)
            # zhang = len(bitem)
            
            # LibraryFrame.list.AddItem(1)


            db.commit()

            self.Destroy()

class SearchFrame(wx.Frame):
    def __init__(self, parent, title,flag):
        '''搜索框'''
        # 便于调用父窗口
        self.mainframe = parent

        # 生成一个450*500的框
        wx.Frame.__init__(self, parent, title = title, size = (450, 450))

        self.panel = wx.Panel(self, pos = (0, 0), size = (450, 450))
        self.panel.SetBackgroundColour("#FFFFFF")                              #背景为白色

        # 五个编辑框，分别用来输出相关信息
        SearchName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 16), size = (65, 25))
        SearchName_tip.SetBackgroundColour("#FFFFFF")
        SearchName_text = wx.TextCtrl(self.panel, pos = (70, 10), size = (230, 25))
        self.SearchName = SearchName_text
        
        search_button = wx.Button(self.panel, label="搜索", pos=(320, 8))
        self.Bind(wx.EVT_BUTTON, self.search, search_button)
        if flag == "lend" :
            lend_button = wx.Button(self.panel, label="借出", pos=(320, 68))
            self.Bind(wx.EVT_BUTTON, self.lend, lend_button)
        if flag == "back" :
            back_button = wx.Button(self.panel, label="还书", pos=(320, 68))
            self.Bind(wx.EVT_BUTTON, self.back, back_button) 
        BookName_tip = wx.StaticText(self.panel, label = "书名:", pos = (5, 76), size = (65, 25))
        BookName_tip.SetBackgroundColour("#FFFFFF")
        BookName_text = wx.TextCtrl(self.panel, pos = (70, 70), size = (230, 25))
        BookName_text.SetEditable(False)
        self.BookName = BookName_text

        ISBN_tip = wx.StaticText(self.panel, label = "ISBN:", pos = (5, 116), size = (65, 25))
        ISBN_tip.SetBackgroundColour("#FFFFFF")
        ISBN_text = wx.TextCtrl(self.panel, pos = (70, 110), size = (230, 25))
        ISBN_text.SetEditable(False)
        self.ISBN = ISBN_text
       
        Author_tip = wx.StaticText(self.panel, label = "作者:", pos = (5, 156), size = (65, 25))
        Author_tip.SetBackgroundColour("#FFFFFF")
        Author_text = wx.TextCtrl(self.panel, pos = (70, 150), size = (230, 25))
        Author_text.SetEditable(False)
        self.Author = Author_text			

        Publish_tip = wx.StaticText(self.panel, label = "出版社:", pos = (5, 196), size = (65, 25))
        Publish_tip.SetBackgroundColour("#FFFFFF")
        Publish_text = wx.TextCtrl(self.panel, pos = (70, 190), size = (230, 25))
        Publish_text.SetEditable(False)
        self.Publish = Publish_text	

        PublishTime_tip = wx.StaticText(self.panel, label = "出版时间:", pos = (3, 236), size = (65, 25))
        PublishTime_tip.SetBackgroundColour("#FFFFFF")
        PublishTime_text = wx.TextCtrl(self.panel, pos = (70, 230), size = (230, 25))
        PublishTime_text.SetEditable(False)
        self.PublishTime = PublishTime_text	    

        Store_tip = wx.StaticText(self.panel, label = "入库时间:", pos = (3, 276), size = (65, 25))
        Store_tip.SetBackgroundColour("#FFFFFF")
        Store_text = wx.TextCtrl(self.panel, pos = (70, 270), size = (230, 25))
        Store_text.SetEditable(False)
        self.StoreTime = Store_text	

        Stock_tip = wx.StaticText(self.panel, label = "库存量:", pos = (5, 316), size = (65, 25))
        Stock_tip.SetBackgroundColour("#FFFFFF")
        Stock_text = wx.TextCtrl(self.panel, pos = (70, 310), size = (230, 25))
        Stock_text.SetEditable(False)
        self.Stock = Stock_text	

        LendNum_tip = wx.StaticText(self.panel, label = "借阅数:", pos = (5, 356), size = (65, 25))
        LendNum_tip.SetBackgroundColour("#FFFFFF")
        LendNum_text = wx.TextCtrl(self.panel, pos = (70, 350), size = (230, 25))
        LendNum_text.SetEditable(False)
        self.LendNum = LendNum_text
            # self.showAllText()
    
    def search(self,evt):

        SearchName = self.SearchName.GetValue()
        self.showAllText(SearchName)
    
    def lend(self,evt):
        SearchName = "'" + self.SearchName.GetValue() + "'"
        LendNum = int(self.LendNum.GetValue() )+1
        cursor = db.cursor()
        cursor.execute("update table1 set LendNum=%s where BookName=%s"%(LendNum,SearchName))

        db.commit()
        cursor.close()

        self.feadback("借书")
    def back(self,evt):
        SearchName = "'" + self.SearchName.GetValue() + "'"
        LendNum = int(self.LendNum.GetValue() )-1
        cursor = db.cursor()
        cursor.execute("update table1 set LendNum=%s where BookName=%s"%(LendNum,SearchName))
        db.commit()
        cursor.close()
        self.feadback("还书")
    def feadback(self,state):
        fead = wx.MessageDialog(
            self, message=str(state) + "成功", caption=str(state)+"反馈", style=wx.YES_DEFAULT | wx.ICON_ERROR)
        fead.ShowModal()  # 提示
        fead.Destroy()
    def showAllText(self, id):
            '''显示概述本原始信息'''
            id = "'" + str(id) + "'"
            db = pymysql.Connect(host='172.81.247.10', user='root',
                         passwd='password', db='db')
            db.ping(reconnect=True)
            cursor = db.cursor()
            try:
                data = LibraryFrame.getBookById(self, id)  # 通过id获取书本信息
                print(data)
                print("test")
                a = str(data[7])
                self.BookName.SetValue(data[0])  # 设置值
                self.ISBN.SetValue(data[1])
                self.Author.SetValue(data[2])
                self.Publish.SetValue(data[3])
                self.PublishTime.SetValue(data[4])
                self.StoreTime.SetValue(data[5])
                self.Stock.SetValue(data[6])
                self.LendNum.SetValue(a)
            except:
                none = "无"
                self.BookName.SetValue(none)  # 设置值
                self.ISBN.SetValue(none)
                self.Author.SetValue(none)
                self.Publish.SetValue(none)
                self.PublishTime.SetValue(none)
                self.StoreTime.SetValue(none)
                self.Stock.SetValue(none)
                self.LendNum.SetValue(none)

class UpdateFrame(wx.Frame):
    def __init__(self, parent, title, select_id):
        '''初始化更新图书信息界面总布局'''

        wx.Frame(parent, title=title, size=(450, 350))

        # 用来调用父frame,便于更新
        self.mainframe = parent
        # 生成一个300*300的框
        wx.Frame.__init__(self, parent, title=title, size=(450, 350))

        self.panel = wx.Panel(self, pos=(0, 0), size=(450, 350))
        self.panel.SetBackgroundColour("#FFFFFF")  # 背景为白色

        # 编辑框，分别用来编辑书名，作者，书籍相关信息
        BookName_tip = wx.StaticText(
            self.panel, label="书名:", pos=(5, 8), size=(65, 25))
        BookName_tip.SetBackgroundColour("#FFFFFF")
        BookName_text = wx.TextCtrl(self.panel, pos=(80, 5), size=(330, 25))
        self.BookName = BookName_text

        ISBN_tip = wx.StaticText(
            self.panel, label="ISBN:", pos=(5, 38), size=(65, 25))
        ISBN_tip.SetBackgroundColour("#FFFFFF")
        ISBN_text = wx.TextCtrl(self.panel, pos=(80, 35), size=(330, 25))
        self.ISBN = ISBN_text.GetValue()
        self.ISBN = ISBN_text

        Author_tip = wx.StaticText(self.panel, label="作者:",
                                pos=(5, 68), size=(65, 25))
        Author_tip.SetBackgroundColour("#FFFFFF")
        Author_text = wx.TextCtrl(self.panel, pos=(
            80, 65), size=(330, 25))
        self.Author =Author_text

        Publish_tip = wx.StaticText(self.panel, label="出版社:",
                                pos=(5, 98), size=(65, 25))
        Publish_tip.SetBackgroundColour("#FFFFFF")
        Publish_text = wx.TextCtrl(self.panel, pos=(
            80, 95), size=(330, 25))
        self.Publish = Publish_text
        
        PublishTime = wx.StaticText(
            self.panel, label="出版时间:", pos=(5, 128), size=(65, 25))
        PublishTime.SetBackgroundColour("#FFFFFF")
        PublishTime_text = wx.TextCtrl(self.panel, pos=(
            80, 125), size=(330, 25))
        self.PublishTime = PublishTime_text

        StoreTime = wx.StaticText(
            self.panel, label="入库时间:", pos=(5, 158), size=(65, 25))
        StoreTime.SetBackgroundColour("#FFFFFF")
        StoreTime = wx.TextCtrl(self.panel, pos=(
            80, 155), size=(330, 25))
        self.StoreTime = StoreTime
        Stock_tip = wx.StaticText(
            self.panel, label="库存:", pos=(5, 188), size=(65, 25))
        Stock_tip.SetBackgroundColour("#FFFFFF")
        Stock_text = wx.TextCtrl(self.panel, pos=(
            80, 185), size=(330, 25))
        self.Stock = Stock_text

        LendNum_tip = wx.StaticText(
            self.panel, label="借阅数:", pos=(5, 218), size=(65, 25))
        LendNum_tip.SetBackgroundColour("#FFFFFF")
        LendNum_text = wx.TextCtrl(self.panel, pos=(
            80, 215), size=(330, 25))
        self.LendNum = LendNum_text
        
        save_button = wx.Button(self.panel, label="保存修改", pos=(160, 250))
        self.Bind(wx.EVT_BUTTON, self.saveUpdate, save_button)

        # 选中的id和bookid
        self.select_id = select_id
        self.bookid = self.mainframe.list.GetItem(
            select_id, 0).Text  # 获取第select_id行的第1列的值
        print(select_id, self.bookid)
        bookid = "'" + self.bookid + "'"
        # 需要用到的数据库接口
        # self.dbhelper = DBHelper()
        self.showAllText(bookid)  # 展现所有的text原来取值
    
    def showAllText(self, bookid):
        '''显示概述本原始信息'''
        
        data = LibraryFrame.getBookById(self, bookid)  # 通过id获取书本信息
        # a = str(data[2])
        print(data)
        self.BookName.SetValue(data[0])  # 设置值
        self.ISBN .SetValue(data[1])
        self.Author.SetValue(data[2])
        self.Publish.SetValue(data[3])
        self.PublishTime.SetValue(data[4])
        self.StoreTime.SetValue(data[5])
        self.Stock.SetValue(data[6])
        self.LendNum.SetValue(str(data[7]))
    
    def saveUpdate(self, evt):
        '''保存修改后的值'''
        BookName = self.BookName.GetValue()  # 获得修改后的值
        ISBN  = self.ISBN.GetValue()
        Author   = self.Author     .GetValue()
        Publish= self.Publish.GetValue()
        PublishTime    = self.PublishTime  .GetValue()
        StoreTime   = self.StoreTime .GetValue()
        Stock    = self.Stock  .GetValue()
        LendNum   = self.LendNum .GetValue()

        print("书名:"+ BookName)
        if BookName == "" or ISBN == "" or Author == "" or Publish == "" or Publish == "":
            print("进来了")
            warn = wx.MessageDialog(
                self, message="所有信息不能为空！！！", caption="错误警告", style=wx.YES_DEFAULT | wx.ICON_ERROR)
            warn.ShowModal()  # 提示错误
            warn.Destroy()
            return
        else:
        # sql = "update book set book.name=%s, book.author=%s, book.content=%s where book.id=%s"

            # conn = self.getCon()
            # if conn == None:
            # 	return

            # cursor = conn.cursor()
            BookName = "'" + BookName + "'"
            ISBN = "'" + ISBN + "'"
            Author = "'" + Author + "'"
            Publish = "'" + Publish + "'"
            PublishTime = "'" + PublishTime + "'"
            StoreTime = "'" + StoreTime + "'"
            Stock = "'" + Stock + "'"
            LendNum = "'" + LendNum + "'"

            db = pymysql.Connect(host='172.81.247.10', user='root',
                         passwd='password', db='db')
            db.ping(reconnect=True)
            cursor = db.cursor()
            cursor.execute("update table1 set BookName=%s,ISBN=%s,Author=%s,Publish=%s,PublishTime=%s,StoreTime=%s, Stock=%s where BookName=%s"%(BookName, ISBN, Author,Publish, PublishTime, StoreTime,Stock,LendNum))

            db.commit()
            cursor.close()

            self.Destroy()


# 类似于c中的main函数，但被其他模块导入时，__name__值不是"__main__"
if __name__ == "__main__":
    app = wx.App()
    try:
        db = pymysql.Connect(host='172.81.247.10', user='root',
                             passwd='password', db='db')
        db.ping(reconnect=True)
        cursor = db.cursor()
        frame = LibraryFrame(None, "图书管理系统")
        app.MainLoop()
    except:
        worn = wx.MessageDialog(
            self, message="数据库连接失败，请检查网络连接！", caption="TimeOut", style=wx.YES_DEFAULT | wx.ICON_ERROR)
        worn.ShowModal()  # 提示
        worn.Destroy()
