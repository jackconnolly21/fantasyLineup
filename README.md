# fantasyLineup
ESPN Fantasy Basketball Daily Lineup Automator

This is a script to set my ESPN Fantasy Basketball lineup daily. Not fully automative as it does not add players off
the bench and into the starting lineup if all the spots are taken, and of course, the players in those spots have games.
In that case, the script sends me an email with the amount of players who were unable to be added to the lineup. This is a slightly modified version of michael-langaman's fntsylu script which can be found [here](https://github.com/michael-langaman/fntsylu).

# How to use

First, you'll need to install:
 - google-chrome
 - selenium webdriver

Next, clone or download the repository and extract the fantasyLineup folder.

Then, before you edit this next method, you'll need to create a gmail account that will notify you when there are players still on your bench. After you create the email, go back into the `sendEmail()` function and change the following lines:

```python
def sendEmail(self, players):
   // some code ///
   email = ""          # Insert the email you just created
   password = ""       # Insert the password for the email you just created
   recipientEmail = "" # Insert the email you want to be notified (your personal email)
   // rest of the code //
```

Additionally, this automation is currently set up for 16-man rosters, but this can be easily changed by changing the `setLineup.ROSTERSIZE` variable at the end of the code.

Finally, to run the automation you need to find some information about your ESPN team and account. The first two arguments are the username and password for your ESPN account, respectively. The third is the LeagueID for your league and the fourth is your TeamID, which can be found by reading the url of the homepage of your fantasy league. Finally, the last argument is the SeasonID (just the year).

In order this is: 'ESPN Username' 'ESPN Password' 'LeagueID' 'TeamID' 'SeasonID'

For example to run the file, navigate to the fantasyLineup folder in your terminal and type the following, replacing the arguments with your information:

 > python setLineup.py fntsyBballGuy password123 7609 18 2018

Chrome should open up and the script should be setting your lineup

# Crontab

Next, you can set up cron to run the command for you. In the terminal, type
 > crontab -e

And enter the following at the bottom of the crontab file:
 > 0 11 * * * export DISPLAY=:0; /usr/bin/python /path/to/setLineup.py 'ESPN Username' 'ESPN Password' 'LeagueID' 'TeamID' 'SeasonID'

For the example line above, cron will run the script every day at 11. A good way to check that your crontab syntax is actually valid is to use https://crontab.guru/.
