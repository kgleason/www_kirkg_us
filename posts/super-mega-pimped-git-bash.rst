.. title: Super Mega-pimped Git-Bash
.. slug: super-mega-pimped-git-bash
.. date: 2014-01-21 19:50:05 UTC-05:00
.. tags:
.. category:
.. link:
.. description:
.. type: text

OK. Maybe that is a little over the top. Yesterday we went through and set up
some git goodness in Windows. But using it kind of sucks, so in this installation
we will work on making things a little bit nicer to use.

Now I have to admit, I'm not a windows guy, but I noticed right off that by
default the git-bash stuff was useful, but pretty spartan. Being the Mac user I
seem to have become, I expect things to be a little bit nicer.

.. TEASER_END

The first thing we are going to need is a respectable text editor.

Either one of these commands will get you something nicer than Notepad:

|

.. code-block:: bash

    cinst notepadplusplus
    cinst sublimetext2

|

You can certainly run both of those, but really you only need one of them.
I'll probably use Sublime Text 2.

Playing around with git-bash
=============================

I'm not entirely sure what you can do with this thing, but it's bash. Why google,
when we can just play? Right?

Open git-bash and type in this command:

|

.. code-block:: bash

    PS1="[\u@\h:\w]\$ "

|

If you typed it correctly, your prompt should change:

|

.. image:: /images/Screen_Shot_2014_01_21_at_8_57_36_PM.png
    :align: center

|

It's still simple, but it's already more useful since it now shows you what
directory you are in. So let's open up the text editor that we installed a few
moments ago, and create a file with some good stuff in it.

.bashrc
----------

Let's start by putting the following into the text editor.

|

.. code-block:: bash
    :number-lines:

    #Define some prompt colors
    RED="\[\033[0;31m\]"
    YELLOW="\[\033[0;33m\]"
    GREEN="\[\033[0;32m\]"
    CYAN="\[\033[1;36m\]"
    BLUE="\[\033[1;34m\]"

    # Set up the prompt to show what directory
    # we are in and if it is a working copy,
    # then show what branch is active
    PS1="[${RED}\t ${GREEN}\w ${YELLOW}\$(__git_ps1) ${GREEN}]\$ "

|

You can change out the colors as you want to. If you want to see what it will
look like, save it in your user folder (for me that is C:\Users\kirk) as .bashrc

Once you have it saved, then run this command in git-bash to make it take effect.

|

.. code-block:: bash

    source ~/.bashrc

|

You should see something like this (assuming that you kept the colors as I had them).

|

.. image:: /images/Screen_Shot_2014_01_21_at_10_13_05_PM.png
    :align: center

|

Aside
------

It has nothing to do with git at all, but if you want a little more color in your
life, then add these lines into that same file:

|

.. code-block:: bash
    :number-lines:

    LS_COLORS='di=1:fi=0:ln=31:pi=5:so=5:bd=5:cd=5:or=31:mi=0:ex=35:*.exe=90'
    export LS_COLORS
    alias ls='ls -F --color --show-control-chars'

|

When you run *ls* inside git-bash, you'll get some colors according to the file type.

Starting ssh-agent
===================

There's probably a bunch more that you can do with the .bashrc file. Google
around. The next thing I really want to fix is to be able to stop entering my
ssh passphrase over and over and over and over and over again. Even getting
through the previous article it was pretty frustrating how many times I had to
enter it.

Pop open a new tab in your text editor. Enter the following stuff.

|

.. code-block:: bash
    :number-lines:

    SSH_ENV="$HOME/.ssh/environment"

    function start_agent {
         echo "Initialising new SSH agent..."
         ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
         echo succeeded
         chmod 600 "${SSH_ENV}"
         . "${SSH_ENV}" > /dev/null
         ssh-add;
    }

    # Source SSH settings, if applicable

    if [ -f "${SSH_ENV}" ]; then
         . "${SSH_ENV}" > /dev/null
         #ps ${SSH_AGENT_PID} doesn't work under cywgin
         ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
             start_agent;
         }
    else
         start_agent;
    fi

|

There's a lot of stuff, but essentially, this will check to see if ssh-agent is
already running. If it is not, then it starts the process up. When ssh-agent
starts, it prompts you for your ssh passphrase. As long as it is running, then
you shouldn't have to enter your passphrase any more.

So save this file in your home directory, and name it .bash_profile

Wrapping it up
================

With that our of the way, all that's left to do is to save all of your files,
close git-bash, and restart it. It should prompt you to enter your passphrase.
Go ahead and do it. You should end up with a friendlier looking prompt.

In addition, I _think_, but have not confirmed, that any tools that use this
installation of git (git gui for example) will also be able to use the running
ssh-agent.

So in the end, we have a couple of new files, that look like this:

|

.bashrc
----------

.. code-block:: bash
    :number-lines:

    # ~/.bashrc
    function parse_git_branch {
      ref=$(git symbolic-ref HEAD 2> /dev/null) || return
      echo "("${ref#refs/heads/}")"
    }

    #Define some prompt colors
    RED="\[\033[0;31m\]"
    YELLOW="\[\033[0;33m\]"
    GREEN="\[\033[0;32m\]"
    CYAN="\[\033[1;36m\]"
    BLUE="\[\033[1;34m\]"


    # Set up the prompt to show what directory we are in
    # and if it is a working copy, then show what branch is active
    PS1="[${RED}\t ${GREEN}\w ${YELLOW}\$(__git_ps1) ${GREEN}]\$ "


    LS_COLORS='di=1:fi=0:ln=31:pi=5:so=5:bd=5:cd=5:or=31:mi=0:ex=35:*.exe=90'
    export LS_COLORS
    alias ls='ls -F --color --show-control-chars'

|

.bash_profile
---------------

|

.. code-block:: bash
    :number-lines:

    # ~/.bash_profile
    SSH_ENV="$HOME/.ssh/environment"

    function start_agent {
         echo "Initialising new SSH agent..."
         ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
         echo succeeded
         chmod 600 "${SSH_ENV}"
         . "${SSH_ENV}" > /dev/null
         ssh-add;
    }

    # Source SSH settings, if applicable

    if [ -f "${SSH_ENV}" ]; then
         . "${SSH_ENV}" > /dev/null
         #ps ${SSH_AGENT_PID} doesn't work under cywgin
         ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
             start_agent;
         }
    else
         start_agent;
    fi
