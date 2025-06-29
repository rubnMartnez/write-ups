# Active

This is my write-up for the machine **Active** on Hack The Box located at: https://app.hackthebox.com/machines/148

## Enumeration

First I started with an [nmap scan](./res/Active/10_10_10_100_nmapReport.txt), which shows the following

![nmapScan](./res/Active/nmapScan.png)

It looks like a typicall windows domain configuration, so first I decided to trigger the enum4linux to gather some general information

![enum4linux](./res/Active/enum4linux.png)

After that I tried listing the shares

![shares](./res/Active/shares.png)

And then I tried to access them, but I only got access to Replication

![shareAccess](./res/Active/shareAccess.png)

After some manual enumeration I found two interesting files, which are GptTmpl.inf that contains some password policies, and Groups.xml which seems to contain a user with some kind of hash

![Replication](./res/Active/Replication.png)

After that I ran some nmap scripts againts smb to enumerate it further, but nothing interesting came through

![smbNmapScripts](./res/Active/smbNmapScripts.png)

And I tried pulling some information from ldap, but the files were empty

![ldapDomainDump](./res/Active/ldapDomainDump.png)

## Exploitation

So before enumerating the other ports, I decided to dig deeper on the hash obtained, first I tried to identify which type of hash it was with hashid and crackstatation, but it didn't work

![hashid](./res/Active/hashid.png)

So, I tried googling for "smb groups xml encryption" and I found [this page](https://github.com/incredibleindishell/Windows-AD-environment-related/blob/master/Exploiting-GPP-AKA-MS14_025-vulnerability/README.md) where they talk about how to decrypt it and provide [this script](https://github.com/incredibleindishell/Windows-AD-environment-related/blob/master/Exploiting-GPP-AKA-MS14_025-vulnerability/gppdecrypt.rb), so I went ahead and try to decrypt the password, and it actually worked

![gppDecrypt](./res/Active/gppDecrypt.png)

Then I tried to get into another share with the recently obtained credentials **active.htb\SVC_TGS:GPPstillStandingStrong2k18** but I got an error on all of them

![sharesFail](./res/Active/sharesFail.png)

So I triggered crackmapexec to make sure the credentials were right

![crackmapexec](./res/Active/crackmapexec.png)

I also tried getting a shell with psexec, but it seems that we don't have write permissions on any share

![psexec](./res/Active/psexec.png)

So I enumerated the users with crackmapexec, but it seems that there's only the default ones a part from the one that we have credentials

![userEnum](./res/Active/userEnum.png)

After that I tried to connect to the Replication share, and when I saw that it didn't work either I realized that I was doing something wrong, and after a few tries I was able to connect to the Users share

![UsersShare](./res/Active/UsersShare.png)

## Post Exploitation

There I was able to retrieve the user flag

![userFlag](./res/Active/userFlag.png)

After that I used GetUserSPNs.py to check if kerberoasting was possible, and I got the Administrator hash

![adminHash](./res/Active/adminHash.png)

Then I went to hashcat to crack it, and it actually did really fast, and the credentials were **Administrator:Ticketmaster1968**

![hashCracked](./res/Active/hashCracked.png)

With that I used psexec to get an elevated shell

![elevatedShell](./res/Active/elevatedShell.png)

And then the only thing left to do was retrieving the root flag

![rootFlag](./res/Active/rootFlag.png)
