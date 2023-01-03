def CREATE():
    f=open("georgia.txt","w")
    f1=input("first half")
    f1+='\n'
    f.write(f1)
    f2=input("second half")
    f2+='\n'
    f.write(f2)
    f.close()
def DISPLAY():
    f=open("georgia.txt","r")
    s=" "
    while s:
        s=f.readline()
        s=s.strip()
        print(s)
    f.close()
        
    

DISPLAY()
        
