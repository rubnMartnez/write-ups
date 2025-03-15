# Grandpa

This is my write-up for the machine **Grandpa** on Hack The Box located at: https://app.hackthebox.com/machines/13

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/Grandpa/nmapScan.png)

Since only the port 80 is open I navigated to it and we are presented with the following page

![defaultPage](./res/Grandpa/defaultPage.png)

I run gobuster to see if there's any interesting subdirectories

![gobusterReport](./res/Grandpa/gobusterReport.png)

Since I wasn't finding anything interesting on the directories neither on the source code, I decided to run some vulnerability scans

![nmapScript](./res/Grandpa/nmapScript.png)
![niktoReport](./res/Grandpa/niktoReport.png)

With that information we know that the exploit probably would be in how those files are handled and the front page, but since I was not familiar with it, I researched how IIS work more in depth

## Exploitation

After gathering the information I started looking for exploits and try some commands suggested, but none of them worked

![failedAttemps](./res/Grandpa/failedAttemps.png)

Until I tried a metasploit module that was suggested, which actually worked

![meterpreterShell](./res/Grandpa/meterpreterShell.png)

## Post Exploitation

The problem was that this shell seemed to have really low privileges that I couldn't even run getuid

![shellRestrictions](./res/Grandpa/shellRestrictions.png)

So I tried migrating processes and it actually worked, at least now we are able to run getuid and some other commands in order to escalate privileges

![processMigration](./res/Grandpa/processMigration.png)

![basicEnum](./res/Grandpa/basicEnum.png)

Since it is a x86 system i tried with the local exploit suggester, which showed the following

![localExploitSuggester](./res/Grandpa/localExploitSuggester.png)

And after some tries, one of the modules suggested worked, and now we have system privileges

![privEscalation](./res/Grandpa/privEscalation.png)

So now the only thing left is to get the flags

![userFlag](./res/Grandpa/userFlag.png)
![rootFlag](./res/Grandpa/rootFlag.png)
