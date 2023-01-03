import csv
import os
def CREATE():
    f=open("collegeatt.csv",'a')
    size=os.path.getsize("collegeatt.csv")
    f.seek(size)
    
    wobj=csv.writer(f)
    
    #n=int(input("Enter no. of colleges:"))
    while True:      #for i in range(n):
        a=eval(input("total list values"))
        for i in a:
            l=[]
            name=a[0]
            stream=a[1]
            country=a[2]
            size=a[3]
            hostel=a[4]
            classmates=a[5]
            fee=a[6]
        """name=input("Enter college name:")
        stream=(eval(input("Enter stream:-!!this is EVAL-put in LIST!!")))
        country=input("Enter country:")
        size=input("Enter size:")
        hostel=(eval(input("Enter hostel facilities:-!!this is EVAL-put in LIST!!")))
        classmates=input("Enter choice of classmates:")
        fee=(eval(input("Enter fee options:-!!this is EVAL-put in LIST!!")))"""
        n=name.split()
        if n[0].lower()!='the':
            comname=n[0].lower()
        else:
            comname=n[1].lower()
            
        img=[comname+'_logo.jpg',comname+'1.jpg',comname+'2.jpg',comname+'3.jpg']
        tfile=comname+'.txt'
        
        l=[name,stream,country,size,hostel,classmates,fee,img,tfile]
        a.append(l)
        wobj.writerow(l)
        ch=input("any more?")
        if ch.lower()=='n':
            break
            
    f.close()

def DISPLAY():
    f=open("collegeatt.csv",'r')
    robj=csv.reader(f)
    #print("Name\tAge\tClass\tSection\tSchool")
    for l in robj:
        if any(l):
            print(l[0],'\t',l[1],'\t',l[2],'\t',l[3],'\t',l[4],l[5],'\t',l[6])
    f.close()

CREATE()
DISPLAY()









































'''import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        self.hi_there["command"] = self.say_hi
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                              command=self.master.destroy)
        self.quit.pack(side="bottom")

    def say_hi(self):
        print("hi there, everyone!")

root = tk.Tk()
app = Application(master=root)
app.mainloop()'''
