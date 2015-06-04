# [ClickOnce](http://en.wikipedia.org/wiki/ClickOnce)

ClickOnce is a fairly old technology that ships with .Net 2.0. It basically installed application in a few clicks, and is shipped with some versioning control on clients' side, as well as some security stuff I don't care of.

As we know, MS has no good application pulishment mechanism at all, which means you have to deal with installer. So either an installer has to contain all the dependencies in one pack, as 99% of them in the market, or you as a client has to deal with dependencies alone, which I met once or twice in my life. And both of them are bad, too old, back in 70s.

So why ClickOnce doesn't become the main stream of app publishment in MS ecosystem? Well, from my stand point, there are two reasons:

1. It's targetting for small app so it's not scalable.
2. Very poor support for team development and multi-environment development.

So poor me once chose ClickOnce because of the easiness of installing and updating. But ended up feeling bad because the second point I mentioned above.

## What does this script do

It basically builds and publishes ClickOnce app to specified positions.


## HOWTO? 

This script is interactive, but first of all, env's need to be set up.

`target_shares` is in big focus:

```python
target_shares = {
    'release': [],
    'test'   : [],
    'dev'    : []
    }
```

Keys of it are environments, and a list under each contains target positions to publish to.

Example:

```python
target_shares = {
    'release': [r'C:\release']
    }
```

Now I've added `C:\release` to one of my release target folders.

Then double click the file to run it.

### Extra

This scripts will modify the assembly name of the ClickOnce app to avoid them having installed in the same directory, such that you can install multiple instances in one account in one box.

## More Complaints and Regrets

ClickOnce is bad, generally speaking, as bad as the rest from MS. The same as other software from MS, for the first glance, it shines, for the second glance, it works, for the thrid glance, it sucks.

### It Shines

It's very easy to have(force) clients update to the version you want them to. And some manifest stuff and security comes with it, to avoid third party to inject dlls as an update(propably not as well as stated though).

Compare to the old way(copy-and-paste exe, self-extraction app, extra updater), it eases your life.

### It Works

Well, it works.

### It Sucks

Ok, here is the thing. Management of ClickOnce is done in VS. I can't imagine that's even a design. Following is a scenario:
<pre>
**A**                                   **B**                                 **Target share**
Start version 1.0.0.0                   Start version 1.0.0.0                 Empty
developing                              published                             1.0.0.0 from B
check in                                developing, no check in               -
publish(still 1.0.0.0)                  -                                     ????
</pre>

so what do you expect happens to Target share??

<pre>
Another problem:
**A**                                   **B**                                 **Target share**
Manually increase version to 2.0.0.0    -                                     1.0.0.0 from B
publish                                 -                                     2.0.0.0 from A
-                                       publish                               ????
</pre>

wtf?!!

There are more similar problems to prevent you from working with others, like lack of support for multiple environment.

Another problemetic setting, is ClickOnce basically gets built into two modes: offline, online. 

In online mode

* it forces to update to the latest version
* you need to have access to the share
* the installation folder is somewhere in your `appData\` folder hidden deeply
* when you don't need it you don't have a clean way to uninstall it
* you can't attach it to task bar or start menu easily

In offline mode

* you can choose to not to update to the latest version
* you don't have to access to the share after install
* you can unistall it from control panel
* it attaches to task bar and start menu automatically

What I need
* from online, I need clients always up to date
* from online, users shall always have access to the share
* from offline, I need clients to be easy to unistall
* from offline, I need clients to be able to attach to whatever places the users want it to

but I can't make it without writing my own script. GJMS, really GJ.

### Conclusion

ClickOnce is counter-cooperative. It's targeting small apps.
