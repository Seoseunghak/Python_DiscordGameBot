import requests
import json

# pip install requests 하시길 바람
playerURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
rankURL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"
api_key = 'Input Your API Key'
print('롤 아이디 입력 : ')
a = input()

sohwansa = playerURL + a + '?api_key=' + api_key

response = requests.get(sohwansa)
data = json.loads(response.text)
print(data)
id = data["id"]
print(id)

sohwansaRank = rankURL + id + '?api_key=' + api_key
response = requests.get(sohwansaRank)
data = json.loads(response.text)
print(data)
print(len(data))
if len(data) == 1:
    if data[0]["queueType"] == 'RANKED_SOLO_5x5':
        solo = data[0]
        unrankQ = 'RANKED_FLEX_SR : Unranked'
        stype, stier, spoint, srank = solo["queueType"], solo["tier"], solo["leaguePoints"], solo["rank"]
        print(stype + " : " + stier + " " + srank + " " + str(spoint))
        print(unrankQ)

    else:
        multi = data[0]
        unrankQ = 'RANKED_SOLO_5x5 : Unranked'
        mtype, mtier, mpoint, mrank = multi["queueType"], multi["tier"], multi["leaguePoints"], multi["rank"]
        print(unrankQ)
        print(mtype + " : " + mtier + " " + mrank + " " + str(mpoint))

else:
    if data[0]["queueType"] == 'RANKED_SOLO_5x5':
        solo = data[0]
        multi = data[1]

    else:
        solo = data[1]
        multi = data[0]

    stype, stier, spoint, srank = solo["queueType"], solo["tier"], solo["leaguePoints"], solo["rank"]
    mtype, mtier, mpoint, mrank = multi["queueType"], multi["tier"], multi["leaguePoints"], multi["rank"]
    print(stype + " : " + stier + " " + srank + " " + str(spoint))
    print(mtype + " : " + mtier + " " + mrank + " " + str(mpoint))

