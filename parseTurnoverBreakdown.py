import time
from readFromWeb import handleData

from array import array
from stripogram import html2text
import datetime
import math
import os
import shutil
import time
import urllib
import xlwt

def bullsPlayerInvolved(rosterlist, str):
    for player in rosterlist:
        validate= player+" turnover"
        validate1=player+"\nturnover"
        dontInclude="steal:"+player
        if dontInclude in str:
            continue
        if validate in str or validate1 in str:
            return rosterlist.index(player)

datagrabber=handleData("http://www.nba.com/games/20121031/SACCHI/gameinfo.html")

url=raw_input("Enter the URL for the current game.  Make sure play by play is updated:")

filehandle = urllib.urlopen(url)
text = html2text(filehandle.read())

cleanedText=text.split('\xa0')
filehandle.close()
plays=cleanedText
plays=[element.lower() for element in plays]
plays=[element.replace("\n"," ") for element in plays]

print plays
roster =["belinelli","boozer","butler","deng","gibson","hamilton","hinrich","mohammed","noah","radmanovic","robinson","rose","teague"]

print len(roster)
turnovers=[[0 for x in xrange(9)] for x in xrange(len(roster))]


categories=["Name","Bad Pass","Lost Ball", "Offensive Foul","Traveling","Three Seconds","Out of Bounds","Other","Stolen","Total Turnovers"]

for play in plays:
    playerIndex=bullsPlayerInvolved(roster,play)
    if playerIndex == None:
        continue
    if "bad pass" in play or "bad\npass" in play:
        turnovers[playerIndex][0]+=1
    elif "out of bounds lost ball" in play or "step out of bounds" in play:
        turnovers[playerIndex][5]+=1
    elif "lost ball" in play or "lost\nball" in play:
        turnovers[playerIndex][1]+=1
    elif "foul" in play:
        turnovers[playerIndex][2]+=1
    elif "traveling" in play or "double dribble" in play:
        turnovers[playerIndex][3]+=1
    elif "offensive goaltending" in play or "backcourt" in play:
        turnovers[playerIndex][6]+=1
    elif "3 second violation" in play:
        turnovers[playerIndex][4]+=1


for t in turnovers:
    t[7]=t[0]+t[1]
    t[8]=t[0]+t[1]+t[2]+t[3]+t[4]+t[5]+t[6]


wbk = xlwt.Workbook()
sheet = wbk.add_sheet('sheet 1',cell_overwrite_ok=True)
sheet1 = wbk.add_sheet('SeasonTotal',cell_overwrite_ok=True)
sheet.write(0,0,categories[0])
sheet.write(0,1,categories[9])

for i in range(1,len(categories)-1):
    sheet.write(0,i+1,categories[i])
j=1
for r in roster:
    index=roster.index(r)+1
    sheet.write(j, 0,r)
    for x in range(1,len(categories)-1):
        if turnovers[index-1][x-1]!=0:
            sheet.write(j,x+1,turnovers[index-1][x-1])
    if turnovers[index-1][8]!=0:
        sheet.write(j,1,turnovers[index-1][8])
    j+=2
    print r +"   "+str(turnovers[roster.index(r)][0])+"   "+str(turnovers[roster.index(r)][1])+"   "+str(turnovers[roster.index(r)][2])+"   "+str(turnovers[roster.index(r)][3])+"   "+str(turnovers[roster.index(r)][4])+"   "+str(turnovers[roster.index(r)][5])+"   "+str(turnovers[roster.index(r)][6])+"   "+str(turnovers[roster.index(r)][7])+"   "+str(turnovers[roster.index(r)][8])

""" Now add in Season totals, for this portion I have a running csv
    file that contains the season totals for each player on the bulls
    which is called SeasonTotal1.csv"""

import csv

reader = csv.reader(open('SeasonTotal1.csv', "rU"), delimiter = ",")
SeasonTotalTurnovers=[];
for row in reader:
    SeasonTotalTurnovers.append(row)

for i in range(1,len(roster)+1):
    sheet.write(2*i,0,'Season Total')

def findPlayerIndex(playerName, SeasonTotalTurnovers):
    for row in SeasonTotalTurnovers:
        if row[0]==playerName:
            return row

for i in range (0,len(roster)):
    SeasonTotal=findPlayerIndex(roster[i], SeasonTotalTurnovers)
    sheet1.write(i,0,roster[i])
    for j in range(2,len(SeasonTotal)):
        sheet1.write(i,j,int(SeasonTotal[j])+turnovers[i][j-2])
        if int(SeasonTotal[j])+turnovers[i][j-2]!=0:
            sheet.write(2*(i+1),j,int(SeasonTotal[j])+turnovers[i][j-2])
    sheet1.write(i,1,int(SeasonTotal[1])+turnovers[i][8])
    if int(SeasonTotal[1])+turnovers[i][8]!=0:
        sheet.write(2*(i+1),1,int(SeasonTotal[1])+turnovers[i][8])


wbk.save('Bulls.xls')
gameOver=False
for play in plays:
    if "end of 4th" in play:
        print "SUCCESS Entire Play by Play Parsed"
        gameOver=True
if gameOver ==False:
    print "FAILURE Play by play missing data, wait for play by play to update and try again"

