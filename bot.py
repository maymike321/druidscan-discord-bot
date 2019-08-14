import re
import sys
from discord import Client
from comment_parser import CommentParser

if len(sys.argv) != 2:
    print("Bot token must be passed in as a command line argument")
    exit()

token = sys.argv[1]

client = Client()
commentParser = CommentParser()

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    commentToSend = commentParser.parse_comment(message.content)
    if commentToSend != '':
        await message.channel.send(f'{commentToSend}')

def get_double_bracketed_texts(messageContent):
    return list(filter(lambda match: not match.startswith('['), re.findall(r'\[\[(.*?)\]\]', messageContent, re.M | re.I)))

def get_triple_bracketed_texts(messageContent):
    return re.findall(r'\[\[\[(.*?)\]\]\]', messageContent, re.M | re.I)

client.run(token)