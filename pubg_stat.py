import discord
import os
import requests
import bs4
import asyncio
import urllib
import json
from user_exception import ViewError, SquadError, NoserverError, NogameError

viewPoint = ''
view_display = ''
co_player = ''
co_display = ''
server_play = ''
server_display = ''

async def pubg_record(msg, view, server, coop, ingame):
    channel = msg.channel

    try:
        if view == 1:
            viewPoint = "-fpp"
            view_display = '1인칭'
        elif view == 3:
            viewPoint = ""
            view_display = '3인칭'
        else:
            raise ViewError

        if server == '스':
            server_play = "steam"
            server_display = '스팀'
        elif server == '카':
            server_play = "kakao"
            server_display = '카카오'
        else:
            raise NoserverError

        if coop == '솔':
            co_player = "solo"
            co_display = '솔로'
        elif coop == '듀':
            co_player = "duo"
            co_display = '듀오'
        elif coop == '스':
            co_player = "squad"
            co_display = '스쿼드'
        else:
            raise SquadError

        url = "https://dak.gg/profile/" + ingame
        html = urllib.request.urlopen(url)
        bs = bs4.BeautifulSoup(html, "html.parser")
        nickname = bs.find("span", {"class" : "nick"})
        if nickname is None:
            raise KeyError

        nickname = nickname.text.strip()
        mode = co_player + viewPoint
        playerURL = "https://api.pubg.com/shards/" + server_play + "/players"
        seasonURL = "https://api.pubg.com/shards/" + server_play + "/seasons"
        params = {"filter[playerNames]": ""}
        params["filter[playerNames]"] = nickname
        headers = {"Accept": "application/vnd.api+json",
                   "Authorization": "Input your Auth"}

        response = requests.get(playerURL, headers=headers, params=params)

        data = json.loads(response.text)
        print(data["data"][0]["id"])
        accountID = data["data"][0]["id"]

        response = requests.get(seasonURL, headers=headers)
        data = json.loads(response.text)
        last = len(data["data"])
        print(data["data"][last - 1]["id"])
        lastSeason = data["data"][last - 1]["id"]

        statURL = "https://api.pubg.com/shards/" + server_play + "/players/" + accountID + "/seasons/" + lastSeason
        response = requests.get(statURL, headers=headers)
        data = json.loads(response.text)

        print(data["data"]["attributes"]["gameModeStats"][mode])
        roundPlayed = data["data"]["attributes"]["gameModeStats"][mode]["roundsPlayed"]
        if int(roundPlayed) == 0:
            raise NogameError

        rankPoints = data["data"]["attributes"]["gameModeStats"][mode]["rankPoints"]
        kills = data["data"]["attributes"]["gameModeStats"][mode]["kills"]
        wins = data["data"]["attributes"]["gameModeStats"][mode]["wins"]
        top10 = data["data"]["attributes"]["gameModeStats"][mode]["top10s"]
        longest = data["data"]["attributes"]["gameModeStats"][mode]["longestKill"]
        dealTotal = data["data"]["attributes"]["gameModeStats"][mode]["damageDealt"]
        maxKill = data["data"]["attributes"]["gameModeStats"][mode]["roundMostKills"]
        headshot = data["data"]["attributes"]["gameModeStats"][mode]["headshotKills"]

        rankPoints = int(rankPoints)
        losses = roundPlayed - top10
        top10 = top10 - wins
        winrate = round(wins / roundPlayed * 100, 1)
        if roundPlayed - wins <= 0:
            kd = 'Perfect!'
        else:
            kd = round(kills / (roundPlayed - wins), 2)
        longest = round(longest, 1)
        dealTotal = int(dealTotal / roundPlayed)
        if int(kills) == 0:
            headshot = 0;
        else:
            headshot = round(headshot / kills * 100, 1)

        embed = discord.Embed(title='{0}님의 배그 전적'.format(nickname), description='**서버 : {0}\n모드 : {1}\n팀 : {2}**'.format(server_display, view_display, co_display), color=0xffa6c9)
        embed.add_field(name='레이팅', value='**{0}**'.format(rankPoints), inline=True)
        embed.add_field(name='승/탑/패', value='**{0}W {1}T {2}L**'.format(wins, top10, losses), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=False)

        embed.add_field(name='승률', value='**{0}%**'.format(winrate), inline=True)
        embed.add_field(name='K/D', value='**{0}**'.format(kd), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=False)

        embed.add_field(name='평균 딜량', value='**{0}**'.format(dealTotal), inline=True)
        embed.add_field(name='최다 킬', value='**{0}킬**'.format(maxKill), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=False)

        embed.add_field(name='헤드샷', value='**{0}%**'.format(headshot), inline=True)
        embed.add_field(name='최장거리 킬', value='**{0}m**'.format(longest), inline=True)

        await channel.send(embed=embed)

    except ViewError:
        await channel.send('시점은 1 또는 3으로만 입력해주세요!\n예시) *배그 3 스 스 인게임아이디')

    except NoserverError:
        await channel.send('서버는 스, 카 중에 하나를 입력해주세요!\n예시) *배그 3 스 스 인게임아이디')

    except SquadError:
        await channel.send('팀원은 솔, 듀, 스 중에 하나를 입력해주세요!\n예시) *배그 3 스 스 인게임아이디')

    except KeyError:
        await channel.send('찾으시는 닉네임이 없어요!')

    except NogameError:
        await channel.send('플레이 기록이 없어요!\n게임을 한판 이상 플레이해주세요!')

    except urllib.error.HTTPError:
        await channel.send('올바르지 않은 닉네임 형식을 사용했어요!\n다시 입력해주세요!')