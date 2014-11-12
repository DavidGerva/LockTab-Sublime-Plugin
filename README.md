LockTab
========

This plugin allows you to lock (and unlock) a tab in Sublime.
The plugin tries to remember the position of the tab and also the position of the
focus in the view.

This is my first work and it has not the claim to be complete or perfect.
(It is full of bug. ;)

It is (and will remain) a very simple and essential, but I hope useful, plugin but it can
be improved in a lot of aspects.

Usage
-----
Just right click on the view (right now not on the tab name, see ToDo#4) and Lock/Unlock
the tab.
LockTab.sublime-settings is quite self-explained.


ToDo
----
1. First of all I'm looking for a method for avoiding the normal behavior of sublime.
Right now I just intercept the tab closing, and then I reopen the tab. This is, as far as I
know, the only thing I can do. Right now is not possibile avoiding the tab closure!
Do you know how to do it?

2. One of the most important things to do is to add a particular icon (or also only a different
colour) to the locked tab. I haven't tried it. It could be very easy or impossible. I don't know.

3. Maybe I should improve the code. It just started out as a "bet" in my office. I don't know a lot
neither of phyton nor of sublime plugins.

4. It could be very useful permit the Lock/UnLock of the tab directly from the tab name
and not only on the tab "body". Right now sublime do not give the view ID of the right-clicked
tab name but only of the view on which you have the focus.
Do you know how to do it?

5. Maybe a better english translation of this Readme?

6. Managing more than one group of views. Again didn't try at all.

7. Improving the "set focus" after the reopen