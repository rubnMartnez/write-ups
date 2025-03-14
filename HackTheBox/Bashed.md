# Bashed

This is my write-up for the machine **Bashed** on Hack The Box located at: https://app.hackthebox.com/machines/118

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/Bashed/nmapScan.png)

Since only the port 80 is open, I proceed to enumerate it, when we navigate to it we are presented with the following page

![defaultPage](./res/Bashed/defaultPage.png)

I run gobuster to see if there are any interesting directories, which seems to be the case

![gobusterReport](./res/Bashed/gobusterReport.png)

If we click on the phpbash from the main page, we are redirected to the single.html file, which have an explanation of how phpbash works, and a link to github with more information. We could also see that on the example they're accessing the shell under /uploads/phpbash.php unfortunately when I went there there was no shell there

![singlePage](./res/Bashed/singlePage.png)

## Exploitation

After navigating through the directories that gobuster facilitated, I found that there's actually a shell on /dev/phpbash.php

![shellFound](./res/Bashed/shellFound.png)

Since we are a low privilege user, I searched for way to escalate privileges, and I found that we should be able to trigger commands as sudo under scriptmanager

![shellFound](./res/Bashed/findingScriptmanagert.png)

But after some tries, I was not able to get a root shell

![scriptmanagerEscalationTries](./res/Bashed/scriptmanagerEscalationTries.png)

I was able to retrieve the user flag though

![userFlag](./res/Bashed/userFlag.png)

Since I was struggling to exploit the scriptmanager because the shell given wasn't interactive enough, I tried a different approach which was creating a reverse shell, first I tried with netcat directly, but the -e flag wasn't working, so I tried a workaround with python, and this one worked

![reverseShell](./res/Bashed/reverseShell.png)

## Post Exploitation

With the reverse shell I was able to get into the scriptmanager, but when I tried to get root I continued to get the error message no tty present

![getScriptmanager](./res/Bashed/getScriptmanager.png)

I tried adding scripts and running them as root inside /home/scriptmanager but I was getting errors, I also tried running linpeas to see if there was something interesting, and since I wasn't finding anything and I was stuck I checked the official write-up, which gave me the hint that there was a folder /scripts owned by scriptmanager but outside of the home folder

![scriptsFolder](./res/Bashed/scriptsFolder.png)

The write-up also suggested to check the timestamps of the files since it a cron job running on the background, and indeed they were changing every minute

![scriptsFolder](./res/Bashed/scriptsTimings.png)

So now all we have to do is replace the test.py with a reverse shell, so we could get root privileges once it is run by it

![scriptsFolder](./res/Bashed/createReverseShell.png)

![scriptsFolder](./res/Bashed/getRootShell.png)

And with that we can retrieve the root flag

![scriptsFolder](./res/Bashed/rootFlag.png)

