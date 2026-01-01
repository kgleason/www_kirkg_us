<!-- 
.. title: Setting up IPv6 with OPNSense and Comcast
.. slug: setting-up-ipv6-with-opnsense-and-comcast
.. date: 2015-08-19 19:45:48 UTC-05:00
.. tags: IPv6, OPNSense, networking
.. category: Technology
.. link: 
.. description:
.. type: text
-->

Ten years ago, I was very much into [IPv6](https://en.wikipedia.org/wiki/IPv6). I had two different tunnels, and all of my home network had v6 IP addresses -- all statically assigned, with working reverse DNS. Even the Windows XP machines. Then I got lazy. I swapped out my hand-crafted [OpenBSD](https://openbsd.org) router for an off-the-shelf wireless router. That old homemade router was old enough that I couldn't put a Wifi card in it, and I just wanted some wifi.

For a couple of years now, I've noticed that Comcast has been giving me an IPv6 address, but I haven't really been able to figure anything out with it. When I was using an Apple AirPort Extreme,  turning on IPv6 would break everything. So I just left it off. Even when I was running [pfSense](https://pfsense.org), I saw it, but I spent so much time accidentally breaking [pfSense](https://pfsense.org) that I never got to look into it any further.

Since I'm a few months into [OPNSense](https://opnsense.org) now, and things seem to be rock solid, I decided to have another go at IPv6. What follows are the steps that I took to get IPv6 up and running as expected on my home network.

<!-- TEASER_END -->

##My setup
Before I get into the screenshots and such, let me oultine what I've got:

   * Comcast residential cable internet service -- not a business class connection, and no static IPs.
   * [ARRIS Surfboard SB6141 Cable Modem](http://www.amazon.com/ARRIS-SURFboard-SB6141-DOCSIS-Cable/dp/B00AJHDZSI/ref=sr_1_1?s=pc&ie=UTF8&qid=1440032565&sr=1-1&keywords=sb6141).  I bought this myself, and I am very happy I did. I used the Comcast rental for a couple of years. The difference is amazing.
   * [OPNsense](https://opnsense.org) 15.7.8-amd64. My [OPNSense](https://opnsense.org) box is built out of random old parts. Nothing amazing, but ample for what I need.


Since I installed [OPNSense](https://opnsense.org), I noticed my WAN interface has had an IPv6 address. Comcast is handing it to me via DHCP6, which I think is the default setting in [OPNSense](https://opnsense.org). I didn't want to NAT for an IPv6 connection, since it defeats the purpose of IPv6. Honestly I didn't even try. In the end, here is what I did to get it all working, with each of my home machines assigned a public IPv6 address.

###Enable IPv6
I think that IPv6 is enabled by default, but just to be sure, go to Settings -> Networking, and make sure that **Allow IPv6** is checked. If it isn't, then check it.

###WAN Settings

Start by looking at the settings for your WAN interface (Interfaces -> WAN). It should be set to *DHCP6* for **IPv6 Configuration Type**.

![DHCP Setting for the WAN interface](../../images/WAN_DHCP_Settings.png)

Scroll down a bit, and find the DHCP6 client configuration. Change the **DHCPv6 Prefix Delegation** size to *64*. Leave all of the other client settings at their defaults.

![DHCP6 Client settings for the WAN interface](../../images/DHCP6_Client_Settings.png)

Click save, and apply the changes if prompted to do so.

###LAN Settings

The next step will be to go over to the LAN settings (Interfaces -> LAN), and make a couple of changes there. Start by setting the **IPv6 Configuration Type** to *Track Interface*.

![DHCP Settings for the LAN interface](../../images/LAN_DHCP_Settings.png)

Scroll down to the **Track IPv6 Interface** section. Verify that **IPv6 Interface** is set to *WAN*, and that **IPv6 Prefix ID** is set to *0*.

![LAN Track interface Settings](../../images/LAN_TrackInterface_Settings.png)

Click save, and apply the changes if you are prompted to.

Once that is applied, you should pretty quickly see that your LAN interface has an IPv6 address. In my case, the LAN IP and the WAN IP seem to be on different subnets, specifically, the WAN address starts with `2001:` and my LAN address starts with `2601:`. In my case, this did not matter.

###Adding in a firewall rule.

When I got to this point, I thought that I was golden, but none of my internal machines would grab an IPv6 address. I was able to ping [ipv6.google.com](http://ipv6.google.com) via [OPNSense](https://opnsense.org)'s diagnostic tools. I was missing the final piece of the puzzle, a firewall rule to allow DHCP6 traffic to pass through.

![Inbound DHCpv6 firewall rule](../../images/DHCP6_IB_Rule.png)

This rule, once applied, will allow DHCP6 to come into the LAN from the outside network.  At this point, I also rebooted [OPNSense](https://opnsense.org), but that probably isn't necessary. Not too long after [OPNSense](https://opnsense.org) came back up, pretty much all of my internal machines had IPv6 addresses..

##Test all the things!

I ran a few tests, just to be sure. Here are a few of them:

  * [Google IPv6](http://ipv6.google.com): This only works from an IPv6 connection. If I recall correctly, you will get 404 or some other error if you browse there from a v4 address.
  * [The Kame Project](http://www.kame.net): If you browse there from a v6 connection, the turtle at the top of the page will be swimming. If it is not moving, then you have connected from a v4 connection.
  * [Comcast IPv6 tests](http://test-ipv6.comcast.net/): This will fire off off some tests. 
  * [IPv6 Port Scan](http://ipv6.chappell-family.com/ipv6tcptest/): Every time I make a change to my firewall, I like to use Steve Gibson's [Shields Up port scanner](https://www.grc.com/x/ne.dll?bh0bkyd2) to make sure that the changes work as I expect. It appears that GRC doesn't yet support v6. But the one I linked up there does. Because of the way IPv6 works, you'll be testing your ocal machine, but it should still be protected by [OPNSense](https://opnsense.org), so it should result in all greens, unless you've opened up some ports.

##Wrapping it all up
The last thing for me was to see if my FreeBSD jails (runnning on a FreeNAS) would grab addresses. They did, which is awesome. Now it's time to migrate some stuff. But that's for another day...