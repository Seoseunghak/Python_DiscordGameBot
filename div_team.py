import discord
import numpy
import random
import asyncio
import os

# 숫자를 받아 해당 숫자의 정원으로 팀을 나누고 팀 리스트를 반환
# number -> 팀 정원, channel_member -> 해당 채널 멤버 리스트, total_team_list -> 팀 전체 리스트
def divide_team(number, channel_member, total_team_list):
    total_member = len(channel_member)                      # 현재 참여하고 있는 보이스 채널 내의 멤버 숫자
    team_count = len(channel_member) // number              # 전체 멤버에서 지정된 팀 수를 나눈 몫
    remain_member = total_member % number                   # 전체 멤버에서 지정된 팀 수를 나눈 나머지

    # team_count 만큼
    for i in range(0, team_count):
        a_team = []

        for i in range(0, number):
            select_member = channel_member.pop(0)
            a_team.append(select_member)

        total_team_list.append(a_team)

    if (remain_member != 0):
        a_team = []

        for i in range(0, remain_member):
            select_member = channel_member.pop(0)
            a_team.append(select_member)

        total_team_list.append(a_team)

    return total_team_list


# divide_team 에서 리턴된 total_team_list를 받아 팀 결과 메세지 전송
# total_team_list -> 팀 전체 리스트, voice_members -> 보이스 채널 멤버 리스트
def show_team_result(total_team_list, voice_members):
    team_number = 1                                               # 몇번째 팀
    total_mention_list = []
    total_mention = ''

    for i in range(0, len(total_team_list)):
        a_team_member = len(total_team_list[i])                   # 각 팀 인원 수

        for j in range(0, a_team_member):
            member = discord.utils.find(lambda x : x.display_name == total_team_list[i][j], voice_members)
            total_mention = total_mention + member.mention

        total_mention_list.append(total_mention)
        total_mention = ''

    return total_mention_list






