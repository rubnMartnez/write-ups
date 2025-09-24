# Tabby

This is my write-up for the machine **Tabby** on Hack The Box located at: https://app.hackthebox.com/machines/259

## Enumeration

First I started with an [nmap scan](./res/Tabby/10_10_10_194_nmapReport.txt), which shows the following

![nmapScan](./res/Tabby/nmapScan.png)

Since port 80 was open I navigated there to see what were we up against, and the following page is displayed

![defPage](./res/Tabby/defPage.png)

Then as usual, I checked wappalyzer for the tech stack, which didn't show much, apart from the apache version, which we already knew from nmap

![wap](./res/Tabby/wap.png)

Then I ran gobuster, which found some endpoint, probably all of them are accessible with normal website usage, but it's worth checking

![gob](./res/Tabby/gob.png)

And I also ran nikto, which didn't found anything interesting

![nikto](./res/Tabby/nikto.png)

So, before digging deeper on port 80 and start checking the source code, requests, etc... I wanted to check port 8080, which has a default page that displays some interesting information

![8080defPage](./res/Tabby/8080defPage.png)

If we follow some of the links there we can see the tomcat version, which is 9.0.31

![docs](./res/Tabby/docs.png)

And some other interesting things like jsp examples and a manager login

![8080endpoints](./res/Tabby/8080endpoints.png)

So I decided to run gobuster against it

![gob8080](./res/Tabby/gob8080.png)

Along with nikto, in order to get as much information as possible before start trying to find vulnerabilities, and actually nikto found some interesting things for us

![nikto8080](./res/Tabby/nikto8080.png)

So first I checked the snoop file, since it was an information disclosure, but in that case it didn't give too much information

![snoop](./res/Tabby/snoop.png)

I also tried some default credentials for the manager login page, but they didn't work

![defCredsF](./res/Tabby/defCredsF.png)

Then I tried doing a put and a post, since nikto said it was allowed, but they didn't work

![putNotAllowed](./res/Tabby/putNotAllowed.png)

After that I decided to google for some exploits on this tomcat version, but since I didn't found anything good, I got back to port 80 to enumerate it further and check if I could get some valuable information from there. First I  checked the endpoints found by gobuster which mostly were forbidden apart from the readme and the news.php, which didn't have much

![news](./res/Tabby/news.png)

But then when I started clicking around the website, I saw that news were actually redirecting to megahosting.htb/news, after adding this domain, we could see a page where they are talking about a data breach

![news2](./res/Tabby/news2.png)

## Exploitation

Since I saw that there was a parameter on the url, I tried LFI, and it worked

![lfi](./res/Tabby/lfi.png)

Then I tried to get the files that were listed on port 8080 default page, but nothing was returned

![tomcatUsersFail](./res/Tabby/tomcatUsersFail.png)

So I tried downloading the running gz which should contain some other documentation

![gz](./res/Tabby/gz.png)

Inside there they talk about the setenv.sh script which is the one that sets up the CATALINA variables

![running](./res/Tabby/running.png)

But I also tried with on those paths, and nothing was returned

![setenvFail](./res/Tabby/setenvFail.png)

So I went back to the documentation, where I saw that a daemon.sh script should be located on catalina home, and this one was actually accessible, which confirmed the CATALINA_HOME path

![daemonSh](./res/Tabby/daemonSh.png)

But after checking the script I didn't see anything about the users xml file, so I got back to the documentation, and I tried all the path that I found there, but none of them worked

![tomcatConfUsersFail](./res/Tabby/tomcatConfUsersFail.png)

So, I checked the write-up to see what I was missing, and apparently the users xml is under usr/share/tomcat9/etc/tomcat-users.xml, which apparently you can discover by googling "/usr/share/tomcat9 directory" but for me it wasn't the case, cause the same paths that we checked before kept appearing, but anyway, with that we are able to get the users.xml which gave us the credentials **tomcat:$3cureP4s5w0rd123!**

![tomcatUsers](./res/Tabby/tomcatUsers.png)

With that we can access the host-manager site

![hostMan](./res/Tabby/hostMan.png)

Now the problem is that in order to add a reverse shell, we need access to the manager site, and with the current user we can only access the host-manager. I checked the documentation again to see if there was a way to add that role remotely or something, when I saw that there's an endpoint that let us execute commands, and even though I got an error, it wasn't a forbidden, which tell us it's working

![deployVer](./res/Tabby/deployVer.png)

I also used burpsuite to make sure that put is allowed

![putCheck](./res/Tabby/putCheck.png)

Then after some tries I got the command working, since we got back that the app has been deployed, though it failed to start

![deploymentFail](./res/Tabby/deploymentFail.png)

So I read the documentation and I saw that the context.xml was needed for the deployment, so I've pulled it, and attached it to the msfvenom payload as a template, but I still got the same error

![templateFail](./res/Tabby/templateFail.png)

After some googling and some tries, I finally got it right

![curl](./res/Tabby/curl.png)

And with that we got our reverse shell back

![shell](./res/Tabby/shell.png)

## Post Exploitation

So now we can start our escalation enumeration as usual

![env](./res/Tabby/env.png)

After that I pulled the os information, along with the user groups

![id](./res/Tabby/id.png)

Then I checked the SUIDs, but as usual there wasn't anything interesting there

![suids](./res/Tabby/suids.png)

After that I checked the crontab, but there wasn't anything as well

![crontab](./res/Tabby/crontab.png)

Neither on the home folder, and ash home folder wasn't accessible

![homeFiles](./res/Tabby/homeFiles.png)

So I navigated around for a bit, when I found a backup file that seemed interesting

![bak](./res/Tabby/bak.png)

I proceeded to tranfer it to my kali machine, in order to inspect it more comfortably

![transferBak](./res/Tabby/transferBak.png)

But unfortunately it was encrypted

![bakEncrypted](./res/Tabby/bakEncrypted.png)

So I had to get the hash with john the ripper

![zip2john](./res/Tabby/zip2john.png)

And crack it

![john](./res/Tabby/john.png)

Then I started checking it's contents, which apparently are the same as we find on the html directory accessible right now, but then I remembered that on news.php there was some kind of data breach mentioned, so I tried reading it and executing it to see if I got some information out of it, but nothing came out

![newsPhp](./res/Tabby/newsPhp.png)

After some time trying to figure out what to do with news.php, I thought that maybe that was a case of password reuse, so I tried to access ash account, and it worked

![ashShell](./res/Tabby/ashShell.png)

Then I grabbed the user flag

![userFlag](./res/Tabby/userFlag.png)

And after that I did some more enumeration to continue escalating privileges, starting with sudo -l and id to check the groups, and even though it wasn't possible to run sudo -l, ash user was on some interesting groups, like adm

![sudoL](./res/Tabby/sudoL.png)

So I ran linpeas to check for vulnerable files and so on, and it highlighted lxd, so I'll start by checking how to escalate with that

![lxd](./res/Tabby/lxd.png)

It has also found the files readable with adm group

![admFiles](./res/Tabby/admFiles.png)

But before digging into adm and trying to find another ways, I wanted to explore lxd, and with some googling I found [this blog](https://morgan-bin-bash.gitbook.io/linux-privilege-escalation/lxc-lxd-linux-container-daemon-privilege-escalation) which explains the escalation process step by step really well, so I started by checking the image list, which of course was empty

![imageList](./res/Tabby/imageList.png)

So I proceeded to follow the steps and download the alpine image, as explained in the blog

![downloadAlpine](./res/Tabby/downloadAlpine.png)

After that I downloaded the image on the target and tried to create the container, but I got the error of no storage pool found

![importImage](./res/Tabby/importImage.png)

So I had to follow the steps to create the storage pool, and then I was able to create the container

![createPool](./res/Tabby/createPool.png)

And with that I was able to follow the other steps, and get an elevated shell

![elevatedShell](./res/Tabby/elevatedShell.png)

Then all I had to do is retrieve the root flag

![rootFlag](./res/Tabby/rootFlag.png)
