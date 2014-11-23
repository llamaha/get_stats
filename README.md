get_stats
=========

Simple Python script to extract statistics from your opponents in League of Legends during loading.  

Obtain your API key from here:
https://developer.riotgames.com/

At the top of the script there is a dictionary that needs to be populated.  Put default values between the quotes along with the API key.

Create the file 'summoners.txt' and put summoner name and champion name separated by spaces:

summoner_name champion_name

There are no spaces in champion names.  For example:

lolplayer987 missfortune

Then just run:

python get_stats.py
