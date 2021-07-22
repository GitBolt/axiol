# Axiol tutorial
Oh hey, look who is here! Welcome to Axiol bot documentation.<br>

<img src="https://cdn.discordapp.com/attachments/843519647055609856/845662999686414336/Logo1.png" width=100>

## Getting started
The first recommended command after you have invited the bot to your guilds is **```.plugins```**. Go ahead I'm waiting.......done? Great! </br>
Now you will see all the plugins which Axiol provides, here you can manage them by reacting to their respective emojis in the embed. </br></br>

To change the prefix use the command **``.prefix``**. In case after changing the prefix you forget what it was, then just ping (mention) Axiol and ask it the prefix just you like you would to anyone else! For example:
> Oh hey @Axiol, what's your prefix?</br>
> @Axiol prefix?</br>
> @Axiol What was your prefix again?</br>
> I forgot the prefix @Axiol, can you help me?</br>

## Before continuing
The prefix used in all examples will be the default one therefore a dot ```.```, use your own prefix for the commands if changed. </br>
For every role, user, member and text channel either their mention or ID can be used, for example: </br>
This...
> ```.avatar @Bolt#8905```
> ```.alertchannel #🧪｜testing```
> ```.addmodrole @Moderator```

and this...
> ```.avatar 791950104680071188```
> ```.alertchannel 843516136540864512```
> ```.addmodrole 843563902078812171```

are same. </br>

Also note that `User` and `Member` are different, whenever there is `Member` in a command that means only people which are in the server can be used, while `User` is global therefore a person does not need to be in the guild for you to use any command which requires a `User`. </br> </br>

Looks great so far? Let's move on! Here are some quick links to the plugins
- [🛡️ AutoMod](#AutoMod)
- [🤖 ChatBot](#ChatBot)
- [🎯 Fun](#Fun)
- [🎭 Karma](#Karma)
- [📊 Leveling](#Leveling)
- [🔨 Moderation](#Moderation)
- [✨ ReactionRoles](#ReactionRoles)
- [✅ Verification](#Verification)
- [👋 Welcome](#Welcome) 
- [➡️ Extras](#Extras) *This is not a plugin*

##### But first let's understand command permissions before moving on to plugins

## Command permissions
Command permissions fall under the settings category therefore can be accessed using the command **```.help settings```**. </br>
Using command permissions you can set a role to have the permission to use any command which Axiol provides, for example setting the role "X" for the command "Y" will only let members having the "X" role use command "Y". Here are the commands for this:</br> </br>

- `setperm <plugin_name>`: Using this command will send an embed with all commands from the plugin defined, the next message which you will send will be used to set command permission, the format is `command_name role`; here the command name is used without the prefix otherwise it will trigger the actual command, then seperated by a space you need to enter your role; whether it be the mention or ID, doing so will a command permission where users having that role can only use that command, to cancel this proccess simply type `cancel`, sending the message in wrong format will result in bot sending a warning message, this won't cancel the entire proccess so you can always try again without having to start over, this only stops if you enter `cancel`. </br>
- `removeperm <command> <role>`: This simply removes a command permission of the role from a command. </br>
- `allperms`: This shows all plugin names inside which the command names which have command permission setted up followed by the roles which an use that command. 

##### Understood? Hope so you did, let's go to the plugins part now!

## AutoMod
Help command: ```.help automod```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865970528871383080/unknown.png" width=280> </br>
By default the plugin is disabled.

#### .filters
  Shows all auto moderation filters, the enabled/disabled emoji before their names shows their status whether they are enabled or disabled </br>
  To configure each filter, use the command ```.filter <filter_name>```. There are four filters: ```badwords```, ```links```, ```invites```, ```mentions``` </br></br>

  To change the response of each filter react to the [gear emoji](https://cdn.discordapp.com/emojis/860554043284914218.png?v=10?size=10). To toggle between enable/disable, react to the other emoji which would be either the [disable](https://cdn.discordapp.com/emojis/847850081700020254.png?v=1) emoji if currently that filter is enabled and would be [enable](https://cdn.discordapp.com/emojis/847850083819323442.png?v=1) emoji if currently that filter is disabled. </br>
  All filter configuration commands are only visible in that filter's embed only if the filter is enabled. </br> </br>
  BadWords and Mentions filters have some extra configurations available, let's have a look into that:
  ```
  * BadWords: 
  .addbadword <your_word> - To add any badword in the list which bot would delete
  .removebadword <you_word> - To remove any badword, make sure that the word is already in the bad word list or else it won't work
  .allbadwords - To view all bad words, this will show all words
  
  * Mentions
  .mentionamount - To add a custom amount of mentions which the bot would delete for mass mentions, remember that only unique mentions are deleted!
  ```
#### .automodblacklist \<channel>
  This command blacklists a channel from auto moderation, members are immune to all filters in that channel.
      
#### .automodwhitelist \<channel>
  By default, all channels are whitelisted hence protected with auto moderation but if any channel has been blacklisted using the previous command then they can be whitelisted again using this command.
  
#### .addmodrole \<role>
  This commands adds a role in the *moderator role list* therefore members having any of the roles which are in the list are immune to all auto moderation actions by the bot.

#### .removemodrole \<role>
  Any role which has been added as a moderator role earlier can be removed from the list using this command, members having this role would no longer be immune to auto moderation.
  
#### .allmodroles
  Use this command to see all moderator roles which you have added to the list, moderator is the just a common usage and example but you can add any roles :D

#### .ignorebots
  Use the command to toggle betwen *ignorebots mode*, this mode decides whether other bots will be affected by auto moderation by Axiol or not, using the command returns an embed which tells the current status of ignorebots mode, to switch just react to the emoji which Axiol will add itself, it would be either the [enable](https://cdn.discordapp.com/emojis/847850083819323442.png?v=1) emoji or [disable](https://cdn.discordapp.com/emojis/847850081700020254.png?v=1) depending on the current status.

  
## ChatBot
Help command: ```.help chatbot```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865985154689400872/unknown.png" width=280> </br>
By default this plugin is enabled, therefore Axiol will reply to all pings and disabling this plugin would make Axiol not reply to any messages or pings.
  
#### .setchatbot \<channel>
  This commands sets a channel to a chatbot channel therefore all messages in that channel will be replied by Axiol and members would not need require to ping!

#### .removechatbot \<channel>
  This commands removes a channel from chatbot channel list if it is there, therefore Axiol would no longer reply to all messages there.

#### .chatbotchannels
  This commands shows all channels which are chatbot channels, the channels shown in the embed are where the bot replies to all messages by everyone.
 
#### .chatbotreport \<description>
  If the chatbot does anything wrong, behaves weirdly or does not work then a quick report to the [support server](https://discord.gg/hxc73psNsB) can be sent with just this command without needing to join the server and reporting manually, the description has no limit so it can be as long as you want.
  
## Fun
Help command: ```.help fun```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/867320597595160606/unknown.png" width=280> </br>
By default this plugin is enabled.

#### .typingtest \<type>
  Test your typing speed! There are two types of test right now: `time` and `word` </br>
  - **Time** based typing test is where you need to type as much as you can under the time you specify, note that your goal is not to complete the entire text given!
  - **Word** based typing test is the opposite of time based one, here you need to complete the entire text under 60 seconds, this test is quicker and starts right after you enter the command and has much smaller text.

  2 seconds are subtracted from total time taken to cover up time taken for image to load and user to start typing.

#### .embed \<channel>
  Use this command to create an embed! These embeds are not useful right now which means you would need to create new embed everytime, if you wish to not set anything which Axiol asks then just type `skip`. As you keep going on, the original embed becomes the preview therefore edits itself to the embed you are creating after each step. This will be the proccess:
  - You would need to set the colour, either you can react to one of the colour circle emojis or react to the paint brush emoji to set a custom hex, when you are done press the continue emoji at the last (not compulsary, can be skipped with the default color)
  - Axiol will ask for title (compulsary, title is required)
  - Axiol will ask for descrption (not compulsary, can be skipped by typing 'skip')
  - Axiol will ask for thumbnail, a file or link can be used; only static images (pngs, jpgs etc) supported (not compulsary, can be skipped)
  - The embed is ready to be sent! However you are free to add fields, footer, image and author by reacting to the respective emojis in the new embed sent, at this point you will see a [tick](https://cdn.discordapp.com/emojis/847850079968559175.png?v=1) emoji in your original embed (which became the preview) just click on the tick emoji to send it to the channel which you defined at the beginning when using the command!

#### .avatar \<user>
  Shows the avatar or profile picture as many say of the user! Notice that it's user not member which means avatar of anyone from discord whether they are in server or not can be viewed.


## Karma
Help command: ```.help karma```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865987550325506108/unknown.png" width=280> </br>
By default this plugin is disabled, very similar to leveling the only difference being members earn points for being nice!
  
#### .karma \<user>
  Shows the karma of the user! If the user is not defined then the karma of the person who used the command is shown, depending on the user's karma average, a small description about the performence is also there!
  
#### .karmaboard
  Shows the karma board! This also shows the average guild karma and has a format very similar to leveling leaderboard, the person who used the command can move to different pages using the arrow reactions in the embed:
``` 
  * ◀️ for first page
  * ⬅️ for previous page
  * ➡️ for next page
  * ▶️ for last page
```

#### .kblacklist \<channel>
  This blacklists a channel with karma therefore any member messaging anything in that channel won't gain any karma, by default no channels are blacklisted.

#### .kwhitelist \<channel>
  By default all channels are blacklisted therefore giving members karma based on their messages, if any channel has been blacklisted using the previous command then they can be whitelisted again using this command.

  
## Leveling
Help command: ```.help leveling```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/865989871486631966/unknown.png" width=280> </br>
By default the plugin is disabled.

#### .rank \<user>
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
  
#### .bargraph \<amount>
  Sends a bargraph image of top users in the leaderboard, the amount field left blank returns top 10 users however the amount can be defined upto 30, more than that was slow and harder to fit in >.<

#### .piechart \<amount>
  Same as bargraph just shows piechart instead
  
#### .givexp \<user> \<amount>
  Adds more XP to a user, the maximum amount which can be given to someone is **10000000**, giving someone XP using this command does not send the levelup alert message.
  
#### .removexp \<user> \<amount>
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
<img src="https://cdn.discordapp.com/attachments/843519647055609856/867323748708909056/unknown.png" width=280> </br>
By default the plugin is enabled, reasons in ban, kick are optional and required in warn.
                
#### .ban \<user> \<reason>
  Permanantly bans a user from guild, user ID can be used too therefore users which are not in the server can also be banned, bans using this command are permanant and can only be reversed manually or by using the next command.

#### .unban \<user>
  Unbans a previously banned user from the guild.

#### .kick \<member> \<reason>
  Kicks a member out of the server, which means they can join again.

#### .mute \<member>
  This creates a 'Muted' role on first time usage and 'send messages' permission is disabled from all channels then the member is assigned the role therefore disabling their ability to send messages hence 'Muting', if there is a 'Muted' role already then it is used without creating any new one.

#### .unmute \<member>
  Removes the 'Muted' role from member therefore lets them send messages again.

#### .warn \<member> \<reason>
  Warns a member, the reason is required. Right now warnings does not have any special punishments

#### .removewarn \<member> \<position>
  Removes a warning from a member, the position is the number in which the warn is placed in the list, after removing a warn the warns below it are moved one position upwards to take the place of the warn removed.

#### .warns \<member>
  Shows all warns of the member with their reasons and position.

#### .purge \<amount>
  Deletes the number of messages defined in the amount field from the channel where the command is used, amount can only be a number.

#### .nick \<member> \<newnick>
  Changes nickname of the member to the new nick defined in the command.

#### .addrole \<member> \<role>
  Adds a role to the member.

#### .removerole \<member> \<role>
  Removes a role from the member.

#### .massrole \<role1> \<role2>
  This gets confusing a bit but hey I got you covered! The **role1** is the role *of which* the members are given **role2**, this means every member in the server who has role1 gets role2, this may take some time depending on the number of members, after entering the command a confirmation embed is sent, reacting to the [tick](https://cdn.discordapp.com/emojis/847850079968559175.png?v=1) emoji will update everyone silently, and reacting to the [enable](https://cdn.discordapp.com/emojis/847850083819323442.png?v=1) emoji will update members with live stats which will send a message after the member gets updated with the role and [cross](https://cdn.discordapp.com/emojis/847850006995402822.png?v=1) emoji will cancel it.

#### .massroleremove \<role1> \<role2>
  This works exactly same as the previous command (.massrole) the only difference being **role2** is removed from people with **role1**.


## ReactionRoles
Help command: ```.help reactionroles```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/866549138962907156/unknown.png" width=280> </br>
By default the plugin is enabled.


#### .rr \<channel> \<messageid> \<role> \<emoji>
  This creates a reaction role, which means after using the command, the message having the id in the channel defined in the command gets a react which is the emoji defined in the command and whenever someone reacts to the emoji they are given the role defined

#### .removerr \<messageid> \<emoji>
  This removes a reaction role, since a message can only have one unique emoji simply using the messageid and emoji removes the reaction role

#### .allrr 
  Shows all reaction roles setted up in the server with pagination similar to leaderboard

#### .uniquerr \<messageid>
  This marks a message with unique reaction role therefore a member can only react once and take on emoji from all reaction role defined in a single message.

#### .removeunique \<messageid>
  This unmarks a message with unique reaction role hence letting users reaction resulting in letting them choose as many self roles as they want.


## Verification
Help command: ```.help verification```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/866550881569734656/unknown.png" width=280> </br>
By default this plugin is disabled. There are two types of verification named 'Command verification' and 'Bot verification'. On first time enabling it, Axiol will ask for the channel to create it the verification channel, after sending the channel name it will create a 'Not Verified' and set up proper permissions, in case some role named 'Not Verified' is found then Axiol will ask whether you want it to use the existing role, create new one while leaving the previous one or create a completely new fresh one and removing the previous one.

#### .verifyinfo
  This shows the verification information of the server which includes the verification channel, the verified role, the role which is given after a member is verified and a description of the type of verification the guild has.

#### .verifyswitch
  Since there are only two types of verification avaiable, using this command will switch the verification type quickly without any confirmation.

#### .verifyrole \<role>
  This adds a role which will be given to the members after they verify successfully, this is not required for members to be able to get verfied and view all channels again. At one time only one verified role can be added which means using this command again after setting up a verifyrole will replace the previous role with the new one.

#### .verifyroleremove
  This removes the verifed role, the role is not needed to define since only one verified role can be setted up.

## Welcome
Help command: ```.help welcome```</br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/866552858354122792/unknown.png" width=280> </br>
By default this plugin is disabled. On first time enabling it, Axiol will ask for the channel where it will welcome members.

#### .welcomecard
  Shows the current guild welcome card, it's not an embed since there is also a message outside the embed so together they form the embed 'card'.

#### .welcomechannel \<channel>
  Changes the welcome channel where members will be greeted.

#### .welcomemessage
  After using this command Axiol will ask for the welcome message, the next message in the same channel by the member who used the command will be setted as the new welcome message. Note that this is the message which is outside the actual embed and this is where the member is pinged, don't confuse it with the greeting!

#### .welcomegreeting
  Similarly to the previous command, Axiol will ask for the welcome greeting. Greeting is the embed description.

#### .welcomeimage
  After using the command the next file or link which you will send will become the embed image, gifs won't work!

#### .welcomerole \<role>
  This will create a autorole which will be given to the members when they join, only works with welcome!

#### .welcomereset
  This resets the welcome card to the default one

These are the default welcome messages which are picked randomly and used:

```
{member} We hope you brought some milk 🥛
{member} Hopped into the server!
{member} Glad to have you here today! 
We hope you brought some sweets 🍩 {member}
Have a pizza slice 🍕 {member}
{member} Woooohooo! We are excited to have you here <a:hyper_cat:809781548210978828>
{member} just joined, hide your cookies!🍪
Swooooooosh! {member} just landed ✈
{member} joined the party <a:party_parrot:810545477668962315>
Roses are red, violets are blue, {member} hopped into the server, are they a kangaroo 🦘?
```

## Extras
Help commands: ```.help extras``` </br>
<img src="https://cdn.discordapp.com/attachments/843519647055609856/867322118785204244/unknown.png" width=280> </br>
This is not a plugin but some extra commands which are also useful. </br>

#### .stats
  Shows the server stats! If the [Verification](#Verification) is enabled then number of members which are not verified is also shown.


#### .about
  Shows bot information including number of server it's in, total number of members, creater, creation date and ping.

#### .suggest \<idea>
  Using this command a direct suggestion to the [Support Server](https://discord.gg/3QfRNFXMzQ) suggestion channel will be sent, there is no limit for the size of the idea.

#### .invite
  Sends the invite link of Axiol.

#### .source
  Sends the GitHub links of Axiol.