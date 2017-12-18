# fntsylu
ESPN Fantasy Basketball Daily Lineup Automator

This is a script to set my ESPN Fantasy Basketball lineup daily. Not fully automative as it does not add players off
the bench and into the starting lineup if all the spots are taken, and of course, the players in those spots have games.
In that case, the script sends me an email with the amount of players who were unable to be added to the lineup. This is a slightly modified version of michael-langaman's fntsylu script which can be found [here](https://github.com/michael-langaman/fntsylu). The current version of mine is made for 16 player rosters. If you want to change this, basically just go through and change everywhere there's a '16' to whatever size roster your league uses.

# How to use

First, you'll need to install:
 - google-chrome
 - selenium webdriver

Next, clone or download the repository and extract the fntsylu folder. Now, open up the teams.csv file in any text editor and enter the following, with no spaces between the fields, and all in one line.

```
'ESPN Username','ESPN Password','LeagueID','TeamID','SeasonID'

```
If you want to automate more than one team, with possibly different ESPN accounts, add a line of information for each team in the teams.csv file and each lineup will be set when the code is run. An example of a correct entry might be:

> fntsyBballGuy,password123,7609,18,2018

'7609' is the ID of the league that I want to enter. '18' is the team ID. You can find your league and team ID by reading the url of the homepage of your fantasy league. '2018' is just the current year.

Before you edit this file, you'll need to create a gmail account that will notify you when there are players still on your bench. After you create the email, go back into the email.csv file and add the following line:

```
'Gmail Username','Gmail Password'
```

If you want the email sent to an account other than this one, you can edit the sendEmail function, setting `recipientEmail` to the email desired.

Once you find your league and team IDs and your email, go to your command line and change directory to the fntsylu folder, then type the following:
 > python fntsylu.py

Chrome should open up and the script should be setting your lineup

# Crontab

Next, you can set up cron to run the command for you. In the terminal, type
 > crontab -e

And enter the following at the bottom of the crontab file:
 > 0 11 * * * export DISPLAY=:0; /usr/bin/python /path/to/setLineup.py

For the example line above, cron will run the script every day at 11.
