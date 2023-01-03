def CREATE():
    f=open("updates.txt","a")
    a=input("enter the line to be added")
    a+='\n'
    f.write(a)
    f.close()
def SHOW():
    f=open("updates.txt","r")
    s=" "
    while s:
        s=f.readline()
        s=s.strip()
        print(s)
    f.close()

SHOW()
