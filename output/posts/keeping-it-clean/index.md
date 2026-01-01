<!--
.. title: Keeping it clean
.. slug: keeping-it-clean
.. date: 2013-10-25 14:04:00 UTC-05:00
.. tags:
.. link:
.. description:
.. type: text
-->

We've got a friend, a friend who is having a problem. It's a problem that a lot of people probably have, but most probably don't know about it.

There is some conventional wisdom out there that would have everyone believe that the younger generations are inherently better at protecting themselves online than the older generations. The logic goes that since these younger people have grown up with computers, they are inherently more savvy. My work experience tells me that these people tend to be larger PITAs. They feel as if they are owed a computer that functions perfectly all of the time. Of course, since they've been told that they are naturally better with the tool that they have been provided since it's always been a part of their life.

Well in the same way that new college grads are the tech gurus that they think they are, your kids don't know how to protect themselves on the internet. They can protect themselves from the threats online about as well as they can protect themselves from a marauding horde of visigoths wreaking havoc in the mall. And it gets even worse if they don't want to protect themselves.

<!-- TEASER_END -->

So it's up to us, as parents, to lay down the law and be good stewards of our networks at home.

I know that someone out there is asking themselves, "Network? I don't have a network." If you have more than one computer, and if you have a router (wireless or otherwise), then you have a network, and it is your responsibility to make sure that it is used appropriately.

That sounds sort of preachy and judgmental. It is intended to be preachy, but I'm not here to judge anyone. Given what I do for a living, I'm in a bit of a better situation to help people out with all of this. I have helped some people here and there, but the thing that our friend is dealing with has caused me to pause. This article is my effort to help spread the word about what you can do to help protect your kids from themselves, and from the generally crapiness on the inter webs. Keep in mind that the best solution is to keep them off of the internet, but that is hardly feasible these days. Even with what I am going to suggest below, there's no replacement for a load of common sense and a vigilant eye.

So without further ado ...

Start out by going to [Open DNS](https://kirkg.us/X3u1PD)and create yourself an account. When you get into the Open DNS stuff, you will need to make some decisions. It will ask you early on to create and label your network. It will detect your settings, and it will most likely be correct. Make sure that you do this step from the network that you want to protect -- not from the LTE connection on your mobile phone or anything like that. At some point it will present you with an option for a level of locked-downedness.  I can tell you that you will not be happy with the highest level of security. Medium, low, or custom is what you will want, depending upon your goals.

Once the account is set up, you should be able to find directions about how to start using your new account. It will involve [reconfiguring your router](https://store.opendns.com/setup/router/).

In order to use this, you will need to make some changes to your router. There's no way around it.  It can be sort of intimidating if you don't know what you are doing, but it is a necessary step. I'll try to explain why this is important.

In essence, the internet works a lot like your mobile phone. When you need to contact someone, you look them up in your address book. The address book contains the mapping of easy to remember names to numbers where they can be reached. The internet works (at a very high level) the same way. When you try to go to a website, your computer automatically looks up the easy-to-remember name (let's say www.gleasons.info) to find out the number where the site lives (in this case  98.223.196.26). That number that identifies the site is called an IP address, and the system to look them up is called DNS.

It is possible to browse directly to some sites by going directly to their IP address, but the number of IP addresses that someone would have to memorize in order to do what they would need to do on the internet in an average day would be astronomical. Open DNS capitalizes on this fact, and leverages it to your advantage. They essentially limit the number of phone numbers that are in the address book where you look names up. If you look up a number for a name that you shouldn't be, it will tell you, "Sorry. I can't give you that number."

After you configure your Open DNS account, you need to reconfigure your router to do a couple of things. The first is you need to tell your router to use the Open DNS servers to find the IP addresses of the sites that you are trying to get to. The second, and this may or may not be required depending upon your router, will be to configure your router to tell the computers on your network to use the Open DNS servers. Once you finish all of these steps, I'd recommend that you reboot your computer, and try going to a website that should be blocked. If you can come up with one, then try this [test site that I think is provided by Open DNS](http://www.internetbadguys.com). (that site shouldn't be anything dirty)

If it works, congrats. You've taken the first step in helping keep stuff you don't want off of your network. Unfortunately, this first step is probably the easiest, because it should be one and done. The next step, which we'll cover next time, is locking things down.

I'd like to ask for people to post questions to the comments below. I know that Facebook may seem easier, but if you do it here, then it is more permanent and other people will gain some advantage from your questions (and hopefully provided answers).

*Update 10/28/2013*

I had the wrong URL above for the Open DNS account creation. It has been fixed.
