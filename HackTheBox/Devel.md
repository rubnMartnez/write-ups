# Devel

This is my write-up for the machine **Devel** on Hack The Box located at: https://app.hackthebox.com/machines/3

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/Devel/nmapScan.png)

Since anonymous login is allowed, I connected there to see if there's something interesting that we could pull, or if we are allowed to upload files, which it seems we are, so probably we can upload a reverse shell, and since the port 80 is open as well maybe we can get it executed from there

![ftpEnum](./res/Devel/ftpEnum.png)

With that information, I procced to enumerate port 80, which show us the following default page. This tell us that the server is running IIS7, which we already know from the nmap scan, but it's good to confirm

![port80defaultPage](./res/Devel/port80defaultPage.png)

We could see that we are able to access the file that we uploaded before with ftp, so now the next step will be google for a reverse shell for IIS7 and upload it

![port80test](./res/Devel/port80test.png)

## Exploitation

I found the following aspx shell online

![aspxShell](./res/Devel/aspxShell.png)

Then I upload it to the server via FTP

![uploadShell](./res/Devel/uploadShell.png)

I start a netcat listener

![ncListener](./res/Devel/ncListener.png)

but after trying to access the shell on the server I got an error

![shellError](./res/Devel/shellError.png)

So I tried a different approach, which was a simpler shell that grants a cmd over port 80

![aspxShell2](./res/Devel/aspxShell2.png)

And this time it worked

![shell2Whoami](./res/Devel/shell2Whoami.png)

I tried some one liners to connect back to my netcat, but none of them worked, so I got back to trying a direct reverse shell. I found a different one which is quite longer

![shell3Code](./res/Devel/shell3Code.png)

And this one connected properly

![shell3Connection](./res/Devel/shell3Connection.png)

## Post Exploitation

When I went to get the flags, it seems that we have no access, so we'll have to do some privilege escalation

![usersPermissionDenied](./res/Devel/usersPermissionDenied.png)

### Enumeration

I did some information gathering in order to prepare for the privilege escalation by pulling the systeminfo

![systeminfo](./res/Devel/systeminfo.png)

And the priviliges and groups, where we could see that SeImpersonatePrivilege is enabled

![privsAndGroups](./res/Devel/privsAndGroups.png)

### Privilege Escalation

After some googling about how to escalate privileges on that version, I saw that using [JuicyPotato](https://github.com/ohpe/juicy-potato/tree/master) was recommended. So I cloned the repo and tried to compile it

![juicyPotatoCompilation](./res/Devel/juicyPotatoCompilation.png)

But since it is compatible with windows and not linux, I was getting some compilation errors, so I've decided to pull a precompiled one

![juicyPotatoCompilationError](./res/Devel/juicyPotatoCompilationError.png)
![pullPrecompiledJuicyPotato](./res/Devel/pullPrecompiledJuicyPotato.png)

Then I tried to upload it to the target machine, but I've got an error, since I did not have writting permissions on that folder

![errorPullingJuicyPotatoOnTarget](./res/Devel/errorPullingJuicyPotatoOnTarget.png)

So I had to find a folder with permissions

![findFolderWithPermissions](./res/Devel/findFolderWithPermissions.png)

But when I run it, it gave me an error, it seems that I've uploaded the wrong version

![versionProblems](./res/Devel/versionProblems.png)

## Different Approach

Since I felt that I was going down a rabbit hole, I checked the official write-up, which gave me the hint to use msfvenom to get the shell in the first place

![msfvenomShell](./res/Devel/msfvenomShell.png)

And with that, after configuring the metasploit listener, we get a meterpreter shell

![meterpreterShell](./res/Devel/meterpreterShell.png)

With that session, since we already know that the windows is x86 from before, I used the local exploit suggester to get modules that I could use to escalate privileges

![localExploitSuggester](./res/Devel/localExploitSuggester.png)

I checked the official write-up again to see which one is the one that works, then I use it to gain the root shell

![gainRootShell](./res/Devel/gainRootShell.png)

Now it's only matter of get the flags, which we already know where they are from before

![userFlag](./res/Devel/userFlag.png)
![rootFlag](./res/Devel/rootFlag.png)