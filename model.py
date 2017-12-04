import numpy as np
import matplotlib.pyplot as plt
import csv
import math, ast
import pickle

#poisson function
def poisson(actual, mean):
    return math.pow(mean, actual) * math.exp(-mean) / math.factorial(actual)

#Prem teams
teamList = sorted(["Arsenal","Burnley","Bournemouth","Chelsea","Everton","Brighton","Liverpool","Man United","Man City","Crystal Palace","Huddersfield","West Ham","West Brom","Southampton","Leicester","Watford","Tottenham","Stoke","Newcastle","Swansea",])


#### data formatting shit, i trim down data from the csv to only get the home away team and the goals
data = []
with open('E0.csv', 'rt') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            data.append(row)

matchdata = []
for i in data:
    matchdata.append(i[2:6])


#10 games in
#create team dictionary with goals scored / conceded
teamStats = {}
for team in teamList:
    gamesPlayed = 0
    homeGoalsScored = 0
    awayGoalsScored = 0
    homeGoalsConceded = 0
    awayGoalsConceded = 0
    for i in matchdata:
        if (i[0] == team) :
            homeGoalsScored = int(i[2]) + homeGoalsScored
            homeGoalsConceded = int(i[3]) + homeGoalsConceded
            gamesPlayed = gamesPlayed + 1
        if (i[1] == team):
            awayGoalsConceded = int(i[2]) + awayGoalsConceded
            awayGoalsScored = int(i[3]) + awayGoalsScored
            gamesPlayed = gamesPlayed + 1
    goalstats = [homeGoalsScored,homeGoalsConceded,awayGoalsScored,awayGoalsConceded]
    teamStats.update({team : goalstats})



##AVERAGE OVER 10 GAMES
teamAverages = {}
for team in teamList:
    teamAverages.update({team : [teamStats[team][0]/10,teamStats[team][1]/10,teamStats[team][2]/10,teamStats[team][3]/10]})

#find the league average
leagueAverages = [0,0,0,0]
for team in teamList:
    for i in range(0,4):
        leagueAverages[i] = leagueAverages[i] + teamAverages[team][i]
for i in range(0,4):
    leagueAverages[i] = leagueAverages[i]/10

#standardised home/away attack/defence scores of each team in the league
teamScores = {}
for team in teamList:
    teamArray = [0,0,0,0]
    for i in range(0,4):
        teamArray[i] = teamAverages[team][i] / leagueAverages[i]
    teamScores.update({team : teamArray})

#function to return probabilities of score lines in a matrix size maxScores and an array of other odds
def matchOdds(team1,team2,maxScores,showOdds):
    homeExp = teamScores[team1][0] * teamScores[team2][3] * teamAverages[team1][0]
    awayExp = teamScores[team2][2] * teamScores[team1][1] * teamAverages[team2][2]
    homeWin = 0
    awayWin = 0
    draw = 0
    over25 = 0
    under25 = 0
    bttsYes = 0
    bttsNo = 0


    resultMatrix = np.zeros((maxScores,maxScores))
    for i in range(0,maxScores):
        for j in range(0,maxScores):
            resultMatrix[i][j] = poisson(i,homeExp) * poisson(j, awayExp) * 100
            if showOdds:
                print(i,'-',j)
                print(resultMatrix[i][j])
            if i > j:
                homeWin = homeWin + resultMatrix[i][j]
            if i < j:
                awayWin = awayWin + resultMatrix[i][j]
            if i == j:
                draw = draw + resultMatrix[i][j]
            if (i+j) > 2.5:
                over25 = over25 + resultMatrix[i][j]
            if (i>0) & (j>0):
                bttsYes = bttsYes + resultMatrix[i][j]

    under25 = 100 - over25
    bttsNo = 100 - bttsYes
    if showOdds:
        print("Home Win:    ",homeWin," Draw:   ",draw," Away Win:   ",awayWin)
        print("Over 2.5:    ",over25," Under 2.5:   ",under25)
        print("Btts Yes:    ",bttsYes," Btts No:    ",bttsNo )

    oddsArray = [homeWin,draw,awayWin,over25,under25,bttsYes,bttsNo]

    return (resultMatrix,oddsArray)


#Print decimal odds
def decimalOdds(team1,team2,maxScores):
    odds = matchOdds(team1,team2,maxScores,False)
    oddsArray = odds[1]
    print("Home Win:    ",100/oddsArray[0]," Draw:   ",100/oddsArray[1]," Away Win:   ",100/oddsArray[2])
    print("Over 2.5:    ",100/oddsArray[3]," Under 2.5:   ",100/oddsArray[4])
    print("Btts Yes:    ",100/oddsArray[5]," Btts No:    ",100/oddsArray[6] )
    return




matchOdds("Man City", "Arsenal",7,True)
