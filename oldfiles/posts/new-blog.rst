.. title: New Blog
.. slug: new-blog
.. date: 2014-03-09 22:27:48 UTC-05:00
.. tags:
.. link:
.. description:
.. type: text

A couple of weeks ago I started putting some thought into moving my blog away from
Wordpress. I don't necessarily have any problems with Wordpress, I was just
looking from something different, something simpler.

For the most part I don't think very much attention gets paid to what I write
here, but I write down a lot of things that I want to remember long term.
Wordpress was an easy way to get started, but it really was overkill for what I
end up doing here.


.. TEASER_END

I wanted something simpler, and since I have been playing in Python a decent
amount recently, I actually started writing a simple site in Python. What I have
right now is very basic, and not yet ready for prime time. I'm going to keep
poking at it until I get it the way that I want.

When I set out, I wanted the following things out of the box (no plugins, no
heavy modifications):

* Simple management interface. I don't need all of the bells and whistles of Wordpress. I want to be able to write an article, and get it published.
* Markdown editor. I had a plugin in WP that would let me write the articles using Markdown. I tried a couple of them in fact, but they always felt like the bolt-ons that the were. It never felt quite natural.
* Built in syntax highlighting. Again I had a plugin in WP that would do this, and it worked. But I always had to look up the syntax about how to use the thing. It was full of features -- more than I ever really needed in fact. None of the markdown editors that I tried support the GitHub code markdown. I really like that, so I wanted it.
* Simple site layout & style. It seemed like I was constantly playing with the themes in WP. Not because I liked playing, but because I never found a style that I liked. I just want soemthing simple. Seriously simple.


Those were really the main requirements. I've even got a couple of them
implemented in Python. In the middle of writing my blogging platform, I was
also still working on a large article (that I still haven't completed). The
thought of finishing it in Wordpress was just sucking up any joy that I might get
from writing an article (and I do enjoy it quite a bit). So I was splitting my
rare free time between writing my own blogging site and writing an article on a
platform that I never really *loved* using.

I was researching markdown editors that I could implement in Python when I
tumbled upon Ghost_. As I started looking through it, it pretty much had all of
the requirements that I had written down for my Python site. Only it is written
in NodeJS. (I recently told someone at work that I would pass on a Node training
session, saying \"I don't think I can handle learning another language halfway.\"
Figures.)

.. _Ghost: http://ghost.org

I played around with it a little bit, and it really like it. It is easy to look
at, has a real time preview, so I can see what the final output will look like.
And it took a single line change to implement the GutHib style code markdown
blocks. Awesome.

During the playing phase, I was looking at options for comments. The old site
never had a single comment, but I think I'd rather give people the option.
There were 2 options: Disqus_ www.disqus.com and Discourse_. I have to admit
that Discourse appealed to me -- a lot. But in the end I went with Disqus. It
really came down to the level of complexity that Discourse entailed by their
required used of Docker_.

.. _Disqus: http://www.disqus.com
.. _Discourse: http://www.discourse.org
.. _Docker: http://www.docker.io

I think that Docker is an amazing concept. I really like the idea of it. But
after 2 days, and 2 different VPSs, I couldn't figure out how to control it
without rebooting the entire VPS. None of the docker control commands seemed to
work. Definitely something to keep playing with, especially since `Digital Ocean`
offers a VPS image that I can poke around with for `less than a penny per hour`_.

.. _Digital Ocean: https://www.digitalocean.com/?refcode=18b80ab28634
.. _`less than a penny per hour`: https://www.digitalocean.com/pricing/?refcode=18b80ab28634

In the end, Disqus was a matter of modifying a couple of code files. If I need
to fix anything, I can restart ghost, and the disqus stuff should be fixed. I
will keep looking at Discourse, and once I get a chance to figure out how docker
works, I may give it another go.

So here we are. I'm in the process of updating the old articles -- in particular
the images, which are still pulling from the old site.

You may have also noticed that I'm using a new URL. The original site was
intended to be a family blog, but for the most part, I'm the only one who is
ever interested in writing on it. So I'm going to temporarily retire the family
blog, and convert it into something that is just mine. If/when the family is
ever interested in getting their thoughts online outside of Facebook, then I'll
put something back up for them.

Until then, I'm going to continue to use Ghost, and work on my site. I'm getting
to the point where I think I'm going to have to teach myself some CSS, so I
suspect that things will slow down.

If you do happen to be poking around, please feel free to drop a comment and let
me know what you think, or if you find any broken links.
