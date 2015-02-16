.. title: Step by step guide to setting up Windows to work with BitBucket and SSH
.. slug: step-by-step-guide-to-setting-up-windows-to-work-with-bitbucket-and-ssh
.. date: 2014-01-20 14:41:46 UTC-05:00
.. tags:
.. link:
.. description:
.. type: text

So at work we recently migrated from SVN to Git, and we chose BitBucket as our
git host. Some tutorials were written internally about how to get started using
git, but since all of the developers have Macs, and I am a Mac user, we wrote
the tutorial assuming OS X. It was mostly designed to get used to some of the
different concepts of DVCS versus the old Subversion model, and not at all an in
depth look at git.

.. TEASER_END

If you've used git at all, you know that it is really easy to use in OS X or in
Linux. However Windows hasn't been such a smooth story. And finding a good tutorial
about getting it all set up isn't really all that easy. To that end, this article is
designed to get you up and running using BitBucket and SSH in windows. This
article is probably not going to be the best for advanced users. If you know how
to create ssh-keys in windows, or already have a functioning Git client running in
Windows, then you probably won't get much out of this. Of course, feedback is
always appreciated, as I am by no means an expert.

In the end, you'll have a functioning install of Git in windows, that will use
SSH to communicate with BitBucket. It should work for most other Git
implementations that support SSH as well. I'll be using a preview of Windows 8.1
(with Smart8 installed), but the steps should be pretty similar in Windows 7 or
newer. If you are using something older than Windows 7, then my advice to you is
to get with it and upgrade already. It's worth it.

Chocolatey
===========
I'm starting with a brand new windows installation. Regardless of what your
situation is, I'd recommend that you begin by installing all of your updates,
unless you have a damned good reason for not installing them. It might take some
time, but it's OK. I'll wait.

Now that you're back, you'll want to install Choclatey_. In fact, then next time
you install windows, you may just want to start with this. If you've ever used
HomeBrew_ in OS X, then you'll probably like Chocolatey. (If you haven't used
homebrew and you are a Mac user, then what are you waiting for? Do it. Do it.)
It is a basic package manager for Windows.

.. _Choclatey: http://www.choclatey.org
.. _HomeBrew: http://brew.sh

It's dead simple to install. Copy the command on the front page of the website I
linked to up there, and paste it into a cmd window or a Run box. It'll do some
stuff, and then it'll be done.  Once it is done, open a new cmd window in order
to get all of the new environmental stuff to refresh.

Install git
=============
Once choclatey is installed, then all you need to do to install git is this:

.. code-block:: text

    c:\Users\kirk\> cinst git

Yep, that's it. Your UAC will probably prompt you about the installation, but
once you say OK, Choclatey will finish it's thing, and you should have a fresh
install of git.

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_7_19_01_PM.png
    :align: center

|

Now that git is installed, close that cmd window, and open a new one. We'll use
that new one to run a quick test. Run these commands in the same cmd window:

.. code-block:: bash

    C:\Users\kirk> mkdir git-test
    C:\Users\kirk> cd git-test
    C:\Users\kirk\git-test> git init


If the output says that git is an unrecognized command (and it might), then we
need to update your path. If you didn't get an error, then do `cd .git`. If that
works, then you have a .git directory, & you are golden. Skip the next section
(Setting up SSH to work with Git), and feel free to delete that git-test directory.

Fixing your path so that git works better
-------------------------------------------
If you got an error above, then we need to adjust your path so that you can type
*git* without having to specify a full path.  Start by going to Control Panel ->
System and Security -> System. On the left hand side choose "Advanced System
Settings".  Click on the "Environment Variables" button.  In the user variables
section, select the \"Path variable\" and choose the edit button.  You need to
add the location of the git executables onto the end of the path. By default,
choclatey will install it in *C:\Program Files (x86)\Git\cmd*. Once you are done,
you should see something like this:

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_7_34_14_PM.png
    :align: center

|

Click OK 3 times, and close your cmd window. Open a new one and re-run that test
from above. It should work.

Setting up SSH to work with Git
=================================

I'm not going to get into why you might want to use SSH with git. I'm just going
to assume that you do. Seriously, why wouldn't you?

Inside your start menu, you should have an item for Git. Inside there you should
also find git-bash. Run that bad boy.  Once you have a prompt (a friendly looking
$ prompt, straight out of war games), run *ssh-keygen.exe*. This step is going to
generate a public and private key pair. It's going to ask some fairly important
questions, but I'll walk you through them.

In the image below, it is asking where you want to save they key pair. If you
know what you are doing, then you can save it somewhere other than in the default
installation. Given that you are reading this article, you probably don't know
what you are doing, so choose the default by hitting enter.

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_8_46_55_PM.png
    :align: center

|

In the next picture, you'll see that you are being prompted for a passphrase.
This is a passphrase that is used to unlock your keychain. It should not be your
windows password, your git password, or any other password that you use.  Make
it something long and memorable. By all means, don't make it "I'd really love
to get some purple footy pajamas for Valentine's day." But make it something like
that. Random is good. Funny is probably more likely to be memorable. Whatever you
come up with, you'll need to enter it 2x.

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_8_48_22_PM.png
    :align: center

|

Once you've successfully entered your passphrase, it'll spit out some stuff. Not
terribly important really. Not for what we are doing here.

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_8_50_35_PM.png
    :align: center

|

This process generated 2 files: *id_dsa* and *id_dsa.pub*:

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_8_58_48_PM.png
    :align: center

|

The file named id_rsa.pub will heretofore be known as your public key. The file
named id_rsa will be referred to as your secret key. Your secret key should be
protected. Don't email it around, don't post it on Facebook, don't put it into a
Gist on github. Anyone who has that secret key and your passphrase (you DID
create a passphrase, right?) will be able to do stuff in git as you. And there
will be no way to prove that you aren't the one who ran

.. code-block:: bash

    for f in $.cs
    do
        tac ${f} > /tmp/${f}
        rm -f ${f}
        cp /tmp/${f} ${f}
    done

against your master branch. Protect it. Seriously.

Enter this command inside of git bash:

.. code-block:: bash

    cat .ssh/id_rsa.pub

Copy the output to your clipboard.

Adding your public key to Bit Bucket
======================================

Now that you have a public key, it is time to associate it with your account on
Bit Bucket. The steps are similar for GitHub. If you really want them written out
for GitHub, then post it in the comments. I'll get it done.

Start by logging into Bit Bucket. In the upper right, click on your picture and
choose Manage Account. There will be a section called SSH keys. Go there.

Click the blue Add a Key button. Name the key something that makes sense, and
paste the key into the big ole' text box:

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_9_07_32_PM.png
    :align: center

|

Hit the "Add Key" button, and put your web browser away for a few moments.

Configuring git
=================

Now that the key is in place, we need to give git a little information about you.
From here on out, run these commands in a git-bash window. You can thank me for
that later.

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_9_39_26_PM.png
    :align: center

|

As you may have guessed, the first command will tell git that your name is "Kirk
Gleason" and the second that your e-mail address is "kgleason at gmail dot com".
Since this probably isn't accurate for you, I'd recommend that you change those
values to represent what they should be for you. Set the e-mail address to be
one that BitBucket knows about for you … probably the one that you used to register.


Testing the ssh connection to BitBucket
-----------------------------------------

With that little config bit out of the way, we should be able to test our
connection to BitBucket. Inside git-bash type in the following command:

.. code-block:: bash

    ssh -T git@bitbucket.org

It will ask you to accept a key. This is the unique finger print for this
specific SSH server. If you typed the hostname correctly, you can say yes
(unless you have reason to suspect that something fraudulent is afoot). This will
add the fingerprint to a list of known servers, and won't prompt you for it again,
unless it changes. Next you should get a message about shell access being disabled.
This is normal. Hit enter to get back to your shell:

|

.. image:: ../../images/Screen_Shot_2014_01_20_at_9_52_17_PM.png
    :align: center

|

If that went as expected, then you have connected to the git server using SSH,
but you haven't really done anything useful with it yet.

Cloning your first repository
================================

If you have a repository to clone, the go for it. The command should look
something like this:

.. code-block:: bash

    git clone git@bitbucket.org:kgleason/dynamicdns_linode.git

If you don't have a repository that you can clone for testing, then feel free to
run that command. It is a public repo that has a script that I wrote to solve a
problem. The README is longer than the script, but hey! What do you want for
nothing? Of course you can't push changes back up, but you get the idea.

You did it!
==============

If it worked, then congrats. You have configured windows to work with BitBucket
via SSH. Any GUI tools that you may install that use the git executable that
chocolatey installed should automatically have access to your key. If you don't
believe me, then go to Start --> All Programs --> Git --> Git GUI and have a go.
It should work.

So there you have it. Next time out, I'll throw out some tidbits about pimping
out your git-bash setup, and how to stop getting prompted all the damned time
for your SSH passphrase.
