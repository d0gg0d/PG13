# PG13
Password Guesser for a Outlook Web Access portal with /rpc, /ews or /public enabled.

This password guesser is based on a an older shell script with the name owa2013.sh. 
Therefore it's call Password Guesser 13 or PG13 for short. Cause it's safe for kids lol.
I decided to rewrite it in python as an exercise to get better at Python.

Instructions:
	-a, --address		- The URL or the Outlook Web Access Poral. i.e. - webmail.company.com
	-u, --users		- The list of users to password against. If it requires DOMAIN\, please prepend to the usernames. One per line.
	-pw, --passwords	- List of passwords to be tested. One per line.
	-t, --tries		- Number of attempts before waiting.
	-w, --wait		- Wait time after reaching number of tries.
	-o, --output		- File to write output to.

The program will output a log file called "PG13.log" incase any errors or weird response from a server occurs.
This is to help in the debugging process and to let users verify the results that are returned by the program.

Issues:
	I've seen some instances where the program will return a false positive if run too quickly.
	Increase the delay if this becomes an issue.

Future Upgrades:
	-Return the name of the Domain used by the Exchange Server and quit
	-Return the name of the Domain used by the Exchange Server and prepend to the userlist
	-Threading

If you have any tips for improvements, please message me or write an issue post.
