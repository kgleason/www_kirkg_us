<!--
.. title: OpenVPN server in a FreeNAS 11 jail
.. slug: openvpn-server-in-a-freenas-11-jail
.. date: 2017-07-08 13:02:49 UTC-05:00
.. tags: Open Source, FreeNAS, FreeBSD, OpenVPN, EasyRSA
.. category: tutorials
.. link:
.. description:
.. type: text
-->

FreeNAS 11 [was recently released](http://www.freenas.org/blog/freenas-11-0/), so I'm going to continue my series on [running](../building-an-openvpn-server-inside-a-freenas-jail) OpenVPN [servers](../running-an-openvpn-server-in-a-freenas-910-jail) from FreeNAS jails. In theory these instractions could be followed on an old [FreeBSD](https://www.freebsd.org) 11 jail, but FreeNAS provides a friendly UI, so why not use it?

For giggles, I'm taking screenshots for this with the new FreeNAS UI. So far it's nice. You should definitely try it.

<!-- TEASER_END -->

##Update the Jail config
The first thing I had to do was to fix the jails config. I did this by going to Jails -> Configuration (in the left hand nav menu). Under advanced mode, there is an option for "Collection URL". The value that was in there by default (http://download.freenas.org/latest/RELEASE/x64/jails) didn't work for me, but I managed to figure out that it should probably be something more like this one [http://download.freenas.org/jails/11/x64/](http://download.freenas.org/jails/11/x64/).

![Updated jails config](../../images/FreeNAS11_Updated_Jails_Config.png)

##Creating the jail
With that out of the way, I was able to create the new jail. In the nav, Jails -> Instances. On that screen, there is a big green + sign where the magic happens. Feel free to name your jail however you want, but I'd recommend that you name it something that indicates what it is. I've named mine "openvpn_11".

![Creating a new jail](../../images/FreeNAS11_NewJail.png)
