import asyncio
import discord
import youtube_dl
import ffmpeg


def ydl_download(rinklist):
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(rinklist.pop(0))
        print(rinklist)
    for file in os.listdir("./"):
        if file.endswith('.mp3'):
            os.rename(file, 'song.mp3')

    lower_song = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('song.mp3'), volume=0.03)
    return lower_song

# 기능 구현 중
def check_queue(rinklist, vclient):
    if rinklist != []:
        rinklist.pop(0)
        print('다음곡!')
        song = ydl_download(rinklist)
        vclient.play(song, after=check_queue(rinklist, vclient))

    else:
        print('큐 종료!')

    # 음성 채널에 봇을 소환합니다.
    if message.content == '*소환':

        # 해당 메시지를 입력한 사람이 보이스채널에 들어가지 않으면
        if not message.author.voice:
            await message.channel.send("먼저 음성채널에 입장해주세요")

        else:
            v_client = None                                             # Bot이 보이스 채널에 있는지 유무

            for vc in app.voice_clients:                                # Bot이 있는 서버들에서
                if vc.guild == message.guild:                           # 봇과 메시지의 길드가 일치하면
                    v_client = vc                                       # Bot이 해당 서버의 보이스 채널에 있음

            if v_client == None:                                        # 해당 서버의 보이스 채널에 없으면
                v_channel = message.author.voice.channel                # 보이스 채널을 메시지 입력자의 보이스 채널로 설정
                await message.channel.send("소나 입장!")
                await v_channel.connect()                               # 설정된 보이스 채널 입장

            else:                                                       # 해당 서버의 보이스 채널에 있다면
                await message.channel.send("이미 들어와있어요!")


    if message.content == '*추방':
        if not message.author.voice:
            await message.channel.send("소나가 있는 채널에 입장해주세요!")

        else:
            v_client = None

            for vc in app.voice_clients:
                if vc.guild == message.guild:
                    v_client = vc

            if v_client == None:
                await message.channel.send("소나가 방에 있나요?")
                pass

            else:
                await message.channel.send("나중에 봐요!")
                await v_client.disconnect()

    if message.content.startswith("*play"):
        if not message.author.voice:
            await message.channel.send("관중이 필요해요!")

        else:
            v_client = None

            for vc in app.voice_clients:
                if vc.guild == message.guild:
                    v_client = vc

            if v_client == None:
                await message.channel.send("소나가 방에 없어요!")
                pass

            else:
                search = ""
                keyword = message.content.split()

                for i in range(1, len(keyword)):
                    search = search + " " + keyword[i]

                print(search)

                path = r'C:\Users\ASUS\Downloads\chromedriver_win32\chromedriver.exe'
                driver = webdriver.Chrome(path)
                driver.get('https://www.youtube.com/results?search_query=' + search)
                source = driver.page_source
                driver.close()

                bs = bs4.BeautifulSoup(source, 'lxml')
                diction = bs.find_all('a', {'id' : 'video-title'})

                try:
                    dictionNum = diction[0]
                    dictionText = dictionNum.text.strip()
                    print(dictionText)

                    diction_hype = dictionNum.get('href')
                    rink = 'https://www.youtube.com' + diction_hype
                    print(rink)

                    if v_client.is_playing():
                        url_list.append([rink])
                        print(url_list)

                    else:
                        url_list.append([rink])
                        print(url_list)

                        song_there = os.path.isfile('song.mp3')

                        try:
                            if song_there:
                                os.remove('song.mp3')

                        except PermissionError:
                            await message.channel.send('현재 음악이 재생중이에요! 곡을 멈추고 다시 시도해주세요!')

                        song = ydl_download(url_list)

                        #v_client.play(discord.FFmpegPCMAudio('song.mp3'), after=check_queue(url_list))
                        #lower_song = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio('song.mp3'), volume=0.03)
                        v_client.play(song)

                except IndexError:
                    await message.channel.send('검색된 영상이 없습니다.')