from tkinter import *
from tkinter import ttk
import sys
import os

print "\t\033[92m*************************************************"
print "\t\033[92m*    Web Application Vulnerability Scanner      *"
print "\t\033[92m*************************************************"

def prc1(event):
    URL = url.get()
    os.system("python rdrct.py"+" "+URL+" payload.txt")
def prc2(event):
    URL = Url.get()
    os.system("python scan.py -t"+" "+URL)
def prc3(event):
    URL = url2.get()
    os.system("python DirScanner.py"+" "+URL)
def prc4(event):
    URL = url4.get()
    os.system("python SQLIScanner.py"+" "+URL)
def prc5(event):
    os.system("nmap")
def prc6(event):
    URL = url4.get()
    os.system("burpsuite")

root = Tk()

root.title("ABlack V 1.0")
 
Label(root, text="URL").grid(row=0, column=0, sticky=W)
url = Entry(root,width=50)
url.grid(row=0, column=1)
b1 = Button(root, text="openredirect")
b1.grid(row=0, column=9)

Label(root, text="URL").grid(row=1, column=0, sticky=W)
Url = Entry(root, width=50)
Url.grid(row=1, column=1)
b = Button(root, text="XSS")
b.grid(row=1,column=9)

Label(root, text="URL").grid(row=2, column=0, sticky=W)
url2 = Entry(root,width=50)
url2.grid(row=2, column=1)
b3 = Button(root, text="Dirbuster")
b3.grid(row=2,column=9)

Label(root, text="URL").grid(row=3, column=0, sticky=W)
url4 = Entry(root,width=50)
url4.grid(row=3, column=1)
b4 = Button(root, text="sqli")
b4.grid(row=3,column=9)

b5 = Button(root, text="Nmap")
b5.grid(row=4, column=4)
b6 = Button(root, text="Burp")
b6.grid(row=4, column=5)


b1.bind("<Button-1>",prc1)
b.bind("<Button-1>",prc2)
b3.bind("<Button-1>",prc3)
b4.bind("<Button-1>",prc4)
b5.bind("<Button-1>",prc5)
b6.bind("<Button-1>",prc6)



root.mainloop()
