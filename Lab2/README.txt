- How is Select Implemented?
https://www.quora.com/Network-Programming-How-is-select-implemented

do_select() has a giant loop which is basically the meat of select, which will generally speaking does 
the following:
Traverses all the fds supplied
Executes an appropriate poll callback on each fd
Set an appropriate bit in the previously allocated bitmap for for each fd polled
Towards the end of the loop, it will check for timeouts, and if so break

This giant loop is exactly why most newer high performance webservers such as node.js, Tornado and 
lighttpd use epoll over select, since when you have lots of file descriptors ( say 10s of thousands fds 
), that polling gets slow.



- Why is epoll faster than select?
https://stackoverflow.com/questions/17355593/why-is-epoll-faster-than-select

Ironically, with select, the largest cost comes from checking if sockets that have had no activity have 
had any activity. With epoll, there is no need to check sockets that have had no activity because if 
they did have activity, they would have informed the epoll socket when that activity happened. In a 
sense, select polls each socket each time you call select to see if there's any activity while epoll 
rigs it so that the socket activity itself notifies the process.


- Julie Evans: Async IO on Linux: select, poll, and epoll
https://jvns.ca/blog/2017/06/03/async-io-on-linux--select--poll--and-epoll/

why don’t we use poll and select?
Okay, but on Linux we said that your node.js server won’t use either poll or select, it’s going 
to use epoll. Why?

From the book:

On each call to select() or poll(), the kernel must check all of the specified file descriptors to see 
if they are ready. When monitoring a large number of file descriptors that are in a densely packed 
range, the timed required for this operation greatly outweights [the rest of the stuff they have to do]

Basically: every time you call select or poll, the kernel needs to check from scratch whether your file 
descriptors are available for writing. The kernel doesn’t remember the list of file descriptors 
it’s supposed to be monitoring!


level-triggered vs edge-triggered
Before we talk about epoll, we need to talk about “level-triggered” vs “edge-triggered” 
notifications about file descriptors. I’d never heard this terminology before (I think it comes from 
electrical engineering maybe?). Basically there are 2 ways to get notifications

get a list of every file descriptor you’re interested in that is readable 
(“level-triggered”)
get notifications every time a file descriptor becomes readable (“edge-triggered”)


what’s epoll?
Okay, we’re ready to talk about epoll!! This is very exciting to because I’ve seen epoll_wait a 
lot when stracing programs and I often feel kind of fuzzy about what it means exactly.

The epoll group of system calls (epoll_create, epoll_ctl, epoll_wait) give the Linux kernel a list of 
file descriptors to track and ask for updates about whether

Here are the steps to using epoll:

1. Call epoll_create to tell the kernel you’re gong to be epolling! It gives you an id back
2. Call epoll_ctl to tell the kernel file descriptors you’re interested in updates about. 
Interestingly, you can give it lots of different kinds of file descriptors (pipes, FIFOs, sockets, POSIX 
message queues, inotify instances, devices, & more), but not regular files. I think this makes sense 
– pipes & sockets have a pretty simple API (one process writes to the pipe, and another process 
reads!), so it makes sense to say “this pipe has new data for reading”. But files are weird! You 
can write to the middle of a file! So it doesn’t really make sense to say “there’s new data 
available for reading in this file”.
3. Call epoll_wait to wait for updates about the list of files you’re interested in.



- How do system calls like select() or poll() work under the hood?
https://stackoverflow.com/questions/11496059/how-do-system-calls-like-select-or-poll-work-under-the-hood


