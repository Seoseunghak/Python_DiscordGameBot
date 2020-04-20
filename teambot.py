import discord
import numpy
import random
import asyncio
import os
import requests
import youtube_dl
import bs4
import ffmpeg
from lol_stat import lol_record
from pubg_stat import pubg_record
from selenium import webdriver
from div_team import divide_team, show_team_result
from admin_mention import men_master, men_submaster, men_admin, men_subadmin, men_staff, men_designer, men_botmanager

app = discord.Client()
token = "your bot token"                                                # 비공개 토큰으로 공백처리
ch_member = []                                                          # 채널 멤버 가져오는 리스트
icon = 'https://i.imgur.com/lgfwo6J.jpg'
queue = {}
playerlist = {}
playlist = []
youtubeHref = {}
url_list = []


# 파일 실행 후 로그창에 Bot이름과 id 표시, 현재 상태 변경
@app.event
async def on_ready():
    print('다음으로 로그인 합니다.')
    print(app.user.name)
    print(app.user.id)
    print('===================')
    await app.change_presence(activity=discord.Game('DJ Sona 1.2b | 소나버프좀'))


# 서버에 새 멤버가 들어올 시 환영인사와 안내문
@app.event
async  def on_member_join(member):
    guest_role = discord.utils.find(lambda  a : a.name == '게스트', member.guild.roles)
    await member.add_roles(guest_role)
    channel = discord.utils.find(lambda x : x.id == 690434659980410880, member.guild.channels)
    await channel.send('{0}'.format(member.mention))
    embed = discord.Embed(title='Ability', description='\n\n{0}님 **Ability**에 오신 것을 환영합니다.'.format(member.display_name), color=0xffa6c9)
    embed.add_field(name='\u200b', value='\u200b', inline=False)
    embed.add_field(name='필독!', value='저희 서버를 찾아주셔서 감사합니다!\n\n서버를 이용 하시기 전에 서버에서 사용할 닉네임을 이 채널에 메시지로 보내주세요!\n\n입력양식은 인게임아이디(별명/나이)=성별 입니다.\n예시) BOT-Tester(테스터/27)=남자\n\n보내진 메시지를 통해 닉네임과 성별에 따른 역할이 자동으로 부여됩니다!\n\n'
                                      '인게임아이디는 주로 사용하시는 서버(스팀 또는 카배)의 아이디로 지정해주시고 성별은 남자 또는 여자로 입력해주세요!\n\n', inline=False)
    await channel.send(embed=embed)


# 메세지를 받아서 if문을 통해 처리
@app.event
async def on_message(message):
    # 메세지를 보낸 대상이 봇이면 무시
    if message.author.bot:
        return None

    if message.content == '*로얄':
        whose = discord.utils.find(lambda  x : x.id == 308585237355692032, message.guild.members)
        await message.channel.send('{0}'.format(whose.mention), file=discord.File('royal.png'))

    if message.content == '*넉살':
        whose = discord.utils.find(lambda x : x.id == 285695379100532736, message.guild.members)
        await message.channel.send('{0} : 오늘도 버려지는 인생...'.format(whose.mention))

    if message.content == '*난새':
        whose = discord.utils.find(lambda x: x.id == 394075864045977601, message.guild.members)
        await message.channel.send('{0} : 오늘도 까이는 인생...'.format(whose.mention))

    # 명령어 목록 정리
    if message.content == '*커맨드':
        embed = discord.Embed(title='커맨드 목록', description='\n\n안녕하세요:hearts: DJ Sona 입니다.', color=0xffa6c9)
        embed.set_author(name='DJ Sona', icon_url=icon)
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name='호출 명령어', value='\n\n *마스터 - 마스터를 호출합니다.\n *관리자 - 관리자를 호출합니다.\n *운영진 - 운영진을 호출합니다.\n *스태프 - 스태프를 호출합니다.\n *디자이너 - 컴퓨터를 호출합니다.', inline=False)
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name="게임 관련 명령어",
                        value="\n\n *팀 x - 해당 음성채널의 인원으로 x명 정원의 커스텀 팀을 랜덤으로 구성합니다. \n\n *모집 - 해당 음성채널의 부족한 인원 수와 위치, 초대 링크를 보냅니다.\n\n *투표 x x ... - 스페이스 기준으로 단어를 분할하여 투표를 진행합니다.",
                        inline=False)
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name="부가 커맨드", value='\n\n *주사위 x - 입력한 숫자 안에서 랜덤 숫자를 구합니다.\n\n *소나 - DJ Sona의 가동 여부를 알려줍니다', inline=False)
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.add_field(name="부가 기능", value="\n\n 필독 카테고리에 건의사항 등록 시 비공개 게시판으로 전송되며 등록된 메시지는 삭제됩니다.")
        embed.add_field(name="* 주의!",
                        value="\n\n *팀 기능은 권한자외에도 내전채널(클랜멤버 모두 사용가능)에서 사용 할 수 있습니다.\n 권한 : (부)마스터, 관리자, 운영진, 스태프, BOT\n내전채널 : 기타게임채팅방, 방송실채팅방\n\n *모집 사용 가능 채널 - 스팀/카배인원모집방, 콜오브듀티채팅방, 기타게임채팅방, 방송실채팅방",
                        inline=False)
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.set_footer(text="DJ Sona v1.2b", icon_url=icon)
        await message.channel.send(embed=embed)


    # 가동 여부 확인
    if message.content == '*소나':
        embed = discord.Embed(color=0xffa6c9)
        embed.set_author(name='DJ Sona', icon_url=icon)
        embed.add_field(name='소나 대기중!', value='문제 발생 시 😈BOT에게 DM 주세요!')
        embed.add_field(name='\u200b', value='\u200b', inline=False)
        embed.set_footer(text='DJ Sona v1.21b', icon_url=icon)
        await message.channel.send(embed=embed)


    if message.channel.id == 690434659980410880:
        if message.author.top_role.id == 689833096937603170:
            guest_role = discord.utils.find(lambda a: a.name == '게스트', message.guild.roles)

            try:
                setting = message.content.split('=')

                if len(setting) != 2:
                    raise IndexError

                setnick = setting[0]

                if setting[1] == '남자':
                    setrole = discord.utils.find(lambda a : a.id == 654330266856456243, message.guild.roles)
                    await message.author.edit(nick=setnick)
                    await message.author.add_roles(setrole)
                    await message.author.remove_roles(guest_role)

                elif setting[1] == '여자':
                    setrole = discord.utils.find(lambda  a : a.id == 654328433177919496, message.guild.roles)
                    await message.author.edit(nick=setnick)
                    await message.author.add_roles(setrole)
                    await message.author.remove_roles(guest_role)

                else:
                    await message.channel.send("성별은 남자 또는 여자로만 입력해주세요!")


            except IndexError:
                await message.channel.send("입력 오류! 입력형식은 인게임아이디(별명/나이)=성별 입니다!\n성별은 남자 또는 여자로만 입력해주세요! Ex)botmanager(봇/27)=남자")

        else:
            return None


    # 채널 마스터 호출
    if message.content == '*마스터': await men_master(message)
    if message.content == '*부마스터': await men_submaster(message)
    if message.content == '*관리자': await men_admin(message)
    if message.content == '*운영진': await men_subadmin(message)
    if message.content == '*스태프': await men_staff(message)
    if message.content == '*디자이너': await men_designer(message)
    if message.content == '*봇관리자': await men_botmanager(message)

    # 지정된 숫자 사이의 랜덤 값 전송
    if message.content.startswith('*주사위'):
        x = message.content.split()

        try:
            num = str(x[1])
            await message.channel.send('__**{0}**__ 당첨!'.format(random.randint(1, int(num))))

        except IndexError:
            await message.channel.send('입력 형식은 *주사위 x입니다.')

        except ValueError:
            await message.channel.send('1이상의 숫자를 입력해주세요!\n입력 형식은 *주사위 x입니다.')


    # 채널 건의사항을 받아 비공개 채팅방으로 닉네임과 메세지를 전송 후 삭제
    if message.channel.id == 686896766251171934:
        if message.author.bot or message.author.id == 654327551124176907:
            return None

        else:
            receive_channel = discord.utils.find(lambda x : x.id == 686896828729393152, message.guild.text_channels)
            user_name = message.author.display_name
            opinion = message.content

            await receive_channel.send('{0} 님의 건의사항!\n{1}'.format(user_name, opinion))
            await message.delete()


    #진실의 방 - 클랜 내 분쟁이 있을때 관리자, 신청자, 피신청자와 논의를 하는 채널
    #            운영자방 카테고리의 진실의방 접수처에 신청자와 내용, 관리자멘션을 메시지로 보냄
    if message.channel.id == 695568634789101577:
        if message.author.bot:
            return None

        else:
            receiver_total = ''
            sender = message.author.mention
            text = message.content
            receive_channel = discord.utils.find(lambda x : x.id == 695571549222207519, message.guild.text_channels)
            receiver_list = ['🔸마스터', '🔸부마스터', '🔸관리자', '🔸운영진', '🔸스태프']

            for rcv in receiver_list:
                receiver = discord.utils.find(lambda x : x.name == rcv, message.guild.roles)
                receiver_total = receiver_total + receiver.mention

            await receive_channel.send('{0} 님이 화가 났어요!\n{1}\n{2}'.format(sender, text, receiver_total))
            await message.delete()


    # 권한체크(관리자 또는 권한채널) 후 원하는 인원 수 만큼 랜덤팀 구성 ex) *팀 4 - 4명 정원의 팀을 랜덤으로 구성
    if message.content.startswith("*팀"):
        if(message.guild.get_role(662809948052258826) or message.guild.get_role(654327551124176907) or message.guild.get_role(654327186848743484) or message.guild.get_role(654327971011887104) or message.guild.get_role(654328104558264341)
            or message.channel.id == 686900056905089027 or message.channel.id == 689823236694736937):

            ch_member.clear()
            team_list = []                                                              # 각 팀을 나누는 이중 리스트
            x = message.content.split()

            try:
                num = str(x[1])

                cha : discord.VoiceChannel = None                                       # 보이스 채널 클래스 cha 선언
                cha = message.author.voice.channel                                      # cha에 메세지를 작성한 멤버의 해당 보이스 채널 할당

                for mem in cha.members:                                                 # 해당 보이스 채널의 멤버들의 하나를 mem에 저장해서 순회
                    if (mem.nick == None):                                              # 멤버의 닉네임이 없다면
                        ch_member.append(mem.display_name)                              # 멤버의 표기된 이름으로 리스트에 저장

                    else:
                        ch_member.append(mem.nick)                                      # 멤버의 닉네임을 리스트에 저장

                numpy.random.shuffle(ch_member)

                team_list = divide_team(int(num), ch_member, team_list)                 # divide_team() => div_team.py의 모듈
                count = 1

                mentioned_list = show_team_result(team_list, cha.members)               # show_team_result() => div_team.py의 모듈

                for i in range(0, len(mentioned_list)):
                    await message.channel.send('[ {0} 팀 ] {1}'.format(count, mentioned_list[i]))
                    count += 1

                team_list.clear()

            except IndexError:                                                          # 입력 형식 에러 ex) *팀2
                await message.channel.send('입력 형식은 *팀 x 입니다.')

            except ValueError:                                                          # 값 형식 에러 ex) *팀 가
                await message.channel.send('숫자를 입력해주세요!\n입력 형식은 *팀 x 입니다.')

            except ZeroDivisionError:                                                   # 0으로 나눌 경우 ex) *팀 0
                await message.channel.send('팀원을 0으로 나눌 수 없어요!')

            except AttributeError:                                                      # VoiceChannel이 None인 경우
                await message.channel.send('**음성채널에 먼저 입장해주세요!**')


    # 음성 채팅방에 부족한 인원을 모집하는 기능 - 해당 음성채널, 부족한 인원 수, 초대링크 전송 / 출력 --> ~~에서 x명 모집!
    if message.content == '*모집':
        # 모집 커맨드 채널 제한
        if(message.channel.id == 686866398928175133 or message.channel.id == 686866451415695371 or message.channel.id == 689823236694736937 or message.channel.id == 689628590903656538 or message.channel.id == 686900056905089027 or message.channel.id == 547408388301127716
            or message.guild.get_role(662809948052258826) or message.guild.get_role(654327551124176907) or message.guild.get_role(654327186848743484) or message.guild.get_role(654327971011887104) or message.guild.get_role(654328104558264341)):

            print(message.author.nick)
            try:
                cha = message.author.voice.channel                                           # 작성자가 들어가있는 음성채널 정보를 받아옴

                link = await cha.create_invite(reason='즐겜배그 스타트', max_age=3600)       # 음성채널의 초대 링크를 생성
                left_member = cha.user_limit - len(cha.members)                              # 음성채널의 남은 자리

                if(cha.user_limit == 0):                                                     # 인원제한 없는 채널일 경우
                    await message.channel.send('**{0} 여기로 모여라!**{1}\n{2}'.format(cha.name, message.guild.default_role, link))

                elif(left_member == 0):                                                      # 남은 자리가 없는 경우
                    await message.channel.send('자리가 다 찼어요 ㅠㅠ')

                else:
                    await message.channel.send('**{0} 에서**\n\n **{1}명 구해요!**\n{2}'.format(cha.name, left_member, link))

            except AttributeError:                                                           # 작성자가 음성채널에 없는 경우
                await message.channel.send('**음성채널에 먼저 입장해주세요!**')

        else:
            await message.channel.send('스팀 또는 카배 모집방에서 이용해주세요!')

    # 커스텀 관련 사진 전송
    if message.content == '*커스텀':
        await message.channel.send(file=discord.File('custom.jpg'))


    if message.content.startswith('*배그'):
        x = message.content.split()

        try:
            viewPoint = int(x[1])
            serv = str(x[2])
            co_op = str(x[3])
            ingameID = str(x[4])

            await pubg_record(message, viewPoint, serv, co_op, ingameID)

        except IndexError:
            await message.channel.send("입력 형식이 옳지 않습니다!\n입력 형식은 *배그 인칭(1/3) 서버(스/카) 팀(솔/듀/스) 인게임아이디 입니다!\n예시) *배그 3 스 스 Emsang76")

        except ValueError:
            await message.channel.send("입력 형식이 옳지 않습니다!\n입력 형식은 *배그 인칭(1/3) 서버(스/카) 팀(솔/듀/스) 인게임아이디 입니다!\n예시) *배그 3 스 스 Emsang76")


    if message.content.startswith("*롤"):
        nickname = ''
        x = message.content.split()
        for i in range(1, len(x)):
            nickname = nickname + ' ' + x[i]

        try:
            lolnick = nickname.strip()

            await lol_record(message, lolnick)

        except IndexError:
            pass

        except ValueError:
            pass

    if message.content.startswith('*삭제'):
        if message.author.id == 316934997699330048:
            x = message.content.split()
            try:
                count = int(x[1])

                await message.channel.purge(limit=count)
                await message.channel.send('{0}개의 메시지를 삭제했어요!'.format(count))

            except Exception:
                await message.channel.send('입력 형식은 *삭제 숫자 입니다.\n예시) *삭제 10')


    # 리액션 이모지 체크
    if message.content == '*따봉':
        emoji = '\N{THUMBS UP SIGN}'
        msg = await message.channel.send("따봉!")
        await msg.add_reaction(emoji)


    # *투표 x x x x.... - 스페이스를 기준으로 단어를 분할하여 투표를 시작합니다.
    # 1. x 2. x .... 로 출력 후 해당 번호에 맞는 숫자 이모지를 전송합니다.
    if message.content.startswith('*투표'):
        context = ""                                    # 출력할 투표목록을 모아놓을 String
        try:
            x = message.content.split()                 # message를 스페이스 기준으로 쪼개서 리스트 x에 넣음
            if(len(x) == 1):                            # x의 길이가 1이면 ValueError 예외를 발생시킴
                raise ValueError

            if(len(x) > 10):                            # x의 길이가 10개 초과하면 IndexError 예외를 발생시킴
                raise IndexError                        # 최대 9개까지 투표 가능

            x.pop(0)                                    # x에서 '*투표'를 삭제

            # 숫자 1 ~ 9까지의 이모지에 대한 명칭을 리스트에 넣음
            emoji_list = ['{0}\N{COMBINING ENCLOSING KEYCAP}'.format(digit) for digit in range(1, len(x)+1)]

            # index = 투표목록 x의 인덱스, value = 투표목록 x의 값 // 즉, context는 1. 커피\n2. 쥬스.....
            for index, value in enumerate(x):
                context += "{0}. {1}\n".format(index+1, value)

            msg = await message.channel.send(context)   # 명령어가 들어온 채널에 메시지를 보냄
            print(context)

            for emo in emoji_list:                      # 보낸 메시지 하단에 리액션 이모지를 추가함
                await msg.add_reaction(emo)

        except ValueError:
            await message.channel.send("입력 형식은 *투표 x x x ..... 입니다!")

        except IndexError:
            await message.channel.send("10개 이상 투표는 조금 곤란해요...")


    # *찾기 x - 유튜브에서 x를 검색해 첫번째 영상의 링크를 디스코드에 전송합니다.
    if message.content.startswith("*찾기"):
        search = ""
        keyword = message.content.split()

        # *찾기 뒤에 단어들을 연결
        for i in range(1, len(keyword)):
            search = search + " " + keyword[i]

        print(search)

        path = r'C:\Users\ASUS\Downloads\chromedriver_win32\chromedriver.exe'               # 크롬드라이버 경로 path
        driver = webdriver.Chrome(path)                                                     # 경로에 있는 웹드라이버 실행
        driver.get('https://www.youtube.com/results?search_query=' + search)                # 유튜브 검색 url의 정보를 가져옴
        source = driver.page_source                                                         # 해당 페이지의 소스를 가져옴
        driver.close()                                                                      # 드라이버 종료

        bs = bs4.BeautifulSoup(source, 'lxml')                                              # 페이지 소스의 lxml 크롤링
        diction = bs.find_all('a', {'id' : 'video-title'})                                  # 검색에 나온 영상들의 video-title 정보를 가져옴

        dictionNum = diction[0]                                                             # 정보 중 첫번째 영상의 정보 dictionNum
        dictionText = dictionNum.text.strip()
        print(dictionText)

        diction_hype = dictionNum.get('href')                                               # dictionNum의 하이퍼링크를 가져옴
        rink = 'https://www.youtube.com' + diction_hype                                     # 하이퍼링크를 추가해 유튜브 url를 생성
        print(dictionText + '\n' + rink)

        youtubeHref[0] = rink                                                               # youtubeHref에 링크를 추가

        if not youtubeHref:                                                                 # youtubeHref에 링크가 없으면
            await message.channel.send("검색한 영상이 없습니다.")

        else:
            print(youtubeHref[0])
            url = youtubeHref[0]
            await message.channel.send(dictionText + "\n" + url)                            # 영상의 제목과 url를 메시지로 보냄


app.run(token)