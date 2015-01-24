.. title: Jenkins, Xamarin.iOS, & Calabash -- putting it all together
.. slug: jenkins-xamarinios-calabash-putting-it-all-together
.. date: 2014-03-23 12:22:12 UTC-05:00
.. tags: technology, xamarin, programming, monotouch, jenkins, calabash, continuous-integration
.. link:
.. description:
.. type: text

We've recently begun writing automated UI tests in Calabash_  for our main
Xamarin.iOS_ project. While the tests are still under development, I decided to
make a Jenkins_ job to fire off the the UI tests whenever a change was detected
on the branch where the tests were being developed.

.. _Calabash: http://calaba.sh/
.. _Xamarin.iOS: http://xamarin.com/ios
.. _Jenkins: http://jenkins-ci.org/

It took a little more than I was expecting to getting it running, so it is
going to become the 2nd article in my impromptu series about Jenkins and Xamarin.

Jenkins in this case, is running on a Mac Mini running the most recent version
of OS X (10.9.2) as a slave:

.. image:: ../images/JenkinsSlaveConfig.png

I like this configuration because it makes it easier for me to test -- if I can
get it to run via SSH, then I can get it to run in Jenkins. In this case I think
it may have also added an additional layer of complexity, but I learned a
couple of things along the way.

My first step was to checkout the branch where the Calabash tests were begin
written, and run all of the build step manually in the Terminal via the UI. A
sanity check if you will. The commands looked something like this (most of these
commands are explained in a previous article_.

.. _article: https://www.kirkg.us/2014/03/11/jenkins-xamarin-apple-enterprise/

.. code-block:: bash
    :number-lines:

    #Unlock the keychain
    security unlock-keychain -p \"My supersecret keychain password\" \"${HOME}/Library/Keychains/login.keychain\"

    #Set some environment variables to make it sort of like a Jenkins env
    WORKSPACE=/Users/builder/Projects/OurAwesomeApp
    BUILD_NUMBER=0
    APP_VERSION=$(date +%Y.$(((($(date +%-m)-1)/3)+1)).%m.${BUILD_NUMBER})
    CLIENT=dev

    #Run through the Info.plist modifications
    /usr/libexec/PlistBuddy -c \"Set CFBundleVersion ${APP_VERSION}\" Info.plist
    /usr/libexec/PlistBuddy -c \"Set CFBundleIdentifier com.ourawesomeapp.${CLIENT}\" Info.plist
    /usr/libexec/PlistBuddy -c \"Set CFBundleURLTypes:0:CFBundleURLName com.ourawesomeapp.${CLIENT}-handler\" Info.plist
    /usr/libexec/PlistBuddy -c \"Set CFBundleURLTypes:0:CFBundleURLSchemes:0 ourawesomeapp-${CLIENT}\" Info.plist

    #Clean the solution
    /Applications/Xamarin\\ Studio.app/Contents/MacOS/mdtool build -c:\"Debug|iPhoneSimulator\" -t:Clean OurAwesomeApp.sln

    #Build the solution
    /Applications/Xamarin\\ Studio.app/Contents/MacOS/mdtool build -t:Build -c:\"Debug|iPhoneSimulator\" OurAwesomeApp.sln


The next step was to issue the ``cucumber`` command, which ultimately failed
(after spending some time laughing at me). Turns out that building for the simulator
doesn't cause the app to get pushed to the simulator, which is what is needed for
Cucumber to execute correctly.

At this point, I opened the solution up in Xamarin Studio and built again, this
time with the deployment to the simulator. I kept my eye on the Build Output
screen, which ends up outputting most of the commands that are issued behind the
scenes when you tell Xamarin Studio to build. I found a command that seemed like
it would do the trick, so I copied it out into an editor, and tweaked it to make
it suit my needs.

.. code-block:: bash
    :number-lines:

    /Developer/MonoTouch/usr/bin/mtouch -sdkroot \"/Applications/Xcode.app/Contents/Developer\" \
    --cache \"${WORKSPACE}/obj/iPhoneSimulator/Debug/mtouch-cache\" --nomanifest --nosign \
    -sim \"${WORKSPACE}/bin/iPhoneSimulator/Debug/OurAwesomeApp.app\" \
    -r \"${WORKSPACE}/MTSplitViewLib/MTSplitViewLib/bin/Debug/MTSplitView.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/System.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/System.Xml.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/System.Core.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/System.Web.Services.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/System.ServiceModel.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/System.Runtime.Serialization.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/Mono.Data.Sqlite.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/System.Data.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/monotouch.dll\" \
    -r \"/Developer/MonoTouch/usr/lib/mono/2.1/MonoTouch.Dialog-1.dll\" \
    -r \"${WORKSPACE}/Assemblies/FlyoutNavigation.dll\" \
    -r \"${WORKSPACE}/Components/calabash-1.5/lib/ios/Calabash.dll\" \
    -debug -nolink -sdk \"6.1\" -targetver \"6.0\" \
    --abi=i386 \"${WORKSPACE}/bin/iPhoneSimulator/Debug/OurAwesomeApp.exe\"


That's a whopper of a single command, but as I understand it from the `mtouch`
documentation_, it pretty much is just defining the build environment -- telling
mtouch explicitly where to find the SDK to build against, which assemblies to
include in the build, etc. The command that I got out of the IDE had a lot of
specific paths, and I did a find/replace job on them so that it could all be
relative to the Jenkins ${WORKSPACE}.

.. _documentation: http://docs.xamarin.com/guides/ios/advanced_topics/mtouch

In the future I'm going to revist this command. It makes the build job brittle
in that if we remove, say, 'MTSplitView.dll' from the main solution, then this
command will break the build process. When I find a way to make it more flexible,
I'll update this post.)

After running that command in the Terminal, and then starting the simulator
manually, I did find the newest version of the app in my simulator. Yippee!!
Now ``cucumber`` would run and all of the tests would run on the build server.

Seemed as if I was in pretty good shape, so I ssh'd into the same build server,
as the same user that I was logged in as, and ran the whole thing again.
Everything ran perfectly up to the point where cucumber started. Then it started
laughing at me again.

After some Googling & testing, I figured out that the very first time I would
walk through my process in the UI, I would get a prompt to enter my password.
It always happened after I would execute the ``cucumber`` command, and after the
simulator had started, but before the tests started. I didn't pay much attention
to it the first time around, and since I resolved most of the problems in the UI
in a single session, I never got prompted again.

My SSH session was trying to prompt, but had no UI to display the prompt on, so
it was just choking, waiting for me to authorize cucumber's request to control
the simulator. There are quite a few threads about this on the internets, but
they were all a little dated, and none of them worked quite right for me (which
is what inspired this article).

The first step was to make my builder account a developer:

.. code-block:: bash

    /usr/sbin/DevToolsSecurity -enable


That command is in my history for that day a couple of times. Sometimes without
the fully qualified path, and sometimes with `sudo`. I don't have great notes
so I don't know exactly which one did the trick, but this output let's me know
that one of them did it:

.. code-block:: bash

    ~$ /usr/sbin/DevToolsSecurity
    Developer mode is already enabled.


The next step, according to what I had managed to scrape up from Google, was to
allow the taskport privilege to be assigned without prompting.

Before executing this next command, I did some research_  `on it`_. I encourage
you to do the same. As I understand it, the following command will allow a process
running as your user to take control of another process running as your user.
While it is exactly what we want in this case, it is generally something that is
allocated on the fly. This command will make the temporary allocation permamnent.
There is a chance that this could be used against you. Consider yourself warned.

.. _research: https://developer.apple.com/library/mac/documentation/Darwin/Reference/Manpages/man8/taskgated.8.html
.. _`on it`: http://www.dssw.co.uk/reference/authorization-rights/index.html

.. code-block:: bash

    sudo security authorizationdb write system.privilege.taskport allow


The output from that command was encouraging:

.. code-block:: bash

    YES (0)


so I ran cucmber again (from SSH), and lo and behold, it worked. Needless to say,
I was very excited. I logged out, and ssh'd in again, and it worked again. Which
lead me to the conclusion that Developer mode only needed to be enabled once,
and the `security authorization` command did not need to be reissued everytime.

I added this command as my last Execute Shell in the build process in Jenkins:

.. code-block:: bash

    cucumber


and fired off the job. It ran without issue.

Next someone asked if there was a way to get a report from ``cucumber``, and it
turns out that there is. I modified the last step to

.. code-block:: bash

    cucumber -f html -o CucumberResults_${BUILD_ID}_${BUILD_NUMBER}.html

and then used a post-build **Send build artifacts over SSH** to copy that html
file and all of the screen shots over to an apache server that indexes the reports:

.. image:: ../images/Screen_Shot_2014_03_23_at_2_09_04_PM.png

Pretty cool right? Clicking on one of those folders takes you right into the
report for that specific build.

This introduced the need to do some additional cleanup at the beginning of the
build, so I added a new **Execute Shell** as the first step of the build:

.. code-block:: bash

    rm -f CucumberResults*.html screenshot_*.png


It's not very elegant, but it does get the job done.

I was ready for my final test, before I put this one to bed for a while. So I
fired the job, and it failed. Ugh.

Turns out that one of the Calabash tests had failed, which caused ``cucumber`` to
exit with a non-zero status. This cause Jenkins to consider the build failed,
which meant that the report was not copied over, so we couldn't really see what
had happened.

I decided to take the easy way out. I modified the ``cucumber`` step in Jenkins to look like this:

.. code-block:: bash

    cucumber -f html -o CucumberResults_${BUILD_ID}_${BUILD_NUMBER}.html || true


which will cause the command to always return 0, thereby tricking Jenkins into
always thinking that ``cucumber`` exited cleanly. There is probably a more elegant
way to solve that problem, but for the time being, it works.

Now as the developers are working on bugs and new features, they are able to
write the UI tests for Calabash, and submit them. For the time being, it is
still all living in a separate git branch. Jenkins is monitoring that branch,
and when changes are pushed to it, Jenkins fires off. Once it is all merged back
into master, then Jenkins will be modified -- and we will probably begin running
our UI tests nightly.

Of course it isn't quite as good as I want it to be yet. I still have the following
things that I need to figure out (so stay tuned, it will be showing up here as
soon as I figure it all out):

* specifying the OS version to run in the simulator. Right now, the simulator starts with whatever the last version was run. I'd like to be able to have it run on every version of the simulator that is installed & that we are currently supporting (right now that is 3 versions of iOS).
* making it run on an actual device. The first rule of app development is don't do all of your testing in the simulator. It's a good rule, and I want to follow it.
* making it all work in Android.

In fact I have a lot of Android work yet to do...
