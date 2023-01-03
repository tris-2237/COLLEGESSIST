import csv

def create():
    f=open("login_data.csv","a")
    wobj=csv.writer(f,delimiter=",")
    b=[]
    while True:
        u=input("enter user name")
        e=input("enter email")
        c=input("enter class")
        p=input("password")
        a=[u,e,c,p]
        wobj.writerow(a)
        ch=input("any more?")
        if ch!="y":
            break
   
    f.close()

def display():
    f=open("test.txt","r")
    s=" "
    while s:
        s=f.readline()
        s=s.strip()
        print(s)
display()
        
