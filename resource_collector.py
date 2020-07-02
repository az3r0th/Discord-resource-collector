import discord
import re
import requests
from bs4 import BeautifulSoup
from github import Github

#edit these
github_token="Your_GitHub_Access_Token"
discord_token="Your_Bot's_Token"
repo_name="Name_of_Your _repo"
channel_name="Name_of_Your_Channel"
name_of_file="File_in_which_resources_will_be_stored"  #create a markdown file for better view




g = Github(github_token) #GitHub Instance

repo = g.get_repo(repo_name) #Getting repo object
url_pattern=r'(https?://)(\w+\.)?\w+\.\w{2,}'
title=r'(?<=title>)\w+(?=</)'

client = discord.Client() #Getting Client Object

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client)) 

#When message is sent to channel this event repeats it self
@client.event
async def on_message(message):
    if message.channel.name == channel_name and re.match(url_pattern,message.content):
        text1=requests.get(message.content)
        soup=BeautifulSoup(text1.text,'html.parser')
        resource=repo.get_contents(name_of_file)
        tmp=resource.decoded_content.decode('utf-8')
        a=tmp+f"- [{soup.title.text}]"+f"({message.content})\n" #Appending the link in Markdownformat
        repo.update_file(resource.path,"Updating resources",a,resource.sha) #updatethe file
        
client.run(discord_token)