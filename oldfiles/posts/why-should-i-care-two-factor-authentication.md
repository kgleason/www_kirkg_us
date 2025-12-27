<!-- 
.. title: Why Should I Care: Two Factor Authentication
.. slug: why-should-i-care-two-factor-authentication
.. date: 2015-11-13 17:27:49 UTC-05:00
.. tags: why should I care, 2fa, two factor auth
.. category: wsic
.. link: 
.. description: 
.. type: text
-->

You know how when you use your debit card at an ATM or at a point of sale, you have to provide your PIN before your transaction can be completed? It makes perfect sense, right? With out the PIN, anyone who find yours debit card would be able to use it as if they were you. No good. Who wants that?

<!--TEASER_END -->

In the world of security, there are 3 generally accepted ways of proving that you are who you claim to be. Otherwise put, there are 3 categories of authentication factor:

1. Something you are. Think of this one as the stuff you see in movies: fingerprint scanner, retina scanners, anything biological.
1. Something you have. This would be some sort of token that you carry on your person: a debit card, a key, a USB drive, what have you
1. Something you know. In order to get this one, it will need to be extracted from your brain.

If you go back to the debit card scenario, you can see that in order to use the card to effect a transaction, you have to provide 2 factors: the card itself (something you have) and your PIN (something you know). Even if you lose your debit card, then someone would need to guess your password in order to be able to get access to your money. 

Now let's change contexts for a little bit. Being the suave modern reader that you are, you probably have all kinds of accounts. You probably have a Facebook account, a Twitter account, an online banking account, an account with your health insurance company, your ISP, your credit card company -- the list could go on for quite some time. In addition to all of that, you also probably have an email account.

Now if I were a nefarious type of person -- the type of person who might steal your wallet from you, or be interested in getting access to your online accounts -- I'd start out by targeting your email account. If I can get access to your email account, then I can reset all of your passwords and get access to all of your other accounts.

Holy crap! Am I right?

In fact, there is a pretty basic step that you can take to help protect yourself. It's called 2 factor authentication, and as I've already demonstrated, you probably already do this all of the time. 

Most major email providers should do this -- if your's doesn't then switch to one that does. For the most part, how it will work is that when you attempt to log in to your account, you will need to verify that you are who you claim to be. Frequently, there will be a couple of different ways to do this. You can get a text message with a code. You can use an app that has been tied to your account to generate a code. You can get a phone call where a code will be read to you by a computer. Think of this code as your PIN. The only difference is that this code will expire after a pretty short amount of time -- 60 seconds to an hour, depending upon the final solution.

When you enable 2FA (two factor authentication), you'll have to register a device -- either by scanning a barcode, or by answering a text or a phone call.  Onc your device is set up, the next time you attempt to log in, then you'll need to use that specific device in order to get the code that you'll need -- the PIN, as it were.

That way, even if your pasword is compromised, an underhanded person would then need your phone in order to be able to use that password.

The great part is that many other accounts (aside from email) probably support 2FA -- Facebook does, as does Twitter.

That is definitely a good thing, because odds are good that if I get your email password, then I probably have your password to all of yor other accounts anyhow.