from __future__ import division
#remove edge cases, try catch everything
#order clusters in decreasing quantity
#change color when clicked
#run on ubuntu

import sys
from os import getcwd
sys.path.append(getcwd() + '/API')
from Main import *

import webbrowser

if sys.version_info[0] < 3:
    from Tkinter import *
    import ttk as ttk
else:
    from tkinter import *
    import tkinter.tkk as ttk

PostObj = PostProcessingAPI()
clusters = {}
searchstring = ''
stacksearchstring = []
furtherCluster = 0	
searchResults = {}
    
"""
This is the script for running the GUI, and gets results from 
ClusterWeb() function in API/Main.py
"""
__author__ =  'Rohan Agrawal'

def DisplayResults(*args):
    """
    Displays results in the resultlbl text box.
    """
    global searchstring
    global stacksearchstring
    global clusters
    global furtherCluster
    global searchResults
    searchstring = query.get()
    if furtherCluster == 0:
        stacksearchstring = []
    stacksearchstring.append(searchstring)
    resultcounter = 1
    if searchstring not in clusters and searchstring not in searchResults:
        clusters, searchResults = ClusterWeb(searchstring, clusters, searchResults ) 
        
    resultslbl['state'] = "normal"
    resultslbl.delete("1.0" , END)	
    if searchstring in clusters:
        for i in clusters[searchstring]:
            resultslbl.insert(END, "-----------------------------Cluster ")
            resultslbl.insert(END, int(i) + 1)
            resultslbl.insert(END, "-----------------------------\n\n")
            for j in clusters[searchstring][i][1]:
                resultslbl.insert(END, str(resultcounter)+". ")
                resultcounter += 1
                resultslbl.insert(END, searchResults[searchstring][j][1].encode('utf-8'))
                resultslbl.insert(END, "\n")
                resultslbl.insert(END, searchResults[searchstring][j][0], "hlink")  
                resultslbl.insert(END, "\nSnippet: ")
                resultslbl.insert(END, searchResults[searchstring][j][2].encode('utf-8'))
                resultslbl.insert(END, "\n\n\n")
            
        resultslbl['state'] = "disabled" 
        counter = 0
        for i in range(0,30):
            clusterlbl[i]['state'] = 'normal'
            clusterlbl[i].delete("1.0", END)
            
        for i in clusters[searchstring]:
            print "Cluster",i + 1
            for j in clusters[searchstring][i][0]:     
                clusterlbl[counter].insert(END, j.encode('utf-8'))
                print j.encode('utf-8')
                
                counter += 1
            print 
        for i in range(0,30):
            clusterlbl[i]['state'] = 'disabled'            
    else:
        resultslbl.insert(END, "No History")
        resultslbl['state'] = "disabled" 
        for i in range(0,30):
            clusterlbl[i]['state'] = 'normal'
            clusterlbl[i].delete("1.0", END)
            clusterlbl[i]['state'] = 'disabled'  
        
        
def back(*args):
    """
    Functionality for the back button provided in the GUI
    If going back is not possible, returns No History
    in the search box
    """
    global furtherCluster
    global stacksearchstring
    if stacksearchstring == []:
        query.set('No History')
    else:    
        stacksearchstring.pop()
        if stacksearchstring == []:
            query.set('No History')
        else:
            query.set(stacksearchstring.pop())
            furtherCluster = 1
            DisplayResults()
            furtherCluster = 0
        
def openLink(event): 
    """
    Module for opening search links on user click
    """
    start, end = resultslbl.tag_prevrange("hlink", 
    resultslbl.index("@%s,%s" % (event.x, event.y))) 
    webbrowser.open(resultslbl.get(start, end) )
    
def clickCluster(event, arg):
    """
    When a user clicks on a cluster label, this function
    takes the text of that label, and runs the cluster search
    algorithm on the new label + search string provided by 
    the user
    """
    global furtherCluster
    label = clusterlbl[arg].get(1.0, END).strip()
    if label != '':
        furtherCluster = 1
        query.set(PostObj.getNewSearchString(searchstring, label))
        DisplayResults()
        furtherCluster = 0
        
def clickClusterLabel(event, arg):
    """
    When a user clicks on a particular cluster number,
    this function displays the search results pertaining 
    to that specific cluster.
    """
    global searchstring
    global searchResults
    label = int(arg)
    resultcounter = 1
    if label in clusters[searchstring]:
        resultslbl['state'] = "normal"
        resultslbl.delete("1.0" , END)	
        for j in clusters[searchstring][label][1]:
            resultslbl.insert(END, str(resultcounter) + ". ")
            resultslbl.insert(END, searchResults[searchstring][j][1].encode('utf-8'))
            resultcounter += 1
            resultslbl.insert(END, "\n")
            resultslbl.insert(END, searchResults[searchstring][j][0], "hlink")  
            resultslbl.insert(END, "\nSnippet: ")
            resultslbl.insert(END, searchResults[searchstring][j][2].encode('utf-8'))
            resultslbl.insert(END, "\n\n\n")
        resultslbl['state'] = "disabled"
    
if __name__ == '__main__':
    """
    Drawing the GUI objects in main
    """
    root = Tk()
    root.state("iconic")
    query = StringVar()
       
    content = ttk.Frame(root)
    frame = ttk.Frame(content, borderwidth=5, relief="sunken", width='30c', height='18c')
    resultslbl = Text(content, relief = "solid")
    resultslbl.tag_configure("hlink", foreground='blue', underline=1) 
    resultslbl.tag_bind("hlink", "<Button-1>", openLink) 
    resultslbl['state'] = "disabled" 
    Instructionlbl = ttk.Label(content, text = 'Click on "Cluster 1" to see only \nCluster 1 specific results. Click\non a specific label to expand\nyour clustering results to that\nspecific cluster, i.e you want\nto cluster that label further, or\njust want more results related\nto that cluster.', background = "lightblue")
    
    querytxt = ttk.Entry(content, textvariable=query)
    searchbtn = ttk.Button(content, text="Cluster Search", command=DisplayResults)
    backbtn = ttk.Button(content, text="Back", command=back)

    box = []
    for i in range (1,11):
        box.append(Text(content, height = 1, width = 5, bg = "gray"))
        box[i-1].grid(column=0, row= 3 + (i-1)*3, ipadx = 21)
        box[i-1].insert(INSERT,"cluster "+str(i))
        box[i-1].bind("<Button-1>", lambda event, arg=i-1: clickClusterLabel(event, arg))
        box[i-1]['state'] = 'disabled'
    
        
    clusterlbl = []
    for i in range (3,33):
        clusterlbl.append(Text(content, height = 1, width = 25, bg = "gray"))
        clusterlbl[i-3].grid(column=1, row= i)
        clusterlbl[i-3].bind("<Button-1>", lambda event, arg=i-3: clickCluster(event, arg))
        clusterlbl[i-3]['state'] = 'disabled'

    content.grid(column=0, row=0)
    frame.grid(column=0, row=0, columnspan=21, rowspan=31)
    resultslbl.grid(column=5, row=0, columnspan=16,rowspan = 31,  sticky = "news")
    Instructionlbl.grid(column = 22, row = 1 , rowspan = 10)

    
    
    s = ttk.Scrollbar(content, orient=VERTICAL, command=resultslbl.yview)
    s.grid(column=21, row=0, rowspan = 31,sticky=(N,S))
    resultslbl['yscrollcommand'] = s.set
    querytxt.grid(column=1, row=0, columnspan=3, ipadx = 70)
    searchbtn.grid(column=1, row=1, columnspan=3, ipadx = 70)
    backbtn.grid(column=1, row=2, columnspan=3, ipadx = 75)
    
    root.bind('<Return>', (lambda e, b=searchbtn: searchbtn.invoke()))
    querytxt.focus_set()
    root.mainloop()



