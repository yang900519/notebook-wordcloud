#!/usr/bin/env python
# coding: utf-8

# In[30]:


from tkinter import *
from tkinter.filedialog import *
from tkinter.messagebox import *
import wordcloud
import string
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import jieba
import nltk
import os
from collections import Counter # 次數統計

filename = ""

#新增文件
def New():
    global windows, filename, Mytext
    windows.title("未命名文件")
    filename = None
    Mytext.delete(1.0, END)
    
#打開檔案
def Open():
    global filename
    filename = askopenfilename(defaultextension=".txt") #記錄檔案名稱
    if filename == "":
        filename = None
    else:
        windows.title("記事本" + os.path.basename(filename)) #依照所選檔案進行更改
        Mytext.delete(1.0, END) #確保一開始為空
        f = open(filename, 'r',encoding="utf-8") #讀取所選檔案
        Mytext.insert(1.0, f.read()) #放到我的記事本中
        f.close() #關上所選的檔案

#找尋特定字元
def Find_event():
    data=Mytext.get("1.0","end-1c") #文本
    find_data=find_text.get("1.0","end-1c") #要找的字元
    if find_data not in data: #是否存在
        messagebox.showinfo('提示', '搜索的字元不存在')
    else:
        self_count.set(str(data.count(find_data)))

#替換
def Replace_event():
    find_data = find_text.get(1.0, "end-1c") #想找的
    data=Mytext.get("1.0","end-1c") #文本
    replace_data=replace_text.get("1.0","end-1c") #想換成的字元
    data = data.replace(find_data, replace_data) #將要找的字元替代成我想要的字元
    Mytext.delete(1.0,END) #原本的全部刪除
    Mytext.insert(INSERT,data) #改好的放進去
    
def Find():
    global Mytext,self_count,find_text,replace_text
    
    self_count=StringVar() #由於每次查詢個數不同，使用StringVar()
    self_count.set('0') #初始為0
    
    top1=Toplevel(Mytext) #使用第二個視窗給使用者操作
    
    top1.title('查詢和替換')
    top1.geometry("400x200")
    find_text = Text(top1, width=10, height=2)
    find_text.pack()
    Button(top1, text='查找', width=10, command=Find_event).pack()
    
    Label(top1, text='查找總数').pack()
    count_label = Label(top1, textvariable=self_count)
    count_label.pack()
    
    replace_text = Text(top1, width=10, height=2)
    replace_text.pack()
    Button(top1, text='替換成', width=10, command=Replace_event).pack(anchor='s')
    
def Save():
    global filename
    try:
        f = open(filename, 'w')
        msg = Mytext.get(1.0, 'end')
        f.write(msg)
        f.close()
    except:
        Saveas()
        
def Saveas():
    global filename
    f = asksaveasfilename(initialfile="未命名.txt", defaultextension=".txt")
    filename = f
    fh = open(f, 'w')
    msg = Mytext.get(1.0, END)
    fh.write(msg)
    fh.close()
    windows.title("記事本 " + os.path.basename(f))
    
def cut():
    global Mytext
    Mytext.event_generate("<<Cut>>")
    
def copy():
    global Mytext
    Mytext.event_generate("<<Copy>>")
    
def paste():
    global Mytext
    Mytext.event_generate("<<Paste>>")
    
def undo():
    global Mytext
    Mytext.event_generate("<<Undo>>")
    
def Ischinese(strs): #使用unicode判斷是否為中文
    for ch in strs:
        if  '\u4e00' <= ch <='\u9fa5':
            return True
    return False
            
def Cloud(): 
    global Mytext
    text=Mytext.get(1.0, END)
    mask = np.array(Image.open('ES.jpg')) #製造mask
    mask=(mask==0)*255 ## 等於0的地方變成255 原本有數字的地方變0，
    font_path='華康秀風體.TTF' #設定中文字體
    wc = wordcloud.WordCloud(background_color='white',margin=2, mask=mask,font_path=font_path
                             ,max_words=200, width=1080, height=720, relative_scaling=0.5 )
    
    if Ischinese(text):
        jieba.set_dictionary('dict.txt.big.txt') #設定分詞庫
        seg_list=jieba.lcut(text, cut_all=False)  # lcut直接返回list
        dictionary = Counter(seg_list) # 統計分詞出現次數
        stopword = [' ', '，', '（', '）', '...', '。', '「', '」','《','》'] # 移除停用詞
        [dictionary.pop(x, None) for x in stopword] #存字典裡刪除停用詞
        wc.generate_from_frequencies(dictionary)
        wc.to_file('mycloudCH.png') #最後存出的檔案名稱
    else:#英文不須太多處裡，可自動拆解文本
        text = ' '.join(nltk.word_tokenize(text))
        wc.generate(text)
        wc.to_file('mycloudEG.png') #最後存出的檔案名稱
    
def Calaulate():
    global Mytext
    count_en=count_nu=count_ch=count_sp=count_else=wordsum=0
    v1=StringVar()
    v1=Mytext.get("1.0","end-1c")
    for word in v1:
        if word in string.ascii_letters:
            count_en+=1
        elif word.isalpha():
            count_ch+=1
        elif word.isspace():
            count_sp+=1
        elif word.isdigit():
            count_nu+=1
        else:
            count_else+=1
    wordsum=count_en+count_ch+count_nu+count_else-count_sp
    top=Toplevel(Mytext)
    top.title('字數計算')
    top.geometry("400x200")
    
    label1=Label(top,text='有'+str(count_ch)+'個中文字元')
    label2=Label(top,text='有'+str(count_en)+'個英文字元')
    label3=Label(top,text='有'+str(count_nu)+'個數字字元')
    label4=Label(top,text='有'+str(count_else)+'個特殊符號')
    label5=Label(top,text='總共有'+str(wordsum)+'個字元')
    
    label1.pack(padx=50)
    label2.pack(padx=50)
    label3.pack(padx=50)
    label4.pack(padx=50)
    label5.pack(padx=50)

    
def redo():
    global Mytext
    Mytext.event_generate("<<Redo>>")
    Mytext.pack(expand=YES, fill=BOTH)    
    
def Selectall():
    global Mytext
    # Mytext.event_generate("<<Cut>>")
    Mytext.tag_add("sel", "1.0", "end")

def mypopup(event):
    # global editmenu
    editmenu.tk_popup(event.x_root, event.y_root)


# In[31]:


windows = Tk()
windows.title("我的記事本")
windows.geometry("600x400")


#輸入框的頂端裝飾
y_bar = Frame(windows, height=15, bg='Azure')
y_bar.pack(expand=NO, fill=X)
#輸入框的左側裝飾
x_bar = Label(windows,width=2,bg='MintCream')
x_bar.pack(side=LEFT, anchor='nw', fill=Y)
#將原本文字全部刪除
Mytext = Text(windows, undo=True)
#無限放大打字框
Mytext.configure(font=("Courier", 10, "italic"))
Mytext.pack(expand=YES, fill=BOTH)    

#創建菜單條
menubar = Menu(windows)

#<菜單條>-文件功能
filemenu = Menu(windows)
filemenu.add_command(label="新建", accelerator="Ctrl+N", command=New)
Mytext.bind("<Control-N>", New)
Mytext.bind("<Control-n>", New)

filemenu.add_command(label="打開", accelerator="Ctrl+O", command=Open)
Mytext.bind("<Control-O>", Open)
Mytext.bind("<Control-o>", Open)

filemenu.add_command(label="保存", accelerator="Ctrl+S", command=Save)
Mytext.bind("<Control-S>", Save)
Mytext.bind("<Control-s>", Save)

filemenu.add_command(label="另存為", accelerator="Ctrl+shift+s", command=Saveas)
menubar.add_cascade(label="文件", menu=filemenu)
 
#<菜單條>-編輯功能
editmenu = Menu(windows)
editmenu.add_command(label="撤銷", accelerator="Ctrl+Z", command=undo)
editmenu.add_command(label="重做", accelerator="Ctrl+Y", command=redo)

editmenu.add_separator()

editmenu.add_command(label="剪下", accelerator="Ctrl+X", command=cut)
editmenu.add_command(label="復制", accelerator="Ctrl+C", command=copy)
editmenu.add_command(label="貼上", accelerator="Ctrl+V", command=paste)

editmenu.add_separator()
editmenu.add_command(label="尋找與替換", accelerator="Ctrl+F", command=Find)
editmenu.add_command(label="全選", accelerator="Ctrl+A", command=Selectall)
Mytext.bind("<Control-A>", Selectall)
Mytext.bind("<Control-a>", Selectall)

menubar.add_cascade(label="編輯", menu=editmenu)

#<菜單條>-檢視功能
viewmenu = Menu(windows)
viewmenu.add_command(label="字數", command=Calaulate)
viewmenu.add_command(label="文字雲", command=Cloud)

menubar.add_cascade(label="檢視", menu=viewmenu)


windows['menu'] = menubar
 
scroll = Scrollbar(Mytext)
Mytext.config(yscrollcommand=scroll.set)
scroll.config(command=Mytext.yview)
scroll.pack(side=RIGHT, fill=Y)

windows.mainloop()


# In[15]:





# In[ ]:




