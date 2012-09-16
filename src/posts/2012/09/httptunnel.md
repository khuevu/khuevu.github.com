Date: 2012-09-17
Title: Tunnel TCP through HTTP - A Python Implementation
Tags: http, tcp, tunneling, python
Slug: http-tunnel
Category: Blog

Sometimes you find yourself behind a restrictive firewall. It blocks any request with destination port other than 80. You can do little thing like browsing websites. 

The solution, if you want to access an application at other ports, is to direct your traffic to a server outside the firewall listening at port 80. The server then forwards the data to your desired destination. It also returns any response from that destination, i.e, `tunneling`. 

The tunneling can leverage on existing protocol, like HTTP. I have written a simple tunnel program in Python. It contains two components, tunnel client and tunnel server. 

### Tunnel Server

It is basically a HTTP server which should resides on the host machine outside the firewall. When the server received a request from client, it relies on the request's HTTP method to start the respective action sequence: 

*   POST method: Signal a new connection. Send server the host and port of the target address. Server will establish a TCP connection with the target address.
*   PUT method: Signal write request. Server gets data from request's payload and send to target through the established TCP connection. 
*   GET method: Signal read request. Server get data from target and send back to client as HTTP Response. 
*   DELETE method: Signal end of connection. Server closes the TCP Connection with target.  

You can start the server with command: 

    $python tunneld.py -p 80 

The default port server listens to is 9999. Type `python tunneld.py -h` for help messages. 

### Tunnel Client

Tunnel Client resides on your local machine or any machine within the firewall. It follows the above mentioned protocol to talk to the Tunnel Server. It spawns separate threads to send and receive data from server (through HTTP PUT and GET respectively) and forward back to the local machine through socket.  

To start the client: 
    
    $python tunnel.py [target_host]:[target_port]

### Testing

To test the Tunnel, for example, tunneling IRC connection, we use linux `nc` command: 

First, start the tunnel service:
    
    $python tunneld.py -p 80
    $python tunnel.py -p 8889 -h localhost:80 irc.freenode.net:6667

Connect to the client using `nc` and send IRC messages: 
    
    $nc localhost 8889 
    NICK abcxyz
    USER abcxyz abcxyz irc.freenode.net :abcxyz

Result: 

    :calvino.freenode.net NOTICE * :*** Looking up your hostname...
    :calvino.freenode.net NOTICE * :*** Checking Ident
    :calvino.freenode.net NOTICE * :*** Found your hostname
    :calvino.freenode.net NOTICE * :*** No Ident response
    NICK abcxyz
    USER abcxyz abcxyz irc.freenode.net :abcxyz
    :calvino.freenode.net 001 abcxyz :Welcome to the freenode Internet Relay Chat Network abcxyz
    :calvino.freenode.net 002 abcxyz :Your host is calvino.freenode.net[213.92.8.4/6667], running version ircd-seven-1.1.3
    :calvino.freenode.net 003 abcxyz :This server was created Sun Dec 4 2011 at 14:42:47 CET
    :calvino.freenode.net 004 abcxyz calvino.freenode.net ircd-seven-1.1.3 DOQRSZaghilopswz CFILMPQbcefgijklmnopqrstvz bkloveqjfI
    :calvino.freenode.net 005 abcxyz CHANTYPES=# EXCEPTS INVEX CHANMODES=eIbq,k,flj,CFLMPQcgimnprstz CHANLIMIT=#:120 PREFIX=(ov)@+ MAXLIST=bqeI:100 MODES=4 NETWORK=freenode KNOCK STATUSMSG=@+ CALLERID=g :are supported by this server
    :calvino.freenode.net 005 abcxyz CASEMAPPING=rfc1459 CHARSET=ascii NICKLEN=16 CHANNELLEN=50 TOPICLEN=390 ETRACE CPRIVMSG CNOTICE DEAF=D MONITOR=100 FNC TARGMAX=NAMES:1,LIST:1,KICK:1,WHOIS:1,PRIVMSG:4,NOTICE:4,ACCEPT:,MONITOR: :are supported by this server
    :calvino.freenode.net 005 abcxyz EXTBAN=$,arx WHOX CLIENTVER=3.0 SAFELIST ELIST=CTU :are supported by this server
    :calvino.freenode.net 251 abcxyz :There are 232 users and 70582 invisible on 31 servers
    :calvino.freenode.net 252 abcxyz 45 :IRC Operators online
    :calvino.freenode.net 253 abcxyz 10 :unknown connection(s)
    :calvino.freenode.net 254 abcxyz 34513 :channels formed
    :calvino.freenode.net 255 abcxyz :I have 6757 clients and 1 servers
    :calvino.freenode.net 265 abcxyz 6757 10768 :Current local users 6757, max 10768
    :calvino.freenode.net 266 abcxyz 70814 83501 :Current global users 70814, max 83501
    :calvino.freenode.net 250 abcxyz :Highest connection count: 10769 (10768 clients) (2194912 connections received)
        ...


### It needs not be HTTP

Here I use tunneling tcp packages through HTTP protocol. It is an existing protocol, which gives the reusability to the program. But you can implement your own program on top of the tunneling TCP Connection. You just need to define your own application layer protocol on how the two end of the tunnel communicate, i.e, when to start sending data, when the data ends...

You can access the source code of the program [here](https://github.com/khuevu/http-tunnel)


    



