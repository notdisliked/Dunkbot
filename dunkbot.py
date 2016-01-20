try:
    import discord
    import requests
    import json
    import random
    import ConfigParser

    config = ConfigParser.ConfigParser()
    config.read("credentials.cfg")

    client = discord.Client()
    client.login(config.get('Credentials', 'discordEmail'), config.get('Credentials', 'discordPass'))

    @client.event
    def on_message(message):
        messageByWord = message.content.split(" ")

        if message.author == client.user:
            return

        if message.content.startswith('!dunkey'):
            r = requests.get('https://www.googleapis.com/youtube/v3/search?key=' + config.get('Credentials', 'youtubeApiKey') + '&channelId=UCsvn_Po0SmunchJYOWpOxMg&type=video&order=date&maxResults=50&part=snippet')
            j = r.json()
            numVids = j['pageInfo']['totalResults']
            vidNum = None
            print(j)
            if len(messageByWord) == 1:
                vidNum = random.randrange(numVids)
            else:
                try:
                    vidNum = int(messageByWord[1]) - 1
                except ValueError:
                    print("I can't find that video")
                    return
            for x in range(0, vidNum / 50):
                nextPageToken = j['nextPageToken']
                r = requests.get('https://www.googleapis.com/youtube/v3/search?key=AIzaSyAwUUgh_BI2pmAaTf2srzA54zb7wa9Ot_o&channelId=UCsvn_Po0SmunchJYOWpOxMg&type=video&order=date&maxResults=50&part=snippet&pageToken=' + nextPageToken)
                j = r.json()
            videoId = j['items'][vidNum % 50]["id"]["videoId"]
            client.send_message(message.channel, "https://www.youtube.com/watch?v=" + videoId)

    @client.event
    def on_ready():
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    client.run()
except Exception as e:
    print(traceback.print_exc())
