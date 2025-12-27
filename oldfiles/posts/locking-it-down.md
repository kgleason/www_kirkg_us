<!--
.. title: Locking It Down
.. slug: locking-it-down
.. date: 2013-10-28 14:17:04 UTC-05:00
.. tags:
.. link:
.. description:
.. type: text
-->

In my [previous post](/posts/keeping-it-clean) about keeping unsavory things off of your network, I made an analogy between DNS and the Contacts database on your mobile phone. As I was explaining this to someone the other day, I used the analogy of a phone book. I pointed out that back in the day, if my parents didn't want a phone number to be accessible, then they could have blacked it out of the phone book with a marker. Such an act would have effectively made that number impossible to find. And that is essentially what Open DNS will do for you.

<!-- TEASER_END -->

However, there are some weaknesses with this methodology. Looming at a different phone book is a way around it. Or just waiting until the new phone book arrives each year. And the same goes for configuring your router to use OpenDNS. Someone with admin access to your computer can change the DNS that your computer uses, and open everything back up. Or they could hold down the factory default button on the router, which would cause the router to ask your ISP which DNS server it should use.

You are probably thinking that maybe I shouldn't have written that out -- spelled out a way for your kids to get around the filters you put in place. Maybe I shouldn't have. But at the very least it will keep you honest. Your kids should not be administrators on your computers at home. They probably shouldn't even be administrators on computers that you buy specifically for them. There are lots of reasons for this, and I hopefully just gave you another one. Putting in filters in place and then giving them admin access is kind of like telling them not to drive your car, and then putting the keys under their pillow. All they have to do is look, and the temptation is there.

If you are serious about protecting yourself & your kids as well as teaching your kids good computing habits, do the following things, right now:

  * Set up an account for you, your spouse, and your kids. Ideally everyone who uses the computer should have a separate account, and only you and your wife should have administrative access. If that's too much, then make an account for the old people to share (with admin access) and an account for the kids to share (without admin access).
  * Move your router to someplace where it is hard to get to. If it is sitting next to the TV, then resetting it is easy.
  * Put a password on your wifi.

As with all things, setting a good example is the best way to encourage proper behavior. Aside from the above, there are some general best practices that you & your kids should do:

  * Change your passwords. Right now. I'm sure it's been too long (72 days for me right now -- about time to do it again).
  * Continue to change your passwords. At least 2x per year. 4x would be better. Do this for your laptop, your phone, your email account, your Facebook account, your bank account. If you log into something frequently, then you should change the password frequently.
  * Turn on multi-factor authentication. I might have to write an entire article about this. Not sure. I'll explain more below.
  * Set your phone to auto lock. 10 minutes or less. 5 would be better. (You'll get better battery life as well).
  * Set your computers, all of them, to have a screen saver come on after 10 minutes. 5 would be better.
  * Set the screen saver to require a password to unlock.

So the one in there that you probably have the most questions about are multi-factor authentication. You can do this with Gmail, Facebook, Dropbox, iTunes and lots of other services that you probably use. The reason that people don't like changing their passwords is that they don't like having to remember a new password -- mostly because they think that their password needs to be complicated. The merits of password complexity are somewhat debatable, but if you like simpler passwords, or don't like changing your password, then multi-factor authentication is great way to continue to be lazy, while getting some decent protection at the same time.

In order to explain how it works, I'll walk you through what happens when I log into my Gmail account. I log to gmail.com, and type in my username & password, just like normal. I get a new screen telling me that I need to enter a code to be able to log in. At this point there are a couple of things that can happen. The simplest way for this to work is for google to send you a text message with the code in it. I enter the code into the webs tie, and voilà, I'm logged into gmail. There is a box that I can check that tells google to remember the computer than I am on, so I don't have to go through this every single time. Any time I log in from an previously unknown browser, I have to have the 2nd code in order to get it. That code only lasts a few minutes, after which it is no longer valid. In essence, I could give you my password, and you could take it home, but you couldn't log into the gmail account unless you've also stolen my phone.

This means that Google requires my password and that the person logging in have access to my phone. So my password for Google hasn't changed in some time (over a year), but it is less important, since no one can log in without having my phone. Or being extremely lucky.
