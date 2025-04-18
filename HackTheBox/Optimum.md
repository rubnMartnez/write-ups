# Optimum

This is my write-up for the machine **Optimum** on Hack The Box located at: https://app.hackthebox.com/machines/6

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/Optimum/nmapScan.png)

Since only the port 80 is open, I proceed to enumerate it, when we navigate to it we are presented with the following page

![defaultPage](./res/Optimum/defaultPage.png)

I run gobuster to see if there's some interesting subdirectories, but apparently not

![gobusterReport](./res/Optimum/gobusterReport.png)

After some navigation through the web, I saw that the server Information section redirect us to another domain, which is rejetto, which apparently is the technology used to build the server, it could be interesting to search information about it

![serverInfoAndRejetto](./res/Optimum/serverInfoAndRejetto.png)

I also tried searching for default credentials for rejetto, but nothing came out, instead and exploit for that specific version showed up, so we can give it a try

## Exploitation

So I went ahead and search for the metasploit module that was suggested

![metasploitModule](./res/Optimum/metasploitModule.png)

I configured the options and run the exploit, but it failed

![exploitFail](./res/Optimum/exploitFail.png)

So I tried with the second option that showed up before, and this one actually worked

![getShell](./res/Optimum/getShell.png)

## Post Exploitation

Doing some basic enumeration, we could see that we are kostas user, and that we have an x86 meterpreter shell, while the system is x64

![generalEnum](./res/Optimum/generalEnum.png)

So I did a process migration in order to match the shells

![processMigration](./res/Optimum/processMigration.png)

Then I used the local exploit suggester to see if there's some vulnerability to escalate privileges

![localExploitSuggester](./res/Optimum/localExploitSuggester.png)

Before trying the exploits from the suggester, I tried incognito and kiwi modules, but I wasn't able to get anything from them

![incognitoTry](./res/Optimum/incognitoTry.png)

I've tried some local exploit suggester modules, but none of them worked. So I went ahead and do some more enumeration by checking the privileges and searching for WSL

![privsAndWSL](./res/Optimum/privsAndWSL.png)

Also checked for stored creds, but nothing was there either

![cmdkey](./res/Optimum/cmdkey.png)

So I got back to the local exploit suggester modules, the first one that I tried said that the user wasn't on admin group

![escalationFail](./res/Optimum/escalationFail.png)

That made me enumerate the users further

![users](./res/Optimum/users.png)

And also ran winPEAS, where I saw that LSA, credetials guard, and so on were not enabled

![winPEAS](./res/Optimum/winPEAS.png)

Which gave me the idea to try the following module

![exploitConfig](./res/Optimum/exploitConfig.png)

And with that I finally got an elevated shell

![gettingElevatedShell](./res/Optimum/gettingElevatedShell.png)

Then the only thing left was to get the flags

![userFlag](./res/Optimum/userFlag.png)
![rootFlag](./res/Optimum/rootFlag.png)
