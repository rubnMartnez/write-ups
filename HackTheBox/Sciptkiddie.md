# Scriptkiddie

This is my write-up for the machine **Scriptkiddie** on Hack The Box located at: https://app.hackthebox.com/machines/314

## Enumeration

First I started with an [nmap scan](./res/Scriptkiddie/10_10_10_226_nmapReport.txt), which shows the following

![nmapScan](./res/Scriptkiddie/nmapScan.png)

Since only port 5000 was open apart from ssh, I navigated there to see what were we up against

![defPage](./res/Scriptkiddie/defPage.png)

Then as usual, I ran gobuster, which didn't find anything at all

![gobRep](./res/Scriptkiddie/gobRep.png)

After that I ran nikto, which found the wp-config, but whenever I tried to access it, I got redirected to the main page

![nikto](./res/Scriptkiddie/nikto.png)

So I continued by checking the source code, but there wasn't anything interesting as well

![source](./res/Scriptkiddie/source.png)

Since I saw that there was an option to do a post, I checked the headers with the options to confirm that and see if I could get any other information

![headers](./res/Scriptkiddie/headers.png)

So I started trying some command injections on the post requests, but they were controlled

![cmdInjectionFail](./res/Scriptkiddie/cmdInjectionFail.png)

Then I was playing with payloads post, when I saw that it generates an exectutable at /static/payloads endpoint, which could be interesting

![staticPayload](./res/Scriptkiddie/staticPayload.png)

## Exploitation

I googled for ways to exploit msfvenom, when I found [this post](https://www.rapid7.com/db/modules/exploit/unix/fileformat/metasploit_msfvenom_apk_template_cmd_injection/), so I tried to generate a payload with it, and apparently it is connecting to my netcat but not giving a shell

![msfApk](./res/Scriptkiddie/msfApk.png)

So I tried with msf multi/handler, and I got a meterpreter shell back

![shell](./res/Scriptkiddie/shell.png)

## Post Exploitation

So I started the enumeration by pulling the os information

![osInfo](./res/Scriptkiddie/osInfo.png)

Then I checked what was on the folder that we spawned, which was the app code, I grabbed it to understand how it works deeply, even though we probably won't need it anymore

![appPy](./res/Scriptkiddie/appPy.png)

After that I checked the etc/passwd to see which other users were available, which apart from root there was only pwn

![etcPass](./res/Scriptkiddie/etcPass.png)

Then I cheked the environment variables, which have some references to metasploit, as expected, and some others to ruby

![env](./res/Scriptkiddie/env.png)

After that I checked the network info, which didn't have anything weird

![netInfo](./res/Scriptkiddie/netInfo.png)

And then the SUID binaries, which also didn't have anything juicy

![suid](./res/Scriptkiddie/suid.png)

After that I went to explore a little bit the files at the home folder, and since I was there I grabbed the user flag

![userFlag](./res/Scriptkiddie/userFlag.png)

Then I ran the local exploit suggester

![localExploitSuggester](./res/Scriptkiddie/localExploitSuggester.png)

And after some tries of the ones that said target vulnerable, I eventually got an elevated shell with the pwnkit one

![elevatedShell](./res/Scriptkiddie/elevatedShell.png)

Then all I had to do is grab the root flag

![rootFlag](./res/Scriptkiddie/rootFlag.png)

## After Work

After that I checked the write-up to see which was the intended way to solve this box, and for the first part we did the same, but for the escalation, we should have done a lateral movement into pwn account first, then use it's sudo privileges to escalate, so I decided to reproduce it just for learning purposes, first, I secured ssh access to kid account to make it more comfortable

![ssh](./res/Scriptkiddie/ssh.png)

Then I executed the command to find all readable files from pwn home folder, where we find the scanlosers script

![findReadable](./res/Scriptkiddie/findReadable.png)

If we inspect the script, we see that it is parsing the information from logs/hackers, doing nmap scans with all ips found and then emptying the log file

![scanlosers](./res/Scriptkiddie/scanlosers.png)

So according to the write-up we have to options here, send an ip with command injection from the website, or since we already have ssh access, add the command injection directly to the file, which is the one we're going to do, and for some reason, it didn't get executed with cat, so we have to add it with 2 spaces before it so it gets executed properly

![pwnShell](./res/Scriptkiddie/pwnShell.png)

Then we can see that we are able to execute metasploit as root

![msf](./res/Scriptkiddie/msf.png)

And once we've done that we only have to get a ruby shell and get another bash shell as root

![ruby](./res/Scriptkiddie/ruby.png)
