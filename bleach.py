from pathlib import Path
from heapq import nlargest
import texttable
from ascii_graph import Pyasciigraph
from ascii_graph.colors import *
from ascii_graph.colordata import vcolor
from heapq import nsmallest
import tempfile
import os
import click_spinner
from datetime import datetime
import shutil


def makeGraph(fList):
    docs=0
    vids=0
    songs=0
    images=0
    others=0
    compressed=0
    codess=0
    ll=len(fList)
    if(oss==1):
        print("Total no of files in system: ",ll)
    else:
        print("Total no of files in user home: ",ll)
    for file in fList:
        if file.name.lower().endswith('.pdf') or file.name.lower().endswith('.docx') or file.name.lower().endswith('.doc') or file.name.lower().endswith('.txt'):
            docs+=1
        
        if file.name.lower().endswith('.mp4') or file.name.endswith('.mkv') or file.name.endswith('.avi'):
            vids+=1
                
        if file.name.lower().endswith('.jpeg') or file.name.endswith('.png') or file.name.endswith('.jpg') or file.name.endswith('.gif'):
            images+=1
            
        if file.name.lower().endswith('.mp3') or file.name.endswith('.ogg') or file.name.endswith('.wav'):
            songs+=1
        
        if file.name.endswith('.apk') or file.name.endswith('.jar') or file.name.endswith('.exe') or file.name.endswith('.iso') or file.name.endswith('.dmg') or file.name.endswith('.csv') or file.name.endswith('.log') or file.name.endswith('.db') :
            others+=1
            
        if file.name.lower().endswith('.zip') or file.name.endswith('.7z') or file.name.endswith('.deb') or file.name.endswith('.tar.gz') or file.name.endswith('.rpm'):
            compressed+=1
          
        if file.name.endswith('.c') or file.name.endswith('.py') or file.name.endswith('.java') or file.name.endswith('.cpp'):
            codess+=1
            
    data = [('docs', docs), ('songs', songs), ('videos', vids),
        ('images', images), ('codes',codess),("compressed",compressed),('others', others)]
    
    pattern = [Gre, Yel, Red]
    data = vcolor(data, pattern) 
    graph = Pyasciigraph()
    for line in graph.graph('Files on PC', data):
        print(line)
        
        

def readbles(num, suffix='B'):
    for unit in ['', 'k', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1000.0:
            return "%3.1f %s%s" % (num, unit, suffix)
        num /= 1000.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def LargestN(fList,fLen):
    nfiles = nlargest(10,fList,lambda x : x.stat().st_size )
    count=1
    table = texttable.Texttable()
    
    tab=[]
    print(fLen,"files scanned!!!")
    tab.append(["No.","Name","Location","Size"])
    for i in nfiles:
        tab.append([count,i.name,i.parents[0],readbles(i.stat().st_size)])
        count+=1
    table.add_rows(tab)
    print(table.draw())


def DelTemp():
    #print(tempfile.gettempdir())
    p=Path(tempfile.gettempdir())
    files = p.glob('**/*.*')
    size=0
    for file in files:
        try:
            #print(file)
            size+=file.stat().st_size
            #print(file)
            os.remove(file)
        except Exception as e:
            size-=file.stat().st_size
            #print(e)
    
    sizee=readbles(size)
    print("Hurray!",sizee, "Space freed.")


def PrintFree(path):
    #print(path)
    st = os.statvfs(path)
    if st.f_frsize:
        s=st.f_frsize * st.f_bavail
        ss=readbles(s)
        print("You have free memory: ",end='' )
        print(ss)
    else:
        s=st.f_bsize * st.f_bavail
        ss=readbles(s)
        print("You have free memory: ",end='' )
        print(ss)


def OldestN(fList,fLen):
    nfiles = nsmallest(10,fList,lambda x : x.stat().st_mtime )
    #nfiles = nfiles.reverse()
    count=1
    table = texttable.Texttable()
    
    tab=[]
    tab.append(["No.","Name","Last Modified","Size","Location"])
    
    print(fLen,"files scanned!!!")
    for i in nfiles:
        tab.append([count,i.name,datetime.fromtimestamp(i.stat().st_mtime),readbles(i.stat().st_size),i.parents[0]])
        count+=1
    
    #tab= tab[::-1]
    
    table.add_rows(tab)
    print(table.draw())    
    
    print("Do you want to delete some of these files?")
    print("1.Yes\t 2.Naah")
    inp=int(input())
    if(inp==1):
            print("Input the file numbers separated by space")
            arr = [int(x) for x in input().split()]
            print(arr)
            for i in arr:
                try:
                    os.remove(nfiles[i-1])
                    print("File deleted - ",end='')
                    print(nfiles[i-1].name)
                except Exception as e:
                    pass
    else:
        raise SystemExit


def fListHere(p):
    with click_spinner.spinner():
        files = p.glob('**/*.*')
        fList = list(files)
    return fList    

def deClutter(p,r):
    files = p.glob('**/*.*')
    
    for file in files:
        if file.name.lower().endswith('.pdf') or file.name.lower().endswith('.docx') or file.name.lower().endswith('.doc') or file.name.lower().endswith('.txt'):
            Path(r/ 'Docs').mkdir(parents=True,exist_ok=True) 
            shutil.move(str(file),r/ 'Docs')
        
        if file.name.lower().endswith('.mp4') or file.name.endswith('.mkv') or file.name.endswith('.avi'):
            Path(r/ 'Videos').mkdir(parents=True,exist_ok=True) 
            shutil.move(str(file),r/ 'Videos')
                
        if file.name.lower().endswith('.jpeg') or file.name.endswith('.png') or file.name.endswith('.jpg') or file.name.endswith('.gif'):
            Path(r/ 'Images').mkdir(parents=True,exist_ok=True) 
            shutil.move(str(file),r/ 'Images')
    
        if file.name.lower().endswith('.mp3') or file.name.endswith('.ogg') or file.name.endswith('.wav'):
            Path(r/ 'Music').mkdir(parents=True,exist_ok=True) 
            shutil.move(str(file),r/ 'Music')
            
        if file.name.lower().endswith('.zip') or file.name.endswith('.7z') or file.name.endswith('.deb') or file.name.endswith('.tar.gz') or file.name.endswith('.rpm'):
            Path(r/ 'Compressed').mkdir(parents=True,exist_ok=True) 
            shutil.move(str(file),r/ 'Compressed')    
        
        if file.name.endswith('.apk') or file.name.endswith('.jar') or file.name.endswith('.iso') or file.name.endswith('.dmg') or file.name.endswith('.csv') or file.name.endswith('.log') or file.name.endswith('.db') :
            Path(r/ 'Others').mkdir(parents=True,exist_ok=True) 
            shutil.move(str(file),r/ 'Others')     
            
        if file.name.endswith('.c') or file.name.endswith('.py') or file.name.endswith('.java') or file.name.endswith('.cpp'):
            try:
                Path(r/ 'Codes').mkdir(parents=True,exist_ok=True) 
                shutil.move(str(file),r/ 'Codes')
            except:
                pass
    print("Desktop cleaned, Didn't touched the icons!\nCheck your Counter Strike icon, just to be sure!:D")
    

#####main
#intro    
print("Which OS you are using?")
print("1.Linux\t 2.Windows")
oss = int(input())
print('What do you wanna do?')
print('1. Show file system statistics')
print('2. Show me the top 10 memory hog files')
print('3. Declutter my desktop')
print('4. Save my space')

print('Enter ur choice')
selected = int(input())
   


#code 
#Show stats
if selected==1:
    if oss==1:
        q=Path.home()
        p=q/'Downloads'
        PrintFree("/")
    else:
        q=Path.home()
        p=q/'Downloads'
    fList  = fListHere(p)
    fLen = len(fList)    
    makeGraph(fList)    
    

#Show top 10 memory hog files
if selected==2:
    if oss==1:
        q=Path.home()
        p=q/'Downloads'
    else:
        q=Path.home()
        p=q/'Downloads'
    #p=Path('/home/anurag/Downloads')
    fList  = fListHere(p)
    fLen = len(fList)
    LargestN(fList,fLen)


#Declutter desktop
if selected==3:
    if oss==1:
        q=Path.home()
        p=q / 'Desktop'
        r=q / 'Documents'
    else:
        q=Path.home()
        p=q / 'Desktop'
        r=q / 'Documents'
    deClutter(p,r)

#free up some space
if selected==4:
    #PrintFree("/")
    DelTemp()
    print("Greedy, eh!! Need more space!")
    print("1.Hell yeah\t2.Nope")
    gr=int(input())
    if gr==1:
        print("Showing the least recently used files")
        if oss==1:
            q=Path.home()
            p=q/'Downloads'
        else:
            q=Path.home()
            p=q/'Downloads'
        ##p=Path('/home/anurag/Downloads')
        fList  = fListHere(p)
        fLen = len(fList)
        OldestN(fList,fLen)




