# Devvortex

This is my write-up for the machine **Devvortex** on Hack The Box located at: https://app.hackthebox.com/machines/577

## Enumeration

First I started with an nmap scan, which shows the following:

![nmapScan](./res/Devvortex/nmapScan.png)

Since only port 80, a part from port 22 is open, I navigated there to see what are we up against, and the default page was the following

![defaultPage](./res/Devvortex/defaultPage.png)

I opened burpsuite and put it to capture while I navigated around, and also ran gobuster, which found more or less the same as me with the manual enumeration

![gobusterReport](./res/Devvortex/gobusterReport.png)

After that I used gobuster again to search for subdomains, but it didn't found anything

![subdomains](./res/Devvortex/subdomains.png)

I also checked wappalyzer to see the tech stack used

![wap](./res/Devvortex/wap.png)

And I checked the source code of the page while nikto was working. I didn't found anything interesting on the source, but nikto did found something interesting, which was the wp-config.php file

![nikto](./res/Devvortex/nikto.png)

So I tried to access it, but it wasn't possible, I either got a 404 or a 200 with the index.html page

![failedReqToWp-config](./res/Devvortex/failedReqToWp-config.png)

Since I was running out of options I tried to find exploits for the known versions, but I only found a DoS for nginx. I also ran http scripts of nmap, but again only a DoS was found

![nmapPort80Scan](./res/Devvortex/nmapPort80Scan.png)

I knew that I was missing something, and after checking all the information I had until now, I decided to rerun the domain enumeration, but with a bigger list, cause that already happened to me on another box but with the directory listing, and with that I got a new domain **dev.devvortex.htb**

![subdomains2](./res/Devvortex/subdomains2.png)

Which have the following default page

![devDefaultPage](./res/Devvortex/devDefaultPage.png)

As usual I ran gobuster against it, and it displayed some interesting things

![devGobusterReport](./res/Devvortex/devGobusterReport.png)

First I went to explore the readme, which seemed to be about Joomla, it didn't contained any sensitive information though

![readme](./res/Devvortex/readme.png)

After that I went to robots.txt, where I found some interesting directories, which could contain sensitive information

![robots](./res/Devvortex/robots.png)

First I went to administration, and there I found a login  page for Joomla, unfortunately, after a quick google search I found out that there's no default credentials for joomla, cause you have to change the password after installation

![joomlaAdminPanel](./res/Devvortex/joomlaAdminPanel.png)

## Exploitation

So I searched for exploits for Joomla with the version that I had from the readme file, and first it wasn't working cause I passed the url incorrectly, and I also had to install some ruby dependencies, but after that, the exploit displayed the users of joomla

![exploit](./res/Devvortex/exploit.png)

After that I checked the exploit again and I saw another URL, which I tried directly from burpsuite, and it contained the configuration of the application, including the user and password

![configRequest](./res/Devvortex/configRequest.png)

Since the password was weird, I thought that it may be some kind of hash, so I went to crackstation to try to crack it, but it didn't recognize the format

![crackstation](./res/Devvortex/crackstation.png)

So I tried this password directly in the login page, and it worked, I was able to login as lewis with the password **P4ntherg0t1n5r3c0n##** which apparently was stored in plain text

![adminPanel](./res/Devvortex/adminPanel.png)

Once I was there, I knew that I had to get a reverse shell from there, and since there was a lot of options on the admin panel, I googled how to get a shell from there, and I found the following [blog](https://anshildev.medium.com/wordpress-and-joomla-reverse-shells-f76dcdbc0339), so I followed the joomla option, which was going to templates

![templates](./res/Devvortex/templates.png)

There I opened an administrator template and replaced the php code with my reverse shell

![reverseShell](./res/Devvortex/reverseShell.png)

And after navigating to that php template I got the shell back on my listener

![shell](./res/Devvortex/shell.png)

## Post Exploitation

With that I began the enumeration in order to escalate privileges, first I pulled the users

![etcPass](./res/Devvortex/etcPass.png)

I also checked the system information

![sysInfo](./res/Devvortex/sysInfo.png)

Then I checked sudo -l (which asked for a password, so it wasn't possible to use it), and the SUID binaries

![perms](./res/Devvortex/perms.png)

After that I ran linpeas, which showed the following

- Some possible exploits
![linuxExploitSuggester](./res/Devvortex/linuxExploitSuggester.png)

- Network information
![networkInfo](./res/Devvortex/networkInfo.png)

With that information, I went ahead and tried the exploit suggested by linpeas **CVE-2021-3560** with the help of a [pdf](https://www.exploit-db.com/docs/50607) that I found on exploit-db

![checkingMiliseconds](./res/Devvortex/checkingMiliseconds.png)

But after some tries it doesn't seem to be working

![exploitFail](./res/Devvortex/exploitFail.png)

Since this exploit was tied to service accounts and also recommended by linpeas, I thought that it was the way to go, but maybe I was doing something wrong. So I got a meterpreter shell in order to try this exploit from there, and to my surprise metasploit recognized the target as not vulnerable

![confirmingThatTargetIsNotVulnerable](./res/Devvortex/confirmingThatTargetIsNotVulnerable.png)

So, taking advantage that I already had a meterpreter shell, I ran the local exploit suggester

![localExploitSuggester](./res/Devvortex/localExploitSuggester.png)

But none of them worked

![localExploitFail](./res/Devvortex/localExploitFail.png)

Since I was stuck I decided to check the write-up, and there they explained that we should check the port listening to discover that there's a MySQL runnning

![network](./res/Devvortex/network.png)

Now we are able to connect there with the same credentials we used to enter the admin panel, and we should be able to extract the credentials for logan from here, I thought that we dumped everything with the previous exploit, but it seems that isn't the case

![checkMySQLtables](./res/Devvortex/checkMySQLtables.png)
![checkingUsers](./res/Devvortex/checkingUsers.png)

With that information we should be able to grab the hash and crack it with hashcat

![hashcat](./res/Devvortex/hashcat.png)

Now we have to use this to do a lateral movement and login into logan via ssh

![sshLogan](./res/Devvortex/sshLogan.png)

Once we begin the enumeration on this new account, we see that there's an interesting command on sudo

![sudo](./res/Devvortex/sudo.png)

Checking GTFObins, we could see that the command isn't there

![GTFObins](./res/Devvortex/GTFObins.png)

But if we google it, we found this [github page](https://github.com/diego-tella/CVE-2023-1326-PoC) where there's an explanation on how to use apport-cli to escalate privileges, and with that it was enough to get an elevated shell

![elevatedShell](./res/Devvortex/elevatedShell.png)

Now the only thing left to do was retrieve the flags

![flags](./res/Devvortex/flags.png)
