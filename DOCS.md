# Axiol tutorial
Oh hey, look who is here! Welcome to Axiol bot documentation (well kinda) <br>

## Getting started
The first recommended command after you have invited the bot to your server is **```.plugins```**. Go ahead I'm waiting.......done? Great! </br>
Now you will see all the plugins which Axiol provides, here you can manage plugins by reacting to their respective emojis in the embed! </br> </br>
To change the prefix use the command **``.prefix``**. In case you forgot what you changed your prefix to; then just ping Axiol and ask him the prefix just you like you would to anyone else! For example:
> Oh hey @Axiol, what's your prefix?</br>
> @Axiol prefix?</br>
> @Axiol What was your prefix again?</br>
> I forgot the prefix @Axiol, can you help me?</br>

The prefix used in all examples will be the default one therefore a dot ```.```, use your own prefix if changed. </br>
For every role, user, member and text channel either their mention or ID can be used, for example: </br
This...
> ```.avatar @Bolt#8905```
> ```.alertchannel #🧪｜testing```
> ```.addmodrole @Moderator```

and this...
> ```.avatar 791950104680071188```
> ```.alertchannel 843516136540864512```
> ```.addmodrole 843563902078812171```

are same. </br>

Note that `User` and `Member` are different, whenever there is `Member` in a command that means only people which are in the server can be used, while `User` is global therefore a person does not need to be in the server for you to use any command which requires a `User`. </br> </br>

Looks great so far? Let's move on! Here are some quick links to the plugins
- [🛡️ AutoMod](#AutoMod)
- [🤖 ChatBot](#ChatBot)
- [🎭 Karma](#Karma)
- [📊 Leveling](#Leveling)
- [🔨 Moderation](#Moderation)
- [✨ ReactionRoles](#ReactionRoles)
- [✅ Verification](#Verification)
- [👋 Welcome](#Welcome) 
- [➡️ Extras](#Extras) *This is not a plugin*

Using any command from a plugin which is disabled will return an error embed. </br>

## AutoMod
Help command: ```.help automod```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865970528871383080/unknown.png" width=280> </br>
By default the plugin is disabled.

#### .filters
  Shows all auto moderation filters, the enabled/disabled emoji before their names shows their status whether they are enabled or disabled </br>
  To configure each filter, use the command ```.filter <filter_name>```. There are four filters: ```badwords```, ```links```, ```invites```, ```mentions``` </br></br>
  To change the response of each filter react to the [gear emoji](https://cdn.discordapp.com/emojis/860554043284914218.png?v=10?size=10). To toggle between enable/disable, react to the other emoji which would be either the [disable](https://cdn.discordapp.com/emojis/847850081700020254.png?v=1) emoji if currently that filter is enabled and would be [enable](https://cdn.discordapp.com/emojis/847850083819323442.png?v=1) emoji if currently that filter is disabled. </br>
  All filter configuration commands are only visible in that filter's embed only if the filter is enabled. </br> </br>
  BadWords and Mentions filters have some extra configurations available, let's have a look into that! </br>
  * BadWords: 
  ```.addbadword <your_word>``` To add any badword in the list which bot would delete</br>
  ```.removebadword <you_word>``` To remove any badword, make sure that the word is already in the bad word list or else it won't work, but wait how would you make sure...? Let's move on to the next command for it! </br>
  ```.allbadwords``` To view all bad words, this will show all words which the bot does not like therefore deletes them!</br>
  * Mentions
  ```.mentionamount``` To add a custom amount of mentions which the bot would delete for mass mentions, remember that only unique mentions are deleted!
  
#### .automodblacklist <channel>
  This command blacklists a channel from auto moderation, users are immune to all filters in that channel.
      
#### .automodwhitelist <channel>
  By default, all channels are whitelisted hence protected with auto moderation but if any channel has been blacklisted using the command above then they can be whitelisted again using this command.
  
#### .addmodrole <role>
  This commands adds a role in the *moderator role list* therefore members having any of the roles which are in the list are immune to all auto moderation actions by the bot.

#### .removemodrole <role>
  Any role which has been added as a mod role earlier can be removed from the list using this command, members having this role would no longer be immune to auto moderation.
  
#### .allmodroles
  Use this command to see all moderator roles which you have added to the list, moderator is the just a common usage and example but you can add any roles :D

#### .ignorebots
  Use the command to toggle betwen ignorebots mode, this mode decides whether other bots will be affected by auto moderation by Axiol or not, using the command returns an embed which tells the current status of ignorebots mode, to switch just react to the emoji which Axiol will add itself, it would be either the [enable](https://cdn.discordapp.com/emojis/847850083819323442.png?v=1) emoji or [disable](https://cdn.discordapp.com/emojis/847850081700020254.png?v=1) depending on the current status.

  
## ChatBot
Help command: ```.help chatbot```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865985154689400872/unknown.png" width=280> </br>
By default this plugin is enabled therefore Axiol will reply to all pings, disabling the plugin would make Axiol not reply to any messages or pings.
  
#### .setchatbot <channel>
  This commands sets a channel to a chatbot channel therefore all messages in that channel will be replied by Axiol and users would not need require to ping!

#### .removechatbot <channel>
  This commands removes a channel from chatbot channel list if it is there, therefore Axiol would no longer reply to all messages there

#### .chatbotchannels
  This commands shows all channels which are chatbot channels, the channels shown in the embed are where the bot replies to all messages by everyone
 
#### .chatbotreport <description>
  If the chatbot does anything wrong, behaves weirdly or does not work then a quick report to the [support server](https://discord.gg/hxc73psNsB) can be sent with just this command without needing to join the server and reporting manually, the description has no limit so it can be as long as you want.
  
  
## Karma
Help command: ```.help karma```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865987550325506108/unknown.png" width=280> </br>
By default this plugin is disabled, very similar to leveling the only difference being users earn points for being nice!
  
#### .karma <user>
  Shows the karma of the user! If the user is not defined then the karma of the person who used the command is shown, depending on the user's karma and average a small description about the performence is also there!
  
#### .karmaboard
  Shows the karma board! This also shows the average server karma and has a format very similar to leveling leaderboard, the person who used the command can move to different pages using the arrow reactions in the embed:
``` 
  * ◀️ for first page
  * ⬅️ for previous page
  * ➡️ for next page
  * ▶️ for last page
```
#### .kblacklist <channel>
  This blacklists a channel with karma therefore any member messaging anything won't gain any karma, by default no channels are blacklisted

#### .kwhitelist <channel>
  By default all channels are blacklisted therefore giving users karma based on their messages, if any channel has been blacklisted using the command above then they can be whitelisted again using this command.

  
## Leveling
Help command: ```.help leveling```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865989871486631966/unknown.png" width=280> </br>
By default the plugin is disabled.

#### .rank <user>
  Shows server rank of a user by returning an embed with all information and box emojis for progress bar x) Use the command without user field to check your own rank, note that this is user therefore xp of members who have left the server is also available.

#### .leaderboard
  Returns an embed with the entire server leaderboard and a clean pagination, to move between pages the system is exactly the same as karma board with one extra option in center:
```  
    * ◀️ for first page
    * ⬅️ for previous page
    * 📊 for top 10 users bargraph image
    * ➡️ for next page
    * ▶️ for last page
```
  The bargraph emoji is a bit different than shown here, it was not possible to show custom discord emoji here.
  
#### .bargraph <amount>
  Sends a bargraph image of top users in the leaderboard, the amount field left blank returns top 10 users however the amount can be defined upto 30, more than that was slow and harder to fit in >.<

#### .piechart <amount>
  Same as bargraph just shows piechart instead
  
#### .givexp <user> <amount>
  Adds more XP to a user, the maximum amount which can be given to someone is **10000000**, giving someone XP using this command does not send the levelup alert message.
  
#### .removexp <user> <amount>
  Removes xp from a user, the maximum amount is same as `.givexp` command therefore **10000000**, removing more XP than what user current has puts them in debt therefore negative XP.
  
#### .levelinfo
  Shows all the level related information which includes highest xp member, xp range, xp blacklisted channels, alert status, alert channel and rewards by if there are any.
  
#### .levelconfig
  This sends an embed which has all leveling related configurations which admins can change, let's have a look at them one by one:
  * `.xprange <min_value> <max_value>`: 
  This sets the xp range between which members will be given random xp, setting up the same xp in both min value and max value will make the xp static therefore
  giving everyone same xp everytime.
  * `.blacklist <channel>`:
  This blacklists a channel from XP hence members won't gain any XP in the channel which are in the blacklisted list, by default no channels are blacklisted.
  * `.whitelist <channel>`:
  By default all channels are whitelist hence give members XP, any channel which has been blacklisted using the command just before this can be whitelisted again with this.
  * `.togglealerts`:
  This is a quick way to turn on/off alerts, if level up alerts are turned on then they are disabled and if they are disabled then are enabled right after entering the command, no confirmation or reaction required.
  * `.reward <level> <role>`:
  Add a role reward for a level! The level field should only be the level itself therefore a number, whenever members reach the level setted up they are automatically given the role.
  * `removereward <level>`:
  Removes any role reward from a level if it has been setted up earlier using the command just before this.
  
  
## Moderation
Help command: ```.help moderation```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865997578503192611/unknown.png" width=280> </br>
By default the plugin is enabled.
                
>
