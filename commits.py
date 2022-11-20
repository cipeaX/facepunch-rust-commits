import requests
import json
import time
from discord_webhook import DiscordWebhook, DiscordEmbed

#SETTINGS
my_webhook_url = "PASTE YOUR WEBHOOK URL HERE!"
my_error_webhook = "PASTE WEBHOOK FOR ERROR MESSAGES (CAN BE SET TO THE SAME CHANNEL AS BEFORE)"
checking_rate = 20
#/SETTINGS

last_post_id = ""
second_last_id = ""

while(True):

    #load json
    headers={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}
    r = requests.get("https://commits.facepunch.com/?format=json", headers=headers)
    if(r.status_code != 200):
        print("ERROR! STATUS CODE: " + str(r.status_code))
        webhook = DiscordWebhook(url=my_error_webhook, content="ERROR! STATUS CODE: " + str(r.status_code))
        response = webhook.execute()
        exit(1)
    content = json.loads(r.content)

    #find first commit thats rust related and public
    index = 0
    first_commit = content["results"][index]
    while(str(first_commit["repo"]) != "rust_reboot" or not(first_commit["changeset"].isnumeric()) ):
        first_commit = content["results"][index]
        index += 1

    if(str(first_commit["id"]) != last_post_id and str(first_commit["id"]) != second_last_id):

        print("New commit detected:" + str(first_commit["id"]))

        #make timestamp
        time_created = str(first_commit["created"])
        l = time_created.split("T")
        time_created = "**" + l[0] + "** at **" + l[1] + "**"

        #make embed content
        commit_title = "__New Commit:__"
        commit_description = "**" + str(first_commit["repo"]) + "/" + str(first_commit["branch"]) + "#" + str(first_commit["changeset"]) +  "** by **" + str(first_commit["user"]["name"]) + "**\n\n" + str(first_commit["message"]) + "\n\n" + time_created

        #build embed and send per webhook
        commit_embed = DiscordEmbed(title=commit_title, description=commit_description, color='c84632')
        commit_embed.set_thumbnail(url="https://i.pinimg.com/originals/cc/40/6a/cc406a8382d8df7eb5f395ec884d3c95.png")
        webhook = DiscordWebhook(url=my_webhook_url, content="")
        webhook.add_embed(commit_embed)
        response = webhook.execute()

        second_last_id = last_post_id
        last_post_id = str(first_commit["id"])

    else: print("No new commits detected")

    time.sleep(checking_rate)
