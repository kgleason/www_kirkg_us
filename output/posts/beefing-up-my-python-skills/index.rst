.. title: Beefing up my python skills
.. slug: beefing-up-my-python-skills
.. date: 2013-12-20 15:07:56 UTC-05:00
.. tags:
.. link:
.. description:
.. type: text

I've got an idea for something that I want to write, but I'm going to keep it to
myself while I work it all out. It will involve using Twilio_. I'm not a
programmer, and I'm by no means a Python expert. I've written one thing in
Python so far (a bot for the now defunct turntable.fm). I'll probably keep this
next project in a private github repo until I get it done.

.. _Twilio: http://www.twilio.com

In any case, I wanted to learn how to use Twilio, and beef up on my Python skills
at the same time. Some of what follows may be just because I am a relative
neophyte, and if so, I apologize. Also, I'm mostly writing this in response
to a tweet_ from `the Twilio team`_. It seemed like it was going to be long for an e-mail,
and I wanted to have a copy for posterities sake. If it isn't obvious, all of
the code you'll see below is taken from Twilio's tutorials, and modified slightly
by me. I think I've linked everything pretty well. (Of course if Twilio makes
some adjustments, then this article might not make a lot of sense in the future.)

.. _tweet: https://twitter.com/twilio/status/414140751941869569
.. _the Twilio team:  https://twitter.com/twilio

.. TEASER_END

Without further ado….

I started at the beginning_ and went through the `environmental setup`_ with
relative ease. I did have to fix my Homebrew, which was kinda messed up, but
that's my fault for not maintaining it. After reading everything, I was excited
to make my first call. Once I had verified my number, I fired it off, and it
almost worked.  I did have to change line 13 of the make_call.py from

.. _beginning: https://www.twilio.com/docs/quickstart/python/rest/initiating-calls
.. _environmental setup: https://www.twilio.com/docs/quickstart/python/devenvironment
.. _make my first call: https://www.twilio.com/docs/quickstart/python/rest/call-request

.. code-block:: python

    print call.sid

to

.. code-block:: python

    print(call.sid)

I knew I would hit a few things like that using python3 as I was. Surprisingly,
that was the only one of those.

Once I had the first call out of the way, I was able to `grab the log`_ with ease.
Things started to get more interesting with the `Hello Monkey web client`_. Getting
the basic client up and running was smooth, and so was adding in the ability to
`hang up from the browser`_.

.. _grab the log: https://www.twilio.com/docs/quickstart/python/rest/call-log
.. _Hello Monkey web client: https://www.twilio.com/docs/quickstart/python/client/hello-monkey
.. _hang up from the browser: https://www.twilio.com/docs/quickstart/python/client/hangup

I did get a little stumped when I was working on `receiving incoming calls`_,
mostly by this sentence: "Give the browser client a name and `register` it with
Twilio." I probably spent 20 minutes looking through every nook and cranny of my
Twilio account, trying to find out where I registered a browser client name.  I
finally shrugged it off, and moved on, only later to realize that it meant that
the browser was going to register itself as a client with Twilio using a name
that I specified.  Other than that I was receiving IB calls like a champ.

.. _receiving incoming calls: https://www.twilio.com/docs/quickstart/python/client/incoming-calls

As I was working on `outgoing calls`_, I realized that I needed to examine the
provided python code line by line, since not all of the changes were highlighted
correctly.  An example is in run.py, line 5. The Python 're' module wasn't needed
up to this point, and I knew what the issue was right away when Flask choked on
the re.search() on line 23. It was probably a good thing that it happened with
something easy to track down.  Quick fix, and I was back up and running, now able
to make outbound calls, and I moved on to the `browser to browser`_ calling.

.. _outgoing calls: https://www.twilio.com/docs/quickstart/python/client/outgoing-calls
.. _browser to browser: https://www.twilio.com/docs/quickstart/python/client/browser-to-browser-calls

This time I noticed quickly that

.. code-block:: python

    import re

was missing even though

.. code-block:: python

    re.search()

was still used on line 21 of run.py.

At this point, I should point out that I was using an awesome combination of
Ngrok_ and Runscope_ to watch my traffic. I was (and still am) admittedly confused
by the choice of the name for the 'from_number' variable. The value is pulled
from the 'PhoneNumber' value in the request, and it certainly seems to me to be
the destination number of the call, and not the originating number (which is
what I would have expected with the name it was given). I kind of shrugged off
the seemingly contradictory naming, and tried my browser to browser calling.
But it would never work. No matter what I did, it seemed as if I was always
trying to call my own client.

.. _Ngrok: http://ngrok.com
.. _Runscope: http://runscope.com

After the code blocks in the lesson, you see where it says,

::

    Let's look at what's actually going on after you enter 'tommy' and press 'Call'

This led me to believe that they were expecting me to be initiating the call
from the 'jenny' client.  If you look at lines 21 - 24:

.. code-block:: python


    if from_number and re.search('^[\\d\\(\\)\\- \\+]+$', from_number):
        r.number(from_number)
    else:
        r.client(default_client)


we see that if the from_number (which is the client that we are trying to call)
does not look like a phone number, then we call the 'default_client' which is
set in line 11 to have a value of 'jenny'. So if I am dialing 'tommy' from the
'jenny' client, what happens is that 'jenny' simply tries to call itself. And
sure enough, if I tried to call any named client from the client named 'tommy',
I ended up opening a connection to 'jenny'.

I could see in line 32 of run.py that I could get the name of the destination
client from the request, so I tried to use that in my voice route. It looked
a little something like this:

.. code-block:: python

    # If we have a number, and it looks like a phone number:
    if from_number and re.search('^[\\d\\(\\)\\- \\+]+$', from_number):
        r.number(from_number)
    else:
        client_name = request.values.get('From',None)
        r.client(client_name)


It had been a few hours since I had looked at it, and I kept getting hung up on
the variable names. If from_number was my ANI (in traditional telephony terms),
then I needed to the get the client name to set my DNIS (in traditional telephony
terms). The above solution got me closer to where I thought I needed to be, but
I kept getting a response that looked like this:

.. code-block:: xml

    <?xml version=\"1.0\" encoding=\"UTF-8\"?>
    <Response>
      <Dial callerId=\"+12125551234\">
        <Client>client:tommy</Client>
      </Dial>
    </Response>


and that `client` value was not flying. I tried a couple of clever ways to get
the 'tommy' portion out of 'client:tommy', like casting the whole thing as a
list, or a dictionary, but none of it worked. In the end, I just hit it with a hammer:

.. code-block:: python
    :number-lines:

    # If we have a number, and it looks like a phone number:
    if from_number and re.search('^[\\d\\(\\)\\- \\+]+$', from_number):
        r.number(from_number)
    else:
        client_name = re.sub('client:','',request.values.get('From',None))
        r.client(client_name)


I was finally getting back the response that I wanted to see in Runscope, but
it finally dawned on me that it is all backwards. The entire time, I thought
I should be seeing the name of MY client in Runscope, when in fact, I wanted to
be seeing the name of the client that I was CALLING. *facepalm*

In the end, what I ended up with looks like this:

.. code-block:: python
    :number-lines:

    @app.route('/voice', methods=['GET', 'POST'])
    def voice():
        dest_number = request.values.get('PhoneNumber', None)

        resp = twilio.twiml.Response()

        with resp.dial(callerId=caller_id) as r:

            # If we have a number, and it looks like a phone number:
            if dest_number and re.search('^[\\d\\(\\)\\- \\+]+$', from_number):
                r.number(dest_number)
            else:
                r.client(dest_number)

        return str(resp)

I changed the name of the variable to dest_number so that I would stop confusing
myself, and I use that value in both the if and the else -- only the method is
different -- number() for numeric phone numbers and client() for named SIP clients.

Finally things seemed to be working the way I expected that they would. I added
in the `presence detection`_ and sent the ngrok tunnel address to everyone at
work, so that they could all bask in my ability to follow a step-by-step
tutorial on a web site.

.. _presence detection: https://www.twilio.com/docs/quickstart/python/client/displaying-availability

It's been fun, and I'm kind of glad that it wasn't 100% perfect, cause I gave
me the chance to play with Runscope and debug an issue using it. I do think that
if that variables had been named a bit more logically, that I probably wouldn't
have gone down the rabbit hole of trying to get the client value from the
request, and probably would have saved myself 45 minutes of head scratching.

I have to admit that I am curious to see if Twilio has a reason for naming that
variable the way that it is.
