<!--
.. title: Continuous Integration with MonoTouch and Jenkins
.. slug: continuous-integration-with-monotouch-and-jenkins
.. date: 2013-04-09 13:24:14 UTC-05:00
.. tags: technology, xamarin, programming, monotouch, jenkins, continuous-integration
.. link:
.. description:
.. type: text
-->

A couple of years ago at work we started developing a mobile application. None
of us had any mobile experience to speak of, so we read some books. As we began
debugging early versions of the app, we learned pretty quickly that we needed a
standardized build process.

At the time we knew of solutions like Jenkins, but didn't really know where to
begin. Since the developers were pretty swamped with development and debugging,
I took on the responsibility of trying to standardize the build process. I'm not
really a programmer, and I didn't really know how solution and project files work.
Since we were working in MonoDevelop rather than in Visual Studio, none of the
devs really had time or capacity to stop and take a look at the options that
were there.

.. TEASER_END

For a couple of months, I was the one who made all of the builds, manually. It
was a pretty tedious process: checkout, open in MonoDevelop, set options, build,
create the IPA package manually, push to the deployment server, edit the options
in the server side plist file, and reset. I got sick of that pretty quickly. So
I started writing a bash script that would handle it all for me.

Part of my frustration that I have had up until recently (and even still now
somewhat) stems from the Apple provisioning process. The app that we were
developing was never intended for the app store. We develop apps for corporate
customers, which means that all of our distribution is done via what Apple calls
"In house enterprise distribution." This means that for each customer we have, we
need to sign the code with their code signing key and provisioning profile. Since
provisioning profiles are related to application ID, the application ID needs to
change for each customer. This allows us to install multiple builds of the app
on a single iPad so that we can test for each customer.

Fast forward 2 years, and an oft-updated version of that script still exists. As
it stands right now, here is the high level of what this script does:

* Process the 6 possible command line options
* Set the 25 various variables this script has evolved to use.
* Begin a loop for each of our customers
* Begin another loop for each of our potential build environments (dev, staging, training, demo, production)
* Use ``awk`` & ``sed`` to make changes (8 of them) to the csproj file.
* Use ``echo | cat > Info.plist << ENDEND`` to do some variable substitution on an Info.plist template that is embedded in the script.
* ``awk`` a change in the solution file
* call ``mdtool`` with the appropriate parameters
* end the environments loop
* end the customers loop

This script has served us pretty well for the last 2 years, but we've found that
this sort of solution is extremely fragile. As an example,  here is a line from
the step where I make changes to the csproj file.

.. code-block:: bash

    # Put our version number into the software
    awk "/\<(Release|Bundle)Version\>/ {sub(/201[1-9][0-9]{4}[a-z]/, "${VERSION}")} {print}" /tmp/csproj1 > /tmp/csproj2

That command, in case you aren't familiar with awk or regex, will search the file
named ``/tmp/csproj1`` for a pattern that essentially is designed to match '20120626b'
and then replace it with my ${VERSION} variable. The problem is that if someone
changes the '20120626b' value with something that doesn't match the pattern, then
the app will be built with the incorrect version, and this will eventually cause
problems with the enterprise deployment. The main developers have all of these
sorts of files set to ignore in our SCM, but when someone who is helping through
a crunch else commits changes, then there is some lost time trying to track down
the problem.

About 2 weeks ago, I was tasked with creating a repeatable way of building an
Android version of our app. It's here that I was introduced to XBuild. When I saw
how easy it was to set up a MonDroid project to build via Jenkins, I started
thinking that there had to be an easier way. I sort of found it, and what comes
next is a description of how I have things set up right now.

My ultimate goal here is to find a way to do all of this without all of the shell
manipulations, and to be able to set up a matrix job in Jenkins to make all of our
production builds. I'm close, but still not there yet, as you can see below.

I started by moving all of the private & public keys, and the signed certs from
Apple into a their own keychain with a password that I don't mind having exposed
in a shell script. Then in my release configuration for the MonoTouch project, I
added a custom pre-build command. The excerpt from the project files looks similar
to this:

.. code-block:: xml
    :number-lines:

    <CustomCommands>
      <CustomCommands>
        <Command type="BeforeBuild" command="bash -c "security unlock-keychain -p 'SuperSecretPassword' ${HOME}/Library/Keychains/iPhoneStuff.keychain"" />
      </CustomCommands>
    </CustomCommands>

That little tidbit allows the code sign step to happen via SSH (after it has been
run at least one time from the build server to allow the keychain to be accessed).

Now that I can build the app via SSH, I started figuring out how to make all of
this work with Jenkins. The command from the previous build script looked like this:

.. code-block:: bash

    "/Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool" build --configuration:"Release|iPhone" OurAwesomeApp.sln

As I started digging in, I found that a lot of the manipulations that I was doing
with `awk` in the build script could be accomplished through a custom build
configuration. After some tweaking, I ended up with something that looks like this:

.. code-block:: xml
    :number-lines:

    <PropertyGroup Condition=" '$(Configuration)|$(Platform)' == 'ClientProduction|iPhone' ">
    <DebugType>none</DebugType>
    <Optimize>false</Optimize>
    <OutputPath>bin\iPhone\Release</OutputPath>
    <DefineConstants>MTOUCH</DefineConstants>
    <ErrorReport>prompt</ErrorReport>
    <WarningLevel>4</WarningLevel>
    <MtouchLink>None</MtouchLink>
    <MtouchI18n />
    <MtouchArch>ARMv7</MtouchArch>
    <IpaPackageName>OurAwesomeApp-Client</IpaPackageName>
    <ConsolePause>false</ConsolePause>
    <CustomCommands>
      <CustomCommands>
        <Command type="BeforeBuild" command="bash -c "security unlock-keychain -p 'Super Secret Password' ${HOME}/Library/Keychains/iPhoneStuff.keychain"" />
      </CustomCommands>
    </CustomCommands>
    <BuildIpa>true</BuildIpa>
    <CodesignKey>iPhone Distribution: Enterprise Distribution Key</CodesignKey>
    <CodesignProvision>FFFFFFFF-FFFF-FFFF-FFFF-FFFFFFFFFFFF</CodesignProvision>
    </PropertyGroup>

That's a huge step in the right directions, so I created a Jenkins job, and set
it up to issue these commands over SSH:

.. code-block:: bash
    :number-lines:

    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -t:Clean -c:"ClientProduction|iPhone" OurAwesomeApp.sln
    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -t:Build -c:"ClientProduction|iPhone" OurAwesomeApp.sln


Seemed like good things were about to happen. But I started right out with an
error about the AppID not matching the Provisioning Profile, and the job ended
with failure. So I needed to find a way to change the AppID on the fly.
Unfortunately, the AppID is not in the Project or Solution file, but in
Info.plist, which doesn't change based on build type. So back to the shell. *sigh*

At this point there were a couple of different options about how to move forward.
In the end, I made a copy of Info.plist and named it Info.plist.Client. Since
Jenkins is aware of the client that it is building for, I'm able to change the
Jenkins steps to look like this:

.. code-block:: bash

    rm -f Info.plist; cp Info.plist.Client Info.plist
    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -t:Clean -c:"ClientProduction|iPhone" OurAwesomeApp.sln
    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -t:Build -c:"ClientProduction|iPhone" OurAwesomeApp.sln

That ended up solving a 2 different issues -- Bundle Display Name & Bundle Identifier.
With everything set up this way, the build was able to succeed, but was
undeployable. As it turns out, the Version of the app is not being set anywhere,
and when using Enterprise deployment, the version number needs to be correct. Since
the version exists in both the Solution file and the csproj file, there didn't
seem to be a great way to handle this.

A distilled version of the original shell script seemed to be the solution. It
accepts a couple of parameters, and is now part of the project. Jenkins executes
the script before cleaning.

.. code-block:: bash

    rm -f Info.plist; cp Info.plist.Client Info.plist
    /bin/bash ShellScripts/Version_Environment_Settings.sh -b ${VERSION} -e PRODUCTION
    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -t:Clean -c:"ClientProduction|iPhone" OurAwesomeApp.sln
    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -t:Build -c:"ClientProduction|iPhone" OurAwesomeApp.sln

The relevant sections of the script look like this:

.. code-block:: bash
    :number-lines:

    ##############################################################################
    # Modify the Solution (.sln) file
    ##############################################################################

    # Put our version number into the software
    cp OurAwesomeApp.sln /tmp/sln
    awk "/version =/ {sub("20110628b", "${VERSION}")} {print}" /tmp/sln > OurAwesomeApp.sln
    rm -f /tmp/sln

    ##############################################################################
    # Modify the csproj file
    ##############################################################################

    # Put our version number into the software
    cp OurAweomseApp.csproj /tmp/csproj
    awk "/\<(Release|Bundle)Version\>/ {sub("20110628b", "${VERSION}")} {print}" /tmp/csproj > OurAwesomeApp.csproj
    rm -f /tmp/csproj

    # Now we should be ready to build.

With all of this in place, Jenkins will build, but some of the old problems still
exist. Namely, there is still opportunity for a commit to the Project or Solution
file to cause issues with the deployment.

I suspect that the reason that we have these problems is that most people are not
constantly changing their BundleIDs since when dealing with the App Store, it does
not seem to be a recommended practice.

I've love to hear from anyone about a better way to handle this. A link to a how-to
would be even better.
