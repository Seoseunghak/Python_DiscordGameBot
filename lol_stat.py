import discord
import os
import requests
import bs4
import asyncio
import urllib
import json
from lol_champion import champ_dict
from user_exception import NonameError, NotierError


async def lol_record(msg, nick):
    channel = msg.channel
    playerURL = "https://kr.api.riotgames.com/lol/summoner/v4/summoners/by-name/"
    rankURL = "https://kr.api.riotgames.com/lol/league/v4/entries/by-summoner/"
    masteryURL = "https://kr.api.riotgames.com/lol/champion-mastery/v4/champion-masteries/by-summoner/"
    api_key = 'Input your API Key'

    try:
        stype = '솔로 랭크'
        mtype = '자유 랭크'

        location = urllib.parse.quote(nick)
        url = "https://www.op.gg/summoner/userName=" + location
        html = urllib.request.urlopen(url)
        bs = bs4.BeautifulSoup(html, "html.parser")

        profile = bs.find("div", {"class" : "Profile"})
        if profile is None:
            raise NonameError

        name = profile.find("span", {"class" : "Name"}).text.strip()
        content = bs.find("div", {"class" : "SideContent"})
        tierBox = content.find("div", {"class" : "TierBox Box"})
        tierImg = tierBox.find("img").get("src")
        tierImgURL = "https:" + str(tierImg)

        user = playerURL + name + '?api_key=' + api_key
        response = requests.get(user)
        data = json.loads(response.text)
        id = data["id"]

        userRank = rankURL + id + '?api_key=' + api_key
        response = requests.get(userRank)
        data = json.loads(response.text)

        if len(data) == 0:
            sStr = '**티어 : Unranked**'
            mStr = '**티어 : Unranked**'

        elif len(data) == 1:
            if data[0]["queueType"] == 'RANKED_SOLO_5x5':
                solo = data[0]
                stier, spoint, srank = solo["tier"], solo["leaguePoints"], solo["rank"]
                swins, slosses = solo["wins"], solo["losses"]
                swinrate = round(swins / (swins + slosses) * 100, 1)
                sStr = '**티어 : {0} {1}**\n**{2} LP / {3} 승 {4} 패**\n**승률 : {5} %**'.format(stier, srank, spoint, swins, slosses, swinrate)
                mStr = '**티어 : Unranked**'

            else:
                multi = data[0]
                mtier, mpoint, mrank = multi["tier"], multi["leaguePoints"], multi["rank"]
                mwins, mlosses = multi["wins"], multi["losses"]
                mwinrate = round(mwins / (mwins + mlosses) * 100, 1)
                sStr = '**티어 : Unranked**'
                mStr = '**티어 : {0} {1}**\n**{2} LP / {3} 승 {4} 패**\n**승률 : {5} %**'.format(mtier, mrank, mpoint, mwins, mlosses, mwinrate)

        else:
            if data[0]["queueType"] == 'RANKED_SOLO_5x5':
                solo = data[0]
                multi = data[1]

            else:
                solo = data[1]
                multi = data[0]

            stier, spoint, srank = solo["tier"], solo["leaguePoints"], solo["rank"]
            mtier, mpoint, mrank = multi["tier"], multi["leaguePoints"], multi["rank"]
            swins, slosses, mwins, mlosses = solo["wins"], solo["losses"], multi["wins"], multi["losses"]
            swinrate = round(swins / (swins + slosses) * 100, 1)
            mwinrate = round(mwins / (mwins + mlosses) * 100, 1)
            sStr = '**티어 : {0} {1}**\n**{2} LP / {3} 승 {4} 패**\n**승률 : {5} %**'.format(stier, srank, spoint, swins, slosses, swinrate)
            mStr = '**티어 : {0} {1}**\n**{2} LP / {3} 승 {4} 패**\n**승률 : {5} %**'.format(mtier, mrank, mpoint, mwins, mlosses, mwinrate)

        userMastery = masteryURL + id + '?api_key=' + api_key
        response = requests.get(userMastery)
        data = json.loads(response.text)
        print(data)

        champ, level, point = str(data[0]["championId"]), data[0]["championLevel"], data[0]["championPoints"]
        most1_info = 'MOST 1 - {0}\n숙련도 : {1} , 포인트 : {2}\n'.format(champ_dict[champ], level, point)

        champ, level, point = str(data[1]["championId"]), data[1]["championLevel"], data[1]["championPoints"]
        most2_info = 'MOST 2 - {0}\n숙련도 : {1} , 포인트 : {2}\n'.format(champ_dict[champ], level, point)

        champ, level, point = str(data[2]["championId"]), data[2]["championLevel"], data[2]["championPoints"]
        most3_info = 'MOST 3 - {0}\n숙련도 : {1} , 포인트 : {2}\n'.format(champ_dict[champ], level, point)

        embed = discord.Embed(title='{0}님의 롤 정보'.format(name), description='**서버 : KR**', color=0xffa6c9)
        embed.add_field(name='{0}'.format(stype), value='{0}'.format(sStr), inline= True)
        embed.add_field(name='{0}'.format(mtype), value='{0}'.format(mStr), inline=True)
        embed.add_field(name='\u200b', value='\u200b', inline=False)

        embed.add_field(name='모스트 3 챔피언', value='**{0}**\n**{1}**\n**{2}**'.format(most1_info, most2_info, most3_info))
        embed.set_thumbnail(url=tierImgURL)
        await channel.send(embed=embed)

    except NonameError:
        await channel.send('해당 아이디가 검색되지 않았어요!')
