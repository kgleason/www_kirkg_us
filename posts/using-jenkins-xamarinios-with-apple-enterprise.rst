.. title: Using Jenkins & Xamarin.iOS with Apple Enterprise
.. slug: using-jenkins-xamarinios-with-apple-enterprise
.. date: 2014-03-03 12:22:45 UTC-05:00
.. tags: technology, xamarin, programming, monotouch, jenkins, continuous-integration
.. link:
.. description:
.. type: text

Xamarin released `some documentation`_ recently that talks about using Jenkins_
in a continuous integration set up. Bravo. I read through with rapt anticipation,
only to be let down. Again.

.. _`some documentation`: http://docs.xamarin.com/guides/cross-platform/ci/jenkins_walkthrough
.. _Jenkins: http://www.jenkins-ci.org

I've written `an other blog post`_ about being an Apple Enterprise developer and
the particular challenges that ensue therefrom. In a nutshell, when you are an
enterprise developer developing apps for other people, you have to work closely
with your clients to get the provisioning working correctly. Then the hard part
starts: you need to figure out how to make it all work in Xamarin Studio.

.. _`an other blog post`: http://www.kirkg.us/2013/04/09/continuous-integration-with-monotouch-and-jenkins/

.. TEASER_END

It probably isn't as complicated as I make it sound. It was probably more of a
chore for me because I don't necessarily consider myself a developer yet -- my
background is in systems administration; and that will probably come through as I
go through how I have Jenkins set up, and some of the crazy hacks that we have in
place. Don't get me wrong, it all works; but not all of the development staff
understands (or cares to understand) what is going on with all of this.

Before I dive into the goodies, a description of our set up is in order. Our
bleeding edge software is deployed to the development environment. We send builds
to staging when we think we are ready for release. Once we have everything set
up and ready to go, we deploy to 3 different production-level environments. One
is called "demo" (for the sales team), the next is called "training" (for the
training team), and "production" (where the real stuff happens). Each of these
environments, aside from production, gets it's own build of our application. In
production, the number of builds = number of clients + #. The plus one is for our
internal use.

In order to comply with Apple's rules, each client specific-build get it's own
App ID (to match the provided provisioning profile). Also each environmental
build has a unique application id so that we can have them all installed on our
devices. It took quite a while to come up with a workable soltuion to all of this,
and it has been through quite a few iterations. Over the course of time, I've
learned a lot about solution and project files (remember when I said I wasn't
really a developer), and picked up some pretty decent awk one-liners as well.
Without further ado, here is a step by step of how I've automated this at work to
make it all build the same, every time. I'll start inside Xamarin Studio.

Build Configs
==============

Here are the requirements:

* a specific build per client, each with their own provisioning profile.
* a specific build per environment, for our own internal use.

In order to accomplish this, I started out by standardizing a few things. If you
look inside my solution file, you'll see build configs that looks like this:
CompanyEnvironment, where Company can represent either the name of a client, or
the name of our company:

* BloomDebug
* BloomStaging
* BloomTraining
* BloomDemo
* BloomProduction
* Client1Production
* Client2Production

You get the idea. For each of the build configs, I have configured custom signing
and provisioning profile settings. I don't rely on the BundleID matching that is
built into Xamarin Studio, since it has caused me some headaches in the past.
For each build, I pair up the key, provisioning profile specifically. This ensures
that if the provisioning profile is not present on the build server (or expired),
that the job will fail. Setting up a new client is somewhat involved, since it
involves something along the lines of the following:

#. Open the solution
#. Go into the project options, and set the bundle id to be the one that was assigned to the clients provisioning profile
#. Close the project options (to make it save)
#. Go back into the project options, and set up the signing cert and provisioning profile for the client.
#. close the projection options (to make it save)
#. Go back in and set the bundle id to what it needs to be for development purposes

Speaking of bundle ids, there is also a standard as to how those are chosen:
com.ourawesomeapp.client1 for production builds, and com.ourawesomeapp.environment.bloom
for non-production builds. The reason for all of the rigid standardization will
become obvious as we start looking at what is going on in Jenkins.

Jenkins
========

There are 5 primary build jobs. There are a couple of variations between them,
all for some pretty specific reasons. The various build jobs are:

* Dev
* Staging
* Demo
* Training
* Production

From a Jenkins perspective, some of the differences are significant.

Dev
----

The dev job is the one that is the most cutting edge. It is the one that builds
the bleeding edge of our development, and it is also the one where I test out
changes to Jenkins. This job monitors our source control for changes, and builds
automatically. Since these dev builds are outside our normal deployment and
versioning process, this build is quite a bit different from the rest. This is
also my favorite one, since it is the least user dependent. Here are the build steps:

Versioning
~~~~~~~~~~~

In general, we version our software YYYY.Q.MM.RR where

* YYYY is the 4 digit year
* Q is the 1 digit quarter of the release
* MM is the 2 digit month of the release
* RR is the release number

However for dev, which is continuously built, this doesn't work. Instead we use
the Jenkins build number for the RR portion. Thus the build starts by setting
calculating the version and setting it in a Jenkins variable. The following are
executed in a Jenkins "Execute Shell" build step

.. code-block:: bash

    echo APP_VERSION=$(date +%Y.$(((($(date +%-m)-1)/3)+1)).%m.${BUILD_NUMBER}) > propsfile
    echo CLIENT=dev >> propsfile

Aside from creating the version, we also set a client name, which is dev in this case.

Once we have the values in the newly created "propsfile", we use a Jenkins
"Inject Environment Variables" step to read in the newly set values.

Once we have the Jenkins environment set to use, we take a look at the
Info.plist changes.

Info.plist
~~~~~~~~~~~

In the past, and in the other build jobs, we had multiple versions of Info.Plist,
and we simply delete the one from git, and copy in the appropriate one. However
I've recently discovered the PlistBuddy command, and I have been playing around
with it in the dev Jenkins build. It will probably get moved up the chain before
too long, because it is much cleaner.

In another Jenkins "Execute Shell" step, the following commands are issued:

.. code-block:: bash

    /usr/libexec/PlistBuddy -c "Set CFBundleVersion ${APP_VERSION}" Info.plist
    /usr/libexec/PlistBuddy -c "Set CFBundleIdentifier com.ourawesomeapp.${CLIENT}" Info.plist
    /usr/libexec/PlistBuddy -c "Set CFBundleURLTypes:0:CFBundleURLName com.ourawesomeapp.${CLIENT}-handler" Info.plist
    /usr/libexec/PlistBuddy -c "Set CFBundleURLTypes:0:CFBundleURLSchemes:0 ourawesomeapp-${CLIENT}" Info.plist


Breaking down the first command, we can see that PlistBuddy is basically being
told "set" the value of "CFBundleVersion" to the value of the Jenkins variable
"APP_VERSION" in "Info.plist". There are 4 lines that need to be edited along
the same lines.

Prebuild cleaning
~~~~~~~~~~~~~~~~~~

You can color me old fashioned, but I do like to clean before build. So with
another "Execute Shell" step, I fire off the following command:

.. code-block:: bash

    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -c:"BloomDev|iPhone" -t:Clean OurAwesomeApp.sln


Building
~~~~~~~~~

The final build step is another "Execute Shell" step:

.. code-block:: bash

    /Applications/Xamarin\ Studio.app/Contents/MacOS/mdtool build -t:Build -c:"BloomDev|iPhone" OurAwesomeApp.sln

The the app build, and bundled into a handy IPA, Jenkins deploys it to our
internal deployment server.

Staging, Demo & Training
--------------------------

We use the same versioning scheme, but like to keep the revision number (RR)
predictiable for our clients. As such the formula used in dev can't be used. In
addition, the Jenkins jobs haven't all yet been migrated to using the PlistBuddy
transformations. So we deal with the verisoning a different way.

Info.plist
~~~~~~~~~~~~

.. code-block:: bash

    rm -f Info.plist; cp InfoPlistFiles/Info.plist.staging Info.plist

Essentially we keep a static Info.plist in the code for every different build
that needs to be made. This technique has worked pretty well, but we have to be
careful about changes to the Info.plist file. For example, we recently added
some entitlements, so that change needs to be merged into all of the static
Info.plist files.

Version manipulations
~~~~~~~~~~~~~~~~~~~~~~~

For this, we use a bash script that is an evolution of what we used to use for
the entire build process. It takes a few different parameters.

.. code-block:: bash

    /bin/bash ShellScripts/Version_Environment_Settings.sh -b ${GIT_TAG} -e STAGING

The ${GIT_TAG} is a Jenkins parameter that is used to specify both the version to
build and the tag to checkout. I'll put the script at the end of this post, if
anyone wants to look at it. Essentially what it does is checks to make sure that
it knows everything that it needs to know, and then it does some find and replace
on the overall solution file (.sln), the Project files (.csproj) and the Info.plist.

I've been wondering for a while if some of this isn't overkill. I just haven't
really tested -- afterall if it isn't broken, then it probably doesn't need to
be fixed.

Building
~~~~~~~~~~

The pre-build clean and actual build commands look exactly the same.

All of these Jenkins jobs (staging, demo, training) are run as individual jobs
so that we can make a build for any of them relatively quickly.

Production
------------

The production build job looks almost identical to the Staging, Demo, & Training
jobs. The primary difference is that it is a Matrix job in Jenkins. The Matrix
variables look like this:

.. image:: ../images/Screen_Shot_2014_03_11_at_9_51_39_PM.png

The effect here is that when this job is called, we restrict the builds to the
OS X Build Server (no point in trying to build in Windows or Linux). It creates
a build for Bloom (us), CLient1, Client2, Client3, & Client4.

When you look at the Version_Environment_Settings script below, you probably
will deduce that I pass the ${CLIENT} variable from Jenkins to the script so
that everything gets transformed for the specific client.

Wish List
==========

This article represents a couple of years of figuring things out -- Apple's
provisioning restrictions, Jenkins, Xamarin, etc. When I started this entire
adventure, I really didn't know what I was doing. I just know that I needed a
way for someone other than me to create a build and have it be done in the same
way.

After a couple of years of figuring this all out, there really is only thing
left that really bugs me about the entire process. It would be most excellent if
the AppID in the Xamarin Project options were able to be tied to a specific
Build Config. With that one change, I could elminate a lot of the extra work
just by setting up the build config the way I need.

Aside from that, with a little experimentation, it is possible to figure out how
to use Jenkins to build client specific apps as an Apple Enterprise Developer.

Version\\_Environment_Settings.sh
====================================

Here is the script that was referenced above.

.. code-block:: bash
    :number-lines:

    #!/bin/bash

    #Define a function to output the usage
    function usage {
    		echo "Usage: ${0} -b BUILDNUM -e DEBUG|STAGING|PRODUCTION|DEMO|TRAINING [-c CARRIERNAME]"
    		exit $1
    }

    #Process the command line arguments
    while getopts "b:e:c:" Option
    do
    	case $Option in
    		b) BUILDNUM=${OPTARG};;   # the version number
    		e) TARGETENVIRONMENT=${OPTARG};;   # the environment where this build will be deployed
    		c) CLIENT=${OPTARG};;   # The client this build is for
    	esac
    done

    #Check that we have everything we need
    if [ -z ${BUILDNUM} -o -z ${TARGETENVIRONMENT} ]
    then
    	usage 1
    else
    	GOODENV=0
    	case ${TARGETENVIRONMENT} in
    		DEBUG)		GOODENV=1
    					BLOOMENV="dev";;
    		STAGING)	GOODENV=1
    					BLOOMENV="staging";;
    		PRODUCTION)	GOODENV=1
    					BLOOMENV="production"
    					if [ "X${CLIENT}" == "X" ]
    					then
    						echo "CLIENTNAME (-c) parameter is required for production builds"
    						exit 4
    					fi;;
    		DEMO)		GOODENV=1
    					BLOOMENV="demo";;
    		TRAINING)	GOODENV=1
    					BLOOMENV="training";;
    	esac

    	if [ ${GOODENV} == 0 ]
    	then
    		usage 2
    	fi

    fi

    # We need some date data for building our version number: YYYY-QQ-MM-BB
    YEAR=$(date +%Y)
    MONTH1=$(date +%-m)
    MONTH=$(date +%m)
    QUARTER=$((((${MONTH1}-1)/3)+1))

    # Check out -b parameter. If it is short, then build the VERSION, otherwise use what was passed in
    if [ ${#BUILDNUM} -eq 12 ]
    then
    	VERSION=${BUILDNUM}
    else
    	VERSION="${YEAR}.${QUARTER}.${MONTH}.${BUILDNUM}"
    fi

    #Put the version in a properties file for Jenkins
    echo "APP_VERSION=${VERSION}" > propsfile

    ##############################################################################
    # Modify the Solution (.sln) file
    ##############################################################################

    # Put our version number into the software
    cp OurAwesomeApp.sln /tmp/sln
    awk "/version =/ {sub(\\"20110628b\\", \\"${VERSION}\\")} {print}" /tmp/sln > OurAwesomeApp.sln
    rm -f /tmp/sln


    ##############################################################################
    # Modify AppConfig.cs
    ##############################################################################

    # Set the TargetEnvironment to the appropriate constant
    cp AMA/AppConfig.cs /tmp/AppConfig
    awk "/Environment = TargetEnvironment./ {sub(/(DEBUG|STAGING|PRODUCTION|DEMO|TRAINING)/,\\"${TARGETENVIRONMENT}\\")} {print}" /tmp/AppConfig > AMA/AppConfig.cs
    rm -f /tmp/AppConfig

    ##############################################################################
    # Modify the Info.plist file
    ##############################################################################

    # Put our version number into the software
    cp Info.plist /tmp/plist
    awk "/\\<key\\>CFBundleVersion\\<\\/key\\>/,/\\<key\\>MinimumOSVersion\\<\\/key\\>/ {sub(/\\<string\\>.*\\<\\/string\\>/,\\"\\<string\\>${VERSION}\\<\\/string\\>\\")} {print}" /tmp/plist > Info.plist
    if [ -z ${CLIENT} ]
    then
    	#This is not a production build. Just move one
    	rm -f /tmp/plist
    else
    	sed "s/com.ourawesomeapp.Bloom/com.ourawesomeapp.${CLIENT}/g" Info.plist > /tmp/plist
    	mv -f /tmp/plist Info.plist
    fi

    ##############################################################################
    # Modify the csproj file
    ##############################################################################

    # Put our version number into the software
    cp OurAwesomeApp.csproj /tmp/csproj
    awk "/\\<(Release|Bundle)Version\\>/ {sub(\\"20110628b\\", \\"${VERSION}\\")} {print}" /tmp/csproj > OurAwesomeApp.csproj
    rm -f /tmp/csproj

    # Now we should be ready to build.
