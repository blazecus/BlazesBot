import os

import re
import discord
import dotsandboxes

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()


client.state_per_server = dict()
client.game_per_server = dict()

for i in client.guilds:
    client.state_per_server[i] = "NO GAME"
    client.game_per_server[i] = None

@client.event
async def on_message(message):
    guild = message.guild.id

    if(guild not in client.state_per_server):
        client.state_per_server[guild] = "NO GAME"
        client.game_per_server[guild] = None

    if(client.state_per_server[guild] == "NO GAME"):
        print("asdkflja;lskdjfa;lskjdf;laskjdf;lakj")
        if(bool(re.match("!playgame dotsandboxes [0-9]*x[0-9]* <@.*>", message.content))):
            message_content = message.content.split(" ")
            (width, height) = [int(i) for i in message_content[2].split("x")]
            if(len(message.mentions) == 1):
                player2 = message.mentions[0].id
                client.state_per_server[guild] = "dotsandboxes"
                client.game_per_server[guild] = dotsandboxes.dotsandboxes(message.author.id, player2, width, height)
                game = client.game_per_server[guild]
                await message.channel.send(game.print_board())
                await message.channel.send("%s's turn!" % ("<@" + str(game.current_player) + ">"))
    
    if(client.state_per_server[guild] == "dotsandboxes"):
        game = client.game_per_server[guild]
        if(message.author.id == game.current_player):
            if(bool(re.match("!move [0-9]*,[0-9]* [0-9]*,[0-9]*", message.content))):
                coords = message.content.split(" ")
                (x1,y1,x2,y2) = [int(i) for i in coords[1].split(",")] + [int(i) for i in coords[2].split(",")]
                if game.check_valid(x1,y1,x2,y2):
                    game.place_line(x1,y1,x2,y2)
                    if(game.tie):
                        client.state_per_server[message.guild.id] = "NO GAME"
                        await message.channel.send("TIE!!!")
                    elif(game.done):
                        client.state_per_server[message.guild.id] = "NO GAME"
                        await message.channel.send(game.print_board())
                        await message.channel.send("GAME OVER! %s WINS WITH " % ("<@" + str(game.current_player) + ">") + str(game.winning_score) + " POINTS!")
                    else:
                        await message.channel.send(game.print_board())
                        await message.channel.send("%s's turn!" % ("<@" + str(game.current_player) + ">"))
                else:
                    await message.channel.send("Invalid choice, try again.")
client.run(TOKEN)