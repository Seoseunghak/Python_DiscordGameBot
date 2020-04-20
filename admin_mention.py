import discord

# 채널 마스터 호출
async def men_master(message):
    whose = discord.utils.find(lambda a: a.name == '🔸마스터', message.guild.roles)
    await message.channel.send('{0}님 찾습니다!'.format(whose.mention))

# 채널 부마스터 호출
async def men_submaster(message):
    whose = discord.utils.find(lambda a: a.name == '🔸부마스터', message.guild.roles)
    await message.channel.send('{0}님 찾습니다!'.format(whose.mention))

# 채널 관리자 호출
async def men_admin(message):
    whose = discord.utils.find(lambda a: a.name == '🔸관리자', message.guild.roles)
    await message.channel.send('{0}님 찾습니다!'.format(whose.mention))

# 채널 운영진 호출
async def men_subadmin(message):
    whose = discord.utils.find(lambda a: a.name == '🔸운영진', message.guild.roles)
    await message.channel.send('{0}님 찾습니다!'.format(whose.mention))

# 채널 스태프 호출
async def men_staff(message):
    whose = discord.utils.find(lambda a: a.name == '🔸스태프', message.guild.roles)
    await message.channel.send('{0}님 찾습니다!'.format(whose.mention))

# 채널 디자이너 호출
async def men_designer(message):
    whose = discord.utils.find(lambda a: a.name == '🔸디자이너', message.guild.roles)
    await message.channel.send('{0}님 외주 들어왔어요!'.format(whose.mention))

# 채널 봇관리자 호출
async def men_botmanager(message):
    whose = discord.utils.find(lambda a: a.name == '🔸봇 관리자', message.guild.roles)
    await message.channel.send('{0}는 인공지능이 아닙니다! 사람이에요.'.format(whose.mention))
