import random


def InitiateMessage(numOfDraws,players):
    return f"Number of numOfDraws {numOfDraws} for players {players}"

def __str__(numOfDraws,players):
    return f"Number of numOfDraws {numOfDraws} for players {players}"

def luckyDraw(luckyWhiteBalls):
      luckyWhiteBalls=[]
      for i in range(5):
         luckyWhiteBalls.append(random.randint(1,69))
         if i == 1:
            luckyPowerBalls = random.randint(1,26)
      print(f"winning white numbers = {luckyWhiteBalls}  and powerBall number = {luckyPowerBalls}")
      return luckyWhiteBalls,luckyPowerBalls


def getPlayerWinningPossibilites(luckyWhiteBalls,luckyPowerBalls):
      whiteBallWinningPossibility=0
      powerBallWinningPossibility=0
      for i in range(5):
         whiteBall=random.randint(1,69)
         if whiteBall in luckyWhiteBalls:
             whiteBallWinningPossibility=whiteBallWinningPossibility+1
         #checking powerBall winning possibility
         if i == 1:
           powerBall = random.randint(1,26)
           if powerBall == luckyPowerBalls:
               powerBallWinningPossibility=powerBallWinningPossibility+1

      return whiteBallWinningPossibility,powerBallWinningPossibility


def getPrizeAmount(whiteBallmatch,powerBallmatch,JackPotRiseAmount):
      prizeAmount=0
      isJackPot=0
      if powerBallmatch==1:
          if whiteBallmatch==0:
              prizeAmount =4
          elif whiteBallmatch==1:
              prizeAmount = 4
          elif whiteBallmatch==2:
              prizeAmount = 7
          elif whiteBallmatch==3:
              prizeAmount = 100
          elif whiteBallmatch==4:
              prizeAmount = 50000
          elif whiteBallmatch==5:
              prizeAmount = 20000000+JackPotRiseAmount
              isJackPot = 1
          else :
              prizeAmount = 0
      else :
          if whiteBallmatch==3:
              prizeAmount = 7
          elif whiteBallmatch==4:
              prizeAmount = 100
          elif whiteBallmatch==5:
              prizeAmount = 1000000
          else :
              prizeAmount = 0
      return prizeAmount,isJackPot

def getAverageEarnings(playersProfitDetailListOfList,numOfDraws):
      TotalByPlayerlist = list()
      AverageByPlayerlist = list()
      for j in range(0,len(playersProfitDetailListOfList[0])):
          tmp = 0
          for i in range(0, len(playersProfitDetailListOfList)):
              tmp = tmp + playersProfitDetailListOfList[i][j]
          TotalByPlayerlist.append(("p"+str(j+1),tmp))
          AverageByPlayerlist.append(("p"+str(j+1),tmp/numOfDraws))


      TotalByPlayerlist.sort(key=lambda TotalByPlayerlist: TotalByPlayerlist[1], reverse=True)
      AverageByPlayerlist.sort(key=lambda AverageByPlayerlist: AverageByPlayerlist[1],reverse=True)
      print("luckiest players {}".format(TotalByPlayerlist))
      print("luckiest players average {}".format(AverageByPlayerlist))

      TotalByPlayerlist.sort(key=lambda TotalByPlayerlist: TotalByPlayerlist[1])
      AverageByPlayerlist.sort(key=lambda AverageByPlayerlist: AverageByPlayerlist[1])
      print("unluckiest players {}".format(TotalByPlayerlist))
      print("unluckiest player averages {}".format(AverageByPlayerlist))

def getUserJackPotDetails(playersJackPotListToList,numOfDraws):
      TotalByPlayerJackPotCountlist = list()
      for j in range(0,len(playersJackPotListToList[0])):
          tmp = 0
          for i in range(0, len(playersJackPotListToList)):
              tmp = tmp + playersJackPotListToList[i][j]
          if tmp>0:
             TotalByPlayerJackPotCountlist.append(("p"+str(j+1),tmp))

      TotalByPlayerJackPotCountlist.sort(key=lambda TotalByPlayerJackPotCountlist: TotalByPlayerJackPotCountlist[1], reverse=True)
      if len(TotalByPlayerJackPotCountlist)>0:
          print("Jackpots by player {}".format(TotalByPlayerJackPotCountlist))
      else:
          print("No one got jackpot for all {} draws".format(numOfDraws))

def getDrawForAllPlayers(numOfDraws,numOfplayers):
      print(InitiateMessage(numOfDraws,numOfplayers))
      playersProfitDetailListOfList=[]
      playersJackPotListToList=[]
      JackPotRiseAmount=0
      luckyWhiteBalls = []
      for j in range(numOfDraws):
          print("taking draw in round :{}".format(j+1))
          
          luckyWhiteBalls,luckyPowerBalls = luckyDraw(luckyWhiteBalls)
          
          playersProfitDetailList = []
          playersJackPotList = []
          for i in range(numOfplayers):
              whiteBallWinningPossibility, powerBallWinningPossibility = getPlayerWinningPossibilites(luckyWhiteBalls, luckyPowerBalls)
              
              prizeAmount,isJackPot = getPrizeAmount(whiteBallWinningPossibility, powerBallWinningPossibility,JackPotRiseAmount)
              
              print((whiteBallWinningPossibility,powerBallWinningPossibility,prizeAmount,isJackPot))
              #print("amount spent is {} won is {}".format(2,prizeAmount))
              playersProfitDetailList.append(prizeAmount-2)
              playersJackPotList.append(isJackPot)
          playersProfitDetailListOfList.append(playersProfitDetailList)
          playersJackPotListToList.append(playersJackPotList)
          if isJackPot==0:
             JackPotRiseAmount=JackPotRiseAmount+numOfplayers
          else:
              isJackPot=0
              JackPotRiseAmount=0

      #print("spentAmount {}".format(playersProfitDetailListOfList))
      #print("jackpot Details {}".format(playersJackPotListToList))
      #return playersProfitDetailListOfList
      getAverageEarnings(playersProfitDetailListOfList,numOfDraws)
      getUserJackPotDetails(playersJackPotListToList,numOfDraws)

print(getDrawForAllPlayers(5,10))