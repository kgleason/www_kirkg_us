<!--
.. title: Giving up the Ghost
.. slug: giving-up-the-ghost
.. date: 2015-01-10 11:34:43 UTC-05:00
.. tags: Nikola, Ghost
.. link:
.. description: Ditching Ghost
.. type: text
-->

A while back, I dropped [Wordpress](http://www.wordpress.org) as my blogging platform in favor of [Ghost](http://www.ghost.org). At the time I was looking for something simpler
to manage than Wordpress, and something new to play with. Ghost seemed like a pretty good candidate -- it is still kind of the new hotness. Node.js seemed like a potential
interesting new thing to learn. So I went for it.

<!-- TEASER_END -->

I should temper everything I'm about to say with the caveat that all of my complaints about Ghost are 100% my issues. I'm sure that for someone versed in Node.js it is
perfectly stable. I'm sure that for someone using a hosted Ghost instance, it is a pleasure to use. As a guy who (as it turns out) is not terribly interested in Node.js and
who wants to host my own blog, Ghost didn't work for me. Not being a Node guy, I don't have the first clue about how to troubleshoot it when it crashes -- and it crashes on
me a lot. I don't even really know how to check the logs for it. I followed the installation instructions on the site as close as I could and I'm running a fairly stock
Ubuntu 14.04 installation at [Digital Ocean](https://www.digitalocean.com/?refcode=18b80ab28634). I haven't done a great job at keeping track, but I know that it hasn't
made it a month without a crash -- and this is a site that no one actually ever visits.

## Tesla was the man ....

Listening to a podcast one day (either [Linux Action Show](http://www.jupiterbroadcasting.com/show/linuxactionshow/) or [Linux Unplugged](http://www.jupiterbroadcasting.com/show/linuxun/))
I heard one of the guys in the mumble room mention that they use [Nikola](http://www.getnikola.com) for the [Ubuntu Mate](http://www.ubuntu-mate.org) site. As he was
describing it, it sounded like it was running about my speed. I really like the idea of running a static site again -- easy to keep running, easy to troubleshoot.

To that end, this is my first post with Nikola. I plan to start using it right away. I do have a fair amount of content still in ghost, but I have all of the exported to a
giant JSON file full of markdown. Since I wrote a lot of it for work (I used those articles to document a complex problem), I want to make sure I keep it around.

My plan is to migrate the old articles one by one in the reverse order that I wrote them in. If you are reading this and looking for something, let me start with a hearty thanks!
Drop me an e-mail and I will bump your request up in the queue. I'm going to shoot for doing about 2 a month, and I hope to be able to add new articles at about the same rate.
