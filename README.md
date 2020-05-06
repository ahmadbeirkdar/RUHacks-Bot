# Ru Hacks Discord Bot

Due to COVID, Ru Hacks moved virtual to Discord. So the organizers at Ru Hacks need a bot to manage the server. 


This features a fully automated verification system. As soon as the user joins the discord, the bot checks the DB(mongodb) if the discord is associated with an account. If not the bot prompts the user for his/her email, if the email is found and there is no discord registered under this account it will set the discord field to the discord account and let them in. If the email is found but a different discord username was found under that email, the discord bot will send a verification request to a channel which admins can view only, the admins will simply manually look over the information. If everything indeed checks out, they will be verified. This feature also sets the user's roles based on his application, high school student, university student, hacker and mentor. It also automatically sets the user's first name and first letter of the user's last name as his discord nickname. 


Many other features such as mutlipage embeded messages, and tickets.


Bot usage below. 


```
Bot Usage:

	Mentor and above:
		$ticket @user1 @user2 @user3 .... etc. (Creates a private channel with the author and the users tagged)
		$add @user1 @user2 @user3 .... etc. (Adds users to the private channel, only usable in the private channel)
		$remove @user1 @user2 @user3 .... etc. (Removes users from the private channel, only usable in the private channel)
		$done (Archives the private channel, only usable in the private channel)

	Organizer:
		$addschedule <day1,day2,day3> <Title> | <date> (Example: $addschedule day1 First event | May 6 8:00AM)
		$delschedule <day1,day2,day3> <item> (Example: $delschedule day1 1)
		$verify @user <ROLES: uni, hs, mentor, hacker> (Works in #verification to manually verify users which were not found in the DB, example: $verify @1338#0198 uni hacker)

	Users:
		$stream (Displays stream information)
		$schedule (Displays the Ru Hacks schedule)

	DMs ONLY(Verifications):
		$check <email> (Checks if email in DB and if the discord it appends it)
		$request <EMAIL: required> <REASON: optional> (Pulls data info and sends to the verification channel for manual verification)
```

This bot won't be changed or actively developed anytime soon. Maybe for RuHacks 2021, well actually hopefully not, we dont want COVID to last that long :P
