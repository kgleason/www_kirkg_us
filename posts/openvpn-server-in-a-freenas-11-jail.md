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

FreeNAS 11 [was recently released](http://www.freenas.org/blog/freenas-11-0/), so I'm going to continue my series on [running](../building-an-openvpn-server-inside-a-freenas-jail) OpenVPN [servers](../running-an-openvpn-server-in-a-freenas-910-jail) from FreeNAS jails. In theory these instructions could be followed on any old [FreeBSD](https://www.freebsd.org) 11 jail, but FreeNAS provides a friendly UI, so why not use it?

For giggles, I'm taking screenshots for this with the new FreeNAS UI. So far it's nice. You should definitely try it.

##Update the Jail config
The first thing I had to do was to fix the jails config. I did this by going to Jails -> Configuration (in the left hand nav menu). Under advanced mode, there is an option for "Collection URL". The value that was in there by default (http://download.freenas.org/latest/RELEASE/x64/jails) didn't work for me, but I managed to figure out that it should probably be something more like this one [http://download.freenas.org/jails/11/x64/](http://download.freenas.org/jails/11/x64/).

<!-- TEASER_END -->

![Updated jails config](../../images/FreeNAS11_Updated_Jails_Config.png)

##Creating the jail
With that out of the way, I was able to create the new jail. In the nav, Jails -> Instances. On that screen, there is a big green + sign where the magic happens. Feel free to name your jail however you want, but I'd recommend that you name it something that indicates what it is. I've named mine "openvpn_11".

![Creating a new jail](../../images/FreeNAS11_NewJail.png)

Unfortunately, I had problems with the that I created from the new UI. Namely, it didn't seem to have properly created a network interface inside the jail, so while it would start, it wouldn't get an IP address. So I deleted the jail, and went back to the classic UI. Created the jail anew, and everything worked as expected.

##Entering the jail
The steps for entering the jail are the same as in previous versions. Essentially, get the list of jails, find your jail, and enter into to using a shell. It is assumed that you have used ssh to connect to your FreeNAS and have become root for the following steps.


    :::shell
    jexec `jls | awk '/openvpn_11/ { print $1 }'` tcsh


Once that command has been executed, your shell prompt should change to reflect that you've entered the jail.

##Install some updates, and some packages
To start out, let's make sure we are all up to date, and then install some packages:


    :::shell
    pkg update
    pkg upgrade
    pkg install vim-lite openvpn


For me, the final command installed 5 packages, but the number may vary. After a quick `rehash`, all of the new commands should be available for use.

##Configuring OpenVPN
I order to make this simpler on myself, I'm going to set some shell variables so that I can simply use the variable in subsequent commands. You don't have to use these, but you'll need to remember to substitute in the paths.


    :::shell
    setenv OVPATH /usr/local/etc/openvpn
    setenv OVRSA /usr/local/etc/openvpn/easy-rsa
    setenv VPNSERVER home.kirkg.us
    setenv VPNCLIENT kirk.kirkg.us


With these set, we'll get started setting up the PKI for OpenVPN.


    :::shell
    mkdir -p $OVPATH
    cp -r /usr/local/share/easy-rsa $OVRSA
    cd $OVRSA
    cp easyrsa.real easyrsa
    chmod 755 easyrsa


Those commans will create the required directories, and get the EasyRSA stuff in place, and create us a working directory.

At this point, we have a choice about configuring EasyRSA. We can answer the same questions over and over again, or we can edit the `vars` file to set some sane defaults, which will allow us to accept the defaults as we go through the script. Odds are that you'll only need to change the stuff about your location:


    :::shell
    set_var EASYRSA_REQ_COUNTRY    "US"
    set_var EASYRSA_REQ_PROVINCE   "Indiana"
    set_var EASYRSA_REQ_CITY       "Bloomington"
    set_var EASYRSA_REQ_ORG        "KirkG dot us"
    set_var EASYRSA_REQ_EMAIL      "kirk@kirkg.us"
    set_var EASYRSA_REQ_OU         "IT"


Uncomment and adjust any values that you would like to change from the defaults.

##Building the PKI
For our certificate infrastructure, this is going to assume that you are looking for a basic installation, where your CA and OpenVPN server are the same host. We will generate all of the certificates right up front. Getting the PKI set up is pretty simple:


  	:::shell
  	cd $OVRSA
  	./easyrsa init-pki
  	./easyrsa build-ca


You'll be prompted for a passphrase for the PEM. This will be the CA passphrase. Be sure to remember what you choose, since you will need this passphrase every time you generate a new client certificate. If you forget this, then you will need to rebuild your CA, and all of your existing client certificates will immediately be useless.

Now we'll generate our server & client certificates


    :::shell
    cd $OVRSA
    ./easyrsa gen-req $VPNSERVER nopass
    ./easyrsa gen-req $VPNCLIENT


Both of those commands will prompt for a PEM passphrase. You can use the `nopass` option for the client if you really want to skip protecting the cert with a passphrase, but it isn't recommended. If you skip the `nopass` option on the server, OpenVPN won't start correctly, since there won't be a way to enter the password for the cert.

Next, we need to sign the certs with our newly minted CA.


    :::shell
    cd $OVRSA
    ./easyrsa sign server $VPNSERVER
    ./easyrsa sign client $VPNCLIENT


During those commands you'll need to type the word `yes` to confirm the certificates, and then enter the passphrase for the CA that you set up a few steps ago.

Finally, we'll set up some Diffe-Hellman parameters (a.k.a. DHPArams). This command will take some time.


  	:::shell
    cd $OVRSA
  	./easyrsa gen-dh


Since you'll want this VPN to be as secure as possible, use the following command to generate a tls-auth key. This step is optional, and you can read more about it when the server config file is created below.


    :::shell
    openvpn --genkey --secret $OVRSA/pki/private/ta.key


With that, all of the PKI should be in place. Before we get started making config files, we'll want to protect our PKI by copying it out of the easy-rsa directory. That way if anyone happens to be playing with the `easyrsa` script, something doesn't get accidentally overwritten.


    :::shell
    cp -R $OVRSA/pki $OVPATH/


Be sure that the paths on the `cp` command don't end with `/`.

##The Server config file

With the client & server PKI business out of the way, it's time to configure the server. The good people at [OpenVPN](http://www.openvpn.net) make some pretty great [sample configs](https://openvpn.net/index.php/open-source/documentation/howto.html#examples) available to us, so it makes sense to start with them. Copy the text for the `server.conf` and paste it into `$OVPATH/server.conf` inside your jail. Or grab it with `fetch`


    :::shell
    cd $OVPATH
    fetch https://raw.githubusercontent.com/OpenVPN/openvpn/master/sample/sample-config-files/server.conf


There is very little that will need tweaking in that file. Read through the comments, and adjust as you see fit, but you'll do well to avoid making too many changes. Here are some sections to consider.

###Local IP

    # Which local IP address should OpenVPN
    # listen on? (optional)
    local 10.0.0.248

The `local` config line should reflect the IP address of your jail. In all likelihood, this will be an RFC-1918 private IP address. This is OK.

###Tracking client IPs


  	# Maintain a record of client virtual IP address
  	# associations in this file.  If OpenVPN goes down or
  	# is restarted, reconnecting clients can be assigned
  	# the same virtual IP address from the pool that was
  	# previously assigned.
  	ifconfig-pool-persist /usr/local/etc/openvpn/ipp.txt


This one is pretty self explanatory. Since the default directory may not exist, it's probably best to keep everything contained within `/usr/local/etc/openvpn`.

###Certificate location
In the end, you'll want a config that looks something like what you see below.

  	# Any X509 key management system can be used.
  	# OpenVPN can also use a PKCS #12 formatted key file
  	# (see "pkcs12" directive in man page).
  	ca /usr/local/etc/openvpn/pki/ca.crt
  	cert /usr/local/etc/openvpn/pki/issued/VPNSERVER.crt
  	key /usr/local/etc/openvpn/pki/private/VPNSERVER.key  # This file should be kept secret

  	# Diffie hellman parameters.
  	# Generate your own with:
  	#   openssl dhparam -out dh2048.pem 2048
  	# Substitute 2048 for 1024 if you are using
  	# 2048 bit keys.
  	dh /usr/local/etc/openvpn/pki/dh.pem


I used the commands to get some of the config to look like i wanted.


    :::shell
    sed 's|ca ca.crt|ca '$OVPATH'/pki/ca.crt|' server.conf > /tmp/server.conf
    sed 's|cert server.crt|cert '$OVPATH'/pki/issued/'$VPNSERVER'.crt|' /tmp/server.conf > server.conf
    sed 's|key server.key|key '$OVPATH'/pki/private/'$VPNSERVER'.key|' server.conf > /tmp/server.conf
    sed 's|dh dh2048.pem|dh '$OVPATH'/pki/dh.pem|' /tmp/server.conf > server.conf


If you've followed the steps up to this point, you will just need to swap out the name of the server in the cert and key lines.  If you put your pki directory elsewhere, then adjust the paths as necessary.


###Internal Subnet


  	# Push routes to the client to allow it
  	# to reach other private subnets behind
  	# the server.  Remember that these
  	# private subnets will also need
  	# to know to route the OpenVPN client
  	# address pool (10.8.0.0/255.255.255.0)
  	# back to the OpenVPN server.
  	push "route 10.0.0.0 255.255.255.0"


For this section, you need to know a little bit about your internal network. The IP address in the `push` line should be a representation of your local network. If you don't know what to put here, then from within your jail, run the `ifconfig` command and get your IP address and subnet mask. If you subnet mask is 255.255.255.0, then change the last octet of your IP address to a 0, and use that. Otherwise, jot down your IP address and subnet mask. With those values in hand, visit [www.subnet-calculator.com](http://www.subnet-calculator.com), and enter your IP address into the IP address field. Adjust the subnet mask dropdown to reflect your subnet mask. Using the values on that site, construct the `push` config line as follows:


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


You'll need to `mkdir /var/log/openvpn/` in order for this work. You'll notice that I've stepped outside of `/use/local/etc/openvpn` for this one. You are welcome to put the log file where you want. I always start in `/var/log` when I look for log files, so this makes sense to me.


###Two factor authentication


    plugin /usr/local/lib/openvpn/plugins/openvpn-plugin-auth-pam.so login


You won't find this line in the sample config, and you can consider it to be optional. If you add it in, then in addition to the required certificates, you will need to provide a username and password to connect to the VPN. If you opt for this (and you probably should), there is an line that you will need to add to the client config as well.

##Networking

With the server config finished, we need to deal with the networking. In order to do this, we'll be using [ipfw](https://www.freebsd.org/doc/en/books/handbook/firewalls-ipfw.html), which is built into FreeBSD. You'll need to start by learning the name of the NIC in your jail. You can get this from `ifconfig`. For this example, we will be using `epair10b`. Yours will probably be very similar to that.

Armed with the interface name, you can create `/usr/local/etc/ipfw.rules`:


  	# /usr/local/etc/ipfw.rules
  	ipfw -q -f flush
  	ipfw -q nat 1 config if epair10b
  	ipfw -q add nat 1 all from 10.8.0.0/24 to any out via epair10b
  	ipfw -q add nat 1 all from any to any in via epair10b


In a nutshell, that rule set does this:

  1. flush out all of the existing firewall rules
  1. Define a NAT (number 1) on our interface
  1. Masquerade any outbound traffic from the openvpn network (10.8.0.0) behind the ip on our interface


##Automatic starting

Presumably you will want everything to start automatically. All of that sort of thing is controlled with `rc.conf` in FreeBSD. Add these lines to the end of `/etc/rc.conf`


  	:::config
  	# /etc/rc.conf
  	cloned_interfaces="tun"
  	gateway_enable="YES"
  	firewall_enable="YES"
  	firewall_script="/usr/local/etc/ipfw.rules"

Also, we'll create a special file for the openvpn daemon:


    :::config
    # /etc/rc.conf.d/openvpn
    openvpn_enable="YES"
    openvpn_if="tun"
    openvpn_configfile="/usr/local/etc/openvpn/server.conf"
    openvpn_dir="/usr/local/etc/openvpn/"


With that in place, you can go back to the [FreeNAS](https://www.freenas.org) UI and restart the jail if you want. Or you can run a couple of commands to turn everything on. If you opt to restart the jail, you need'nt execute these commands, and they would only need to be run one time, assuming that you made the changes to `rc.conf` outlined above.


    :::shell
    sysctl net.inet.ip.forwarding=1
    service ipfw start
    service openvpn start


If, like me, you get an error about not being able to start openvpn, then make sure that the `/var/log/openvpn/` directory exists. If that doesn't resolve it, see if `grep error /var/log/messages` returns anything helpful.

##Configuring the client

With the server up and running, the last step is going to be to get a client to connect. There are many different clients that you can use, depending upon your platform. We are going to assume that you are using a unix command line client. There are a bunch of different ways that you can get this installed:

   * FreeBSD:
     * pkg install openvpn
   * Linux:
     * use your package manager to install `OpenVPN`
         * Arch: sudo pacman -S openvpn
         * Debian: sudo apt-get install openpvn
         * RedHat: sudo yum install openvpn
   * OS X (You'll have to do more than just install openvpn, but homebrew should tell you what to do to get the tun/tap driver installed in OS X)
     * brew install openvpn
   * Windows
     * Sorry. No clue. I'm sure google can help you out.

Once you have the `openvpn` binary installed, your client platform of choice shouldn't be of great concern.

###Get the files

In order to keep everything clean, you'll need to create a directory to hold all the stuff:


 	  :::shell
    mkdir ~/.openvpn
    cd ~/.openvpn


There are 4 files on the server that you will need on your client. The jail isn't running ssh, so you can get creative about how you get them back to your client. One option is to copy the contents of the files off of the server and paste them into the files on the client. Or you can start ssh with `service sshd onestart`, but that's really only going to be useful if you've already added in auser in your jail.

The files that you'll need from the server are:


   * `/usr/local/etc/openvpn/pki/ca.crt`
   * `/usr/local/etc/openvpn/pki/private/ta.key`
   * `/usr/local/etc/openvpn/pki/issued/VPNCLIENT.crt`
   * `/usr/local/etc/openvpn/pki/private/VPNCLIENT.key`


##The client config file

With all of the certs in place, it's time to create a client-side config file. Go back to the [OpenVPN sample configs](https://openvpn.net/index.php/open-source/documentation/howto.html#examples) and grab the client config. Paste the contents into `~/.openvpn/VPNSERVER.ovpn`.

If you are still on FreeBSD, you can grab to config like this:


    :::shell
    cd ~/.openvpn
    fetch https://raw.githubusercontent.com/OpenVPN/openvpn/master/sample/sample-config-files/client.conf
    mv client.conf $VPNSERVER.ovpn


As with the server config, there isn't much to change.

###Remote endpoint


   	# The hostname/IP and port of the server.
   	# You can have multiple remote entries
   	# to load balance between the servers.
   	remote 10.0.0.248 1194


For the initial test, you should be able to specify the local IP of the [OpenVPN](https://www.openvpn.org) jail. We'll have to come back and change this later.

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
   	cert VPNCLIENT.crt
   	key VPNCLIENT.key


If they are in a different location, you can use full paths.

###The TLS auth key


   	# If a tls-auth key is used on the server
   	# then every client must also have the key.
   	tls-auth ta.key 1


This key needs to be the same on the client and the server. The `1` parameter indicates that this is a client.

###Two Factor Authentication


 	  # Force username & password authenitcation
    auth-user-pass

    # Disable client-side password caching
    auth-nocache


These are the client-analogue lines to the optional config line in the server that will require a username and password to connect. If you added the optional line to the server config, then you will need to add this to the client config. If you add these lines to the client config without the server lines, then you will be prompted for a username and password that will then be ignored.
If you added this to both configs, then you will need to add a user inside your jail.


###Protecting your keys a bit
The [OpenVPN](https://www.openvpn.org) client will complain about the default permissions on the keys (assuming you have the same umask set as I do), and it is a good practice to at least make it hard for prying eyes to get to our keys. Assuming that you've saved your keys and certs in the same place I have, a quick chmod will put us in a better position.


  	:::shell
  	chmod 600 ~/.openvpn/*.key


##Firing up the test

Save the config file, and fire up a test:


 	  :::bash
    sudo openvpn VPNSERVER.ovpn


Depending upon the specific path that you followed, you may also see various prompts. For example, if you used the `auth-user-pass` option then you will be prompted for a username and password. If you omitted the `nopass` option when you created the client certificate (which is the recommended way), then you'll also be prompted for the passphrase to unlock the client key.

You may see some errors about adding a route. If your test client and your server are on the same network, then the route to that network already exists on the client. If you ignore that for now, you should still get a connection -- useless, but a connection nonetheless.

##Wrapping up
All in all, this didn't change too much from the previous version. The versions of OpenVPN and EasyRSA are the same, so that makes it easy.

Now I have to go file some bugs with FreeNAS about their new UI.
