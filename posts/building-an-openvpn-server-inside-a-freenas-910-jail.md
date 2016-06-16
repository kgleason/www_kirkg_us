<!-- 
.. title: Building an OpenVPN server inside a FreeNAS 9.10 jail
.. slug: building-an-openvpn-server-inside-a-freenas-910-jail
.. date: 2016-06-12 11:27:48 UTC-05:00
.. tags: Open Source, FreeNAS, FreeBSD, OpenVPN
.. category: 
.. link: 
.. description: 
.. type: text
-->

A while back, I wrote a post about [Building an OpenVPN server inside a FreeNAS jail](../posts/building-an-openvpn-server-inside-a-freenas-jail) for a friend who has a small FreeNAS device, but doesn't have a firewall that will let him run an OpenVPN server directly. Much to my surprise, this article seems to have gotten some traction, so I'm posting an update to it (leaving the old on in place for posterity's sake).

Since I wrote the previous article, a few things have changed. The most important chance that the diligent reader will need to be aware of is that I've upgraded my FreeNAS from the 9.3 train to the 9.10 train. The UI looks the same, but there is the added benefit of being able to use FreeBSD 10 as the jail template.

<!-- TEASER_END -->

I had some issue with standard jails after the upgrade to FreeNAS 9.10, so before I get into the meat of it, I'm going to outline what I did to get back to a funcitonal state. I haven't yet looked to see if there are any known bugs yet, but I will at some point. I honestly think that I've probably screwed it up, since I tend to mess with the `warden` command a bit. 

In attempting to add a new jail, I was getting an error message from FreeNAS about not being able to find the jail template. In order to successfully add the new jail, I created a custom jail template. In the FreeNAS UI, go to Jails -> Templates, and click the "Add Jail Template" button. 

![FreeNAS Custom Jail](../../images/FreeNAS_JailTemplate.png)

The URL for the jail template is [http://download.freenas.org/jails/10/x64/freenas-standard-10.3-RELEASE.tgz](http://download.freenas.org/jails/10/x64/freenas-standard-10.3-RELEASE.tgz).

Once I had a functioning template, I was able to create a jail. I did have to go into "Advanced" to specify the template, but otherwise, it is a pretty stock jail.

##Installing OpenVPN

For the most part the high level steps are going to be the same. We'll start out by getting into the jail from the FreeNAS shell:


	:::shell
    sudo jexec `jls | grep -i openvpn | awk '{ print $1 }'` csh


That command assumes that you only have a single jail with the name OpenVPN in the name. If you have more than one, or if your jail doesn't have the word `OpenVPN` in the name, then that command won't work. I'll leave it to you to figure it out.

Once you are in the jail, run some basic updates:


	:::shell
	pkg update
	pkg upgrade


The output from these commands will vary, but in general, you'll want to say yes to whatever is asked. I'm also going to install `vim` Once that is done, install OpenVPN.


	:::shell
	pkg install vim-lite openvpn


There should be 3 total packages that get installed.

##Configuring OpenVPN
With the basic OpenVPN installed, you'll want to get down to configuring it. For this go around, it is going to be more FreeBSD-esque, and set everything up in `/usr/local/`


	:::shell
	mkdir -p /usr/local/etc/openvpn/
	cp -R /usr/local/share/easy-rsa /usr/local/etc/openvpn/easy-rsa/


Easy RSA has changed a lot of stuff between EasyRSA 2 and EasyRSA 3, so the old steps don't apply anymore. We'll get started with EasyRSA 3 by making ourselves a copy of the shell script was can use:


	:::shell
	cd /usr/local/etc/openvpn/easy-rsa
	cp easyrsa-.real easyrsa
	chmod 755 easyrsa


At this point, we have a choice about configuring EasyRSA. We can answer the same questions over and over again, or we can edit the vars file to set some sane defaults, which will allow us to accept the defaults as we go through the script. odds are that you'll only need to change the stuff about your location:


    set_var EASYRSA_REQ_COUNTRY    "US"
	set_var EASYRSA_REQ_PROVINCE   "Indiana"
	set_var EASYRSA_REQ_CITY       "Bloomington"
	set_var EASYRSA_REQ_ORG        "KirkG dot us"
	set_var EASYRSA_REQ_EMAIL      "kirk@kirkg.us"
	set_var EASYRSA_REQ_OU         "IT"


##Building the PKI
Getting the PKI set up is pretty simple:


	:::shell
	/usr/local/etc/openvpn/easy-rsa/easyrsa init-pki
	/usr/local/etc/openvpn/easy-rsa/easyrsa build-ca


You'll be prompted for a pass phrase for the PEM. This will be the CA passphrase. Be sure to remember what you choose. Next we'll need to generate a server certificate:


	:::shell
	/usr/local/etc/openvpn/easy-rsa/easyrsa gen-req VPN_SERVER_NAME nopass


Replace the VPN_SERVER_NAME with the shortname of your VPN. For example, I'm using testvpn.kirkg.us as the hostname for this test instance, so in the command, I used `testvpn` in place of VPN_SERVER_NAME. Next, we'll need to generate the client certificate:


	:::shell
	/usr/local/etc/openvpn/easy-rsa/easyrsa gen-req VPN_CLIENT_SHORTNAME


In this case, replace the VPN_CLIENT_SHORTNAME with the short name of your client. Since you'll need to generate a certficiate per client, you can use this to delineate which certs go to which clients.

This command will prompt for a password. Your clients will need this password to unlock the certificate in order to connect. You can use the `nopass` option if you want, but it isn't recommended.

The next step is to have the CA sign the requests so that they are proper certs.


	:::shell
	/usr/local/etc/openvpn/easy-rsa/easyrsa sign server VPN_SERVER_NAME
	/usr/local/etc/openvpn/easy-rsa/easyrsa sign client VPN_CLIENT_SHORTNAME


During those commands you'll need to type the word `yes` to confirm the certificates, and then enter the passphrase for the CA that you set up a few steps ago. 

The last step of the PKI is to set up some Diffe-Hellman parameters (a.k.a. DHPArams). One command should do it.


	:::shell
	/usr/local/etc/openvpn/easy-rsa/easyrsa gen-dh


Since you'll want this VPN to be as secure as possible, use the following command to generate a tls-auth key. This step is optional, and you can read more about it when the server config file is created below.


	:::shell
	openvpn --genkey --secret /usr/local/etc/openvpn/easy-rsa/pki/private/ta.key


With that, all of the PKI should be in place. Before we get started making config files, we'll want to protect our PKI by copying it out of the easy-rsa directory. That way if anyone happens to be playing with the `easyrsa` script, something doesn't get accidentally overwritten.


	:::shell
	cp /usr/local/etc/openvpn/easy-rsa/pki /usr/local/etc/openvpn

##The Server config file

With the client & server key business out of the way, it's time to configure the server. The good people at [OpenVPN](http://www.openvpn.net) make some pretty great [sample configs](https://openvpn.net/index.php/open-source/documentation/howto.html#examples) available to us, so it makes sense to start with them. Copy the text for the server.conf and paste it into `/usr/local/etc/openvpn/server.conf` inside your jail.

There is very little that will need tweaking in that file. Read through the comments, and adjust as you see fit, but you'll do well to avoid making too many changes. Here are some sections to consider.

###Local IP

    # Which local IP address should OpenVPN
    # listen on? (optional)
    local 10.0.0.248

The `local` config line should reflect the IP address of your jail. In all likelihood, this will be an RFC-1918 private IP address. This is OK.

###Tracking client IPs


	# Maintain a record of client  virtual IP address
	# associations in this file.  If OpenVPN goes down or
	# is restarted, reconnecting clients can be assigned
	# the same virtual IP address from the pool that was
	# previously assigned.
	ifconfig-pool-persist /usr/local/etc/openvpn/ipp.txt


This one is pretty self explanatory. Since the default directory may not exist, it's probably best to keep everything contained within `/usr/local/etc/openvpn`.

###Certificate location


	# Any X509 key management system can be used.
	# OpenVPN can also use a PKCS #12 formatted key file
	# (see "pkcs12" directive in man page).
	ca /usr/local/etc/openvpn/pki/ca.crt
	cert /usr/local/etc/openvpn/pki/issued/VPN_SERVER_NAME.crt
	key /usr/local/etc/openvpn/pki/VPN_SERVER_NAME.key  # This file should be kept secret

	# Diffie hellman parameters.
	# Generate your own with:
	#   openssl dhparam -out dh2048.pem 2048
	# Substitute 2048 for 1024 if you are using
	# 2048 bit keys.
	dh /usr/local/etc/openvpn/pki/dh.pem


If you've followed the steps up to this point, you will just need to swapout the name of the server in the cert and key lines.  If you put your keys directory elsewhere, then adjust the paths as necessary.


###Internal Subnet


	# Push routes to the client to allow it
	# to reach other private subnets behind
	# the server.  Remember that these
	# private subnets will also need
	# to know to route the OpenVPN client
	# address pool (10.8.0.0/255.255.255.0)
	# back to the OpenVPN server.
	push "route 10.0.0.0 255.255.255.0"


For this section, you need to know a little bit about your internal network. The IP address in the `push` line should be a representation of your local network. If you don't know what to put here, then from within your jail, run the `ifconfig` command and get your IP address and subnet mask. If you subnet mask is 255.255.255.0, then change the last octet of your IP address to a 0, and use that. Otherwise, jot down your IP address and subnet maslk. With those values in hand, visit [www.subnet-calculator.com](http://www.subnet-calculator.com), and enter your IP address into the IP address field. Adjust the subnet mask dropdown to reflect your subnet mask. Using the values on that site, construct the `push` config line as follows:


    push "route <Subnet ID> <Subnet Mask>"


###TLS Auth Key


	# The server and each client must have
	# a copy of this key.
	# The second parameter should be '0'
	# on the server and '1' on the clients.
	tls-auth /usr/local/etc/openvpn/pki/private/ta.key 0 # This file is secret


That one is pretty simple. Point the `tls-auth` directive to your `ta.key`.


###Logging


	# Output a short status file showing
	# current connections, truncated
	# and rewritten every minute.
	status /var/log/openvpn/openvpn-status.log

You'll need to `mkdir /var/log/openvpn/` in order for this work.


###Two factor authenitcation


    plugin /usr/local/lib/openvpn/plugins/openvpn-plugin-auth-pam.so login


You won't find this line in the sample config, and you can consider it to be optional. If you add it in, then in addition to the required certificates, you will need to provide a username and password to connect to the VPN. If you opt for this (and you probably should), there is an line that you will need to add to the client config as well.

##Networking

With the server config finsihed, we need to deal with the networking. In order to do this, we'll be using [ipfw](https://www.freebsd.org/doc/en/books/handbook/firewalls-ipfw.html), which is built into FreeBSD. You'll need to start by learning the name of the NIC in your jail. You can get this from `ifconfig`. For this example, we will be using epair8b. Yours will probably be very similar to that.

Armed with the interface name, you can create `/usr/local/etc/ipfw.rules`:


	# /usr/local/etc/ipfw.rules
	ipfw -q -f flush
	ipfw -q nat 1 config if epair8b
	ipfw -q add nat 1 all from 10.8.0.0/24 to any out via epair8b
	ipfw -q add nat 1 all from any to any in via epair8b


In a nutshell, that ruleset does this:

  1. flush out all of the existing firewall rules
  1. Define a NAT (number 1) on our interface
  1. Masquerade any outbound traffic from the openvpn network (10.8.0.0) behind the ip on our interface

##Automatic starting

Presumably you will want everything to start automatically. All of that sort of thing is controlled with rc.conf in FreeBSD. Add these lines to the end of `/etc/rc.conf`


	:::config
	# /etc/rc.conf
	openvpn_enable="YES"
	openvpn_if="tun"
	openvpn_configfile="/usr/local/etc/openvpn/server.conf"
	openvpn_dir="/usr/local/etc/openvpn/"
	cloned_interfaces="tun"
	gateway_enable="YES"
	firewall_enable="YES"
	firewall_script="/usr/local/etc/ipfw.rules"


With that in place, you can go back to the FreeNAS UI and restart the jail if you want. Or you can run a couple of commands to turn everything on:


	:::shell
    sysctl net.inet.ip.forwarding=1
    service ipfw start
    service openvpn start


 If, like me, you get an error about not being able to start openvpn, then make sure that the `/var/log/openvpn/` directory exists.

 ##Configuring the client

 With the server up and running, the last step is going to be to get a client to connect. There are many different clients that you can use, depending upon your platform. We are going to assume that you are using a unix command line client. There are a bunch of different ways that you can get this installed:

   * FreeBSD:
     * pkg install openvpn
   * Linux:
     * use your package manager to install `OpenVPN`
         * Arch: sudo pacman -S openvpn
         * Debian: sudo apt-get install openpvn
         * RedHat: sudo yum install openvpn
   * OS X (You'll have to do more that just install openvpn, but homebrew should tell you what to do to get the tun/tap driver installed in OS X)
     * brew install openvpn

 Once you have the `openvpn` binary installed, your client platform of choice shouldn't be of great concern.

 ###Get the files

 In order to keep everything clean, you'll need to create a directory to hold everything:


 	:::shell
     mkdir ~/.openvpn
     cd ~/.openvpn


 There are 4 files on the server that you will need on your client. The jail isn't running ssh, so you can get creative about how you get them back to your client. One option is to copy the contents of the files off of the server and paste them into the files on the client. Or you can start ssh with `service sshd onestart`. The files that you'll need from the server are:


   * /usr/local/etc/openvpn/pki/ca.crt
   * /usr/local/etc/openvpn/pki/private/ta.key
   * /usr/local/etc/openvpn/pki/issued/VPN_CLIENT_SHORTNAME.crt
   * /usr/local/etc/openvpn/pki/private/VPN_CLIENT_SHORTNAME.key


 Replace VPN_CLIENT_SHORTNAME up there with the client name that you've used up to this point.

 ##The client config file

 With all of the certs in place, it's time to create a client side config file. Go back to the [OpenVPN sample configs](https://openvpn.net/index.php/open-source/documentation/howto.html#examples) and grab the client config. Paste the contents into `~/.openvpn/VPN_SERVER_NAME.ovpn`.

 As with the server config, there isn't much to change.

 ###Remote endpoint


 	# The hostname/IP and port of the server.
 	# You can have multiple remote entries
 	# to load balance between the servers.
 	remote 10.0.0.248 1194


 For the initial test, you should be able to specify the local IP of the OpenVPN jail. We'll have to come back and change this later.

 ###Quiet down the wifi warnings


 	# Wireless networks often produce a lot
 	# of duplicate packets.  Set this flag
 	# to silence duplicate packet warnings.
 	mute-replay-warnings


 Not much to say. You can keep this commented out if you want.

 ###Where are the certs?

 If you have all of the certs in the same directory as the client config file, then you can define the cert locations like this:


 	# SSL/TLS parms.
 	# See the server config file for more
 	# description.  It's best to use
 	# a separate .crt/.key file pair
 	# for each client.  A single ca
 	# file can be used for all clients.
 	ca ca.crt
 	cert VPN_CLIENT_SHORTNAME.crt
 	key VPN_CLIENT_SHORTNAME.key


 If they are in a different location, you can use full paths.

 ###The TLS auth key


 	# If a tls-auth key is used on the server
 	# then every client must also have the key.
 	tls-auth ta.key 1


 This key needs to be the same on the client and the server. The `1` parameter indicates that this is a client.

 ###Two Factor Authenitcation


 	# Force username & password authenitcation
     auth-user-pass

     # Disable client-side password caching
     auth-nocache


 These are the client-analogue lines to the optional config line in the server that will require a username and password to connect. If you added the optional line to the server config, then you will need to add this to the client config. If you add these lines to the client config without the server lines, then you will be prompted for a username and password that will then be ignored.

 ##Firing up the test

 Save the config file, and fire up a test:


 	:::bash
     sudo openvpn <client>.ovpn


 You'll probably see some errors about adding a route. If your test client and your server are on the same network, then the route to that network already exists on the client. If you ignore that for now, you should still get a connection -- useless, but a connection nonetheless.
