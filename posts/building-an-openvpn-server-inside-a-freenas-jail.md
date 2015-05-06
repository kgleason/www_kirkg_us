<!--
.. title: Building an OpenVPN server inside a FreeNAS jail
.. slug: building-an-openvpn-server-inside-a-freenas-jail
.. date: 2015-04-30 18:23:36 UTC-05:00
.. tags: Open Source, FreeNAS, FreeBSD, OpenVPN
.. category:
.. link:
.. description:
.. type: text
-->

If you have an up to date FreeNAS server (9.3 stable at the time of this writing), then this guide should walk you through building a jail and installing an OpenVPN server inside of it. The beauty of this system is that it is all being done inside a jail, so the odds of making a mistake that could take down your entire NAS is slim. If something goes awry, you can just delete the jail, and start over again.

After you finish, you will end up with an certificate based OpenVPN server. Each user will need to have their own certificate to go along with their username and password. In essence, we'll be implementing a two factor authenticated VPN.

<!-- TEASER_END -->

You'll need to start out by logging into your FreeNAS and clicking on the Jails tab. Click the `Add Jail` button to get started creating a new jail. Name your jail something obvious, like "OpenVPN_1". And click `Add` to get started. If you have already set up FreeNAS, then it should create a standard jail automatically and assign an IP address based from the jails pool. Depending upon your FreeNAS specs, the jail could take a few minutes to be made. Be paitent.

With that out of the way, you should open up your favorite terminal and ssh into your FreeNAS. Yes the FreeNAS, not the newly created jail. Once you are in, and assuming that you only have a single jail with the word 'openvpn' in it, you should be able to run this command to get into the jail:


	:::shell
    sudo jexec `jls | grep -i openvpn | awk '{ print $1 }'` csh


If, for whatever reason that command did not work, then run `jls` to get a list of your jails. Note the ID of the jail that you want to use, and enter this command to get in:


	:::shell
    sudo jexec ID csh


replacing ID with the ID of the jail that you want to use.

You should now have a root shell inside the jail, so now you can get to it. Run `pkg install openvpn`. This command will start out by checking if your version of pkgng is up to date. If it is not, then it ask you if it is OK for it to update itself:


    Installed packages to be UPGRADED:
	pkg: 1.3.7 -> 1.5.1

    The process will require 258 kB more space.
    2 MB to be downloaded.

    Proceed with this action? [y/N]: Y


Say Yes. Then it will prompt you about installing the OpenVPN package:


    The following 3 package(s) will be affected (of 0 checked):

    New packages to be INSTALLED:
	    openvpn: 2.3.6_3
	    easy-rsa: 2.2.0.m
	    lzo2: 2.09

    The process will require 1 MiB more space.
    521 KiB to be downloaded.

    Proceed with this action? [y/N]:


Once again, you should say yes. The packages should install pretty quickly. Once it is finished, run the `rehash` command so that you have access to the newly installed binaries.

When you have your shell back, make a directory to store all of the OpenVPN bits, and bring in a couple of tools that we are going to need.


    :::shell
    cd /
    mkdir openvpn
    cd openvpn
    cp -r /usr/local/share/easy-rsa .
    cd easy-rsa


A quick edit to the `vars` file will keep you from having to answer the same questions over and over again -- you will have to generate quite a few certificates, so this is a worthwhile step.

##A quick word about editors in FreeBSD

At this point, I'm generally inclined to `pkg install vim-lite` because I prefer `vim` to `vi`, but you'll want to resist that temptation -- installing `vim-lite` will mess with the default gettext library, and will give you a headache. Attempting to install nano will do the same thing. Fixing that issue is beyond the scope of this tutorial.

Luckily, FreeBSD comes it a built in editor called `edit`. It's pretty intuitive, so if you don't want to deal with `vi`, I'd recommend that.

##The vars file

For the most part, you can leave most of this file as is. If you go all the way down to the end, you will find the pieces that will need to be changed:


	:::shell
	export KEY_COUNTRY="US"
	export KEY_PROVINCE="IN"
	export KEY_CITY="Bloomington"
	export KEY_ORG="KirkG dot us"
	export KEY_EMAIL="me@mydomain.com"
	export KEY_EMAIL=mail@mydomain.com
	export KEY_CN=vpn.mydomain.com
	#export KEY_NAME=changeme
	export KEY_OU=IT
	#export PKCS11_MODULE_PATH=changeme
	export PKCS11_PIN=1234


The comments right above that part say to not leave any of the fields blank, but it is really not that big of a deal. Save your vars.

##Setting up your certificates

If you haven't noticed, the default shell for root in FreeBSD is csh. In order to perform the next few steps, we'll need some Bourne shell functionality. If you really want to install bash, you can, but it is overkill for what you are about to do. The following commands are going to use `sh` (the Bourne shell). It should also work with `bash`, if that's the kind of person you are.

Note that the 2nd command has a space between the period (.) and the vars. In the classic Bourne shell, this is how you source a file. The space is important.


	:::shell
    sh
    . vars
    ./clean-all
    ./build-ca
    ./build-key-server $KEY_CN
    ./build-dh
    openvpn --genkey --secret keys/ta.key


 After you source vars, you will get a warning about `clean-all` ... don't fret. It is perfectly safe. When you run `./build-ca`, you should  be able to hit enter to accept all of the defaults. The `build-ca` step builds a certificate authority for your VPN to use.

 When you run the `./build-key-server` command, you will pass in the CN value that you defined in vars. This keeps things consistent. You can continue to press enter for the default until you get to


    Please enter the following 'extra' attributes
    to be sent with your certificate request


It will prompt you for a challenge password and an optional company name. We recommend that you leave these blank. When you are prompted to sign the certificate, you should say yes. When you are asked to commit the new cert, you should once again say yes.

Building the Diffie-Hellman keys may take a few minutes, depending upon your hardware. The `openvpn` command will execute quickly.

The last step in the key building process is to generate the certs for your client to connect. If you are going to have multiple users, you will want to run this command for each client that you plan to have connect.


	:::shell
    ./build-key <client-name>


Your client-name should be something descriptive. It is purely for human readability purposes. You can press enter for all of the questions that are asked. When prompted to sign the certificate and commit the certificate, you should once again say yes.

##Protect your keys

The `clean-all` command that we ran up there will wipe out all of your keys. Right now it's not big deal -- just generate new ones. However once you've handed a key out to your clients, then the deletion of the keys will prevent your client from connecting.

For right now, you can protect your keys from accidental deletion with:


	:::shell
    cp -r keys ../
    cd ..
    exit
		rehash


The `exit` is to get us out of the Bourne shell, and back to `csh`, where things look more friendly. The `rehash` is just for good measure.

##The Server config file

With the client key business out of the way, it's time to configure the server. The good people at [OpenVPN](http://www.openvpn.net) make some pretty great [sample configs](https://openvpn.net/index.php/open-source/documentation/howto.html#examples) available to us, so it makes sense to start with them. Copy the text for the server.conf and paste it into `/openvpn/server.conf` inside your jail.

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
	ifconfig-pool-persist /openvpn/ipp.txt


This one is pretty self explanatory. Since the default directory may not exist, it's probably best to keep everything contained within `/openvpn`.

###Certificate location


	# Any X509 key management system can be used.
	# OpenVPN can also use a PKCS #12 formatted key file
	# (see "pkcs12" directive in man page).
	ca /openvpn/keys/ca.crt
	cert /openvpn/keys/homevpn.kirkg.us.crt
	key /openvpn/keys/homevpn.kirkg.us.key  # This file should be kept secret

	# Diffie hellman parameters.
	# Generate your own with:
	#   openssl dhparam -out dh1024.pem 1024
	# Substitute 2048 for 1024 if you are using
	# 2048 bit keys.
	dh /openvpn/keys/dh1024.pem


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
	tls-auth /openvpn/keys/ta.key 0 # This file is secret


That one is pretty simple. Point the `tls-auth` directive to your `ta.key`.


###Logging


	# Output a short status file showing
	# current connections, truncated
	# and rewritten every minute.
	status /openvpn/log/openvpn-status.log

You'll need to `mkdir /openvpn/log` in order for this work.


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
	openvpn_configfile="/openvpn/server.conf"
	openvpn_dir="/openvpn/"
	cloned_interfaces="tun"
	gateway_enable="YES"
	firewall_enable="YES"
	firewall_script="/usr/local/etc/ipfw.rules"


With that in place, you can go back to the FreeNAS UI and restart the jail if you want. Or you can run a couple of commands to turn everything on:


	:::shell
    sysctl net.inet.ip.forwarding=1
    service ipfw start
    service openvpn start


 If, like me, you get an error about not being able to start openvpn, then make sure that the `/openvpn/log` directory exists.


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


  * /openvpn/keys/ca.crt
  * /openvpn/keys/ta.key
  * /openvpn/keys/<client-name\>.crt
  * /openvpn/keys/<client-name\>.key


Replace the <client-name\> up there with the client-name you used when you created the client cert.

##The client config file

With all of the certs in place, it's time to create a client side config file. Go back to the [OpenVPN sample configs](https://openvpn.net/index.php/open-source/documentation/howto.html#examples) and grab the client config. Paste the contents into `~/.openvpn/<homevpn>.ovpn`.

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
	cert kirk-client.crt
	key kirk-client.key


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

##Finishing up

If you are satisfied, then you will want to do 3 things to wrap it all up.

First, in the OpenVPN client config, you'll need to change the `remote` directive, replacing the internal IP with either your public IP, or a DNS hostname.

Secondly, you'll want to run the `adduser` command within the jail to add a user.

Lastly, you'll need to configure your router to pass traffic coming in on port 1194 to your new jail's IP. With that in place, you should be able to connect to your network from a remote location.
