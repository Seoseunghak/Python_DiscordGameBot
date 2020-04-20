import discord
import os
import requests
import bs4
import asyncio
import urllib
from user_exception import NonameError, NotierError


async def lol_record(msg, nick):
    channel = msg.channel

    try:
        location = urllib.parse.quote(nick)
        url = "https://www.op.gg/summoner/userName=" + location
        html = urllib.request.urlopen(url)
        bs = bs4.BeautifulSoup(html, "html.parser")

        profile = bs.find("div", {"class" : "Profile"})
        if profile is None:
            raise NonameError

        name = profile.find("span", {"class" : "Name"})

        nameText = name.text.strip()
        embed = discord.Embed(title='{0}님의 롤 전적'.format(nameText), description='테스트', color=0xffa6c9)

        content = bs.find("div", {"class" : "SideContent"})
        tierBox = content.find("div", {"class" : "TierBox Box"})
        subtierBox = content.find("div", {"class" : "sub-tier"})

        tierImg = tierBox.find("img").get("src")
        tierImgURL = "https:" + str(tierImg)
        embed.set_thumbnail(url=tierImgURL)

        soloRank = tierBox.find("div", {"class" : "TierRank"}).text.strip()
        print(soloRank)
        soloInfo = tierBox.find("span", {"class" : "LeaguePoints"})
        if soloInfo is None:
            embed.add_field(name='솔로랭크', value='**티어 : {0}**'.format(soloRank), inline=True)

        else:
            soloInfo = soloInfo.text.strip()
            solowin = tierBox.find("span", {"class" : "wins"}).text.strip().replace('W', '승')
            sololose = tierBox.find("span", {"class" : "losses"}).text.strip().replace('L', '패')
            solorate = tierBox.find("span", {"class": "winratio"}).text.strip().replace('Win Ratio', '승률')
            embed.add_field(name='솔로랭크',
                            value='**티어 : {0}**\n**{1} / {2} {3}**\n**{4}**'.format(soloRank, soloInfo, solowin, sololose, solorate),
                            inline=True)

        subRank = subtierBox.find("div", {"class" : "sub-tier__rank-tier unranked"})
        if subRank is not None:
            subRank = subRank.text.strip()
            embed.add_field(name='5:5 랭크', value='**티어 : {0}**'.format(subRank), inline=True)

        else:
            subRank = subtierBox.find("div", {"class" : "sub-tier__rank-tier"}).text.strip()
            subInfolist = subtierBox.find("div", {"class" : "sub-tier__league-point"}).text.strip().split('/')
            subInfolist[1] = subInfolist[1].replace('W', '승').replace('L', '패')
            subInfo = " / ".join(subInfolist)
            subrate = subtierBox.find("div", {"class" : "sub-tier__gray-text"}).text.strip().replace('Win Rate', '승률')
            embed.add_field(name='5:5 랭크',
                            value='**티어 : {0}**\n**{1}**\n**{2}**'.format(subRank, subInfo, subrate),
                            inline=True)

        embed.add_field(name='\u200b', value='\u200b', inline=False)
        mostChamp = content.find("div", {"class" : "MostChampionContent"})

        if mostChamp is None:
            embed.add_field(name='Most 3 챔피언', value='기록이 없어요!', inline=True)

        else:
            most1 = mostChamp.find("div", {"class" : "ChampionBox Ranked"})


        await channel.send(embed=embed)

    except NonameError:
        await channel.send('입력하신 닉네임을 찾지 못했어요!')

    except NotierError:
        await channel.send("티어 정보가 없어요!")