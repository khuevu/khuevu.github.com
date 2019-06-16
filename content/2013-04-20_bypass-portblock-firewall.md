Title: Bypass port block by firewall with Tor
Tags: firewall, tunnel
Category: Technology
Image: https://upload.wikimedia.org/wikipedia/commons/1/15/Tor-logo-2011-flat.svg
Summary: Tor has a network of so-called Tor bridges that can forward your data to the desired destination anonymously. This article discusses how you can setup Tor to work around firewall port restrictions.

Your network adminstrator often configure the firewall to only allow certain port for outgoing TCP connection like 80 (HTTP), 443 (HTTPS), 22 (SSH). It is a problem if the application you are using relies on other ports to communicate to outside world, for example, IRC, git. 

One solution is to find an alternative endpoints for the external services, which uses the open ports. For example: use https for git, web client for irc, but they are not always available. 

The second solution which is more generic is to have an external HTTP/SOCK proxy (proxy outside of the firewall) and configure your application to use the proxy accordingly.

The third solution is to setup a kind of tunnel. The local end will receive application packages, encapsulate them and send over to a remote end, which listens on one of the open ports. The remote end will be responsible to unwrap the packages and forward them to the desired destinations. This method is called tunneling, you can use existing program like SSH, which relies on a ssh connection. I have written a [tunnel program]({filename}/2012-09-10_httptunnel.md) using HTTP connection, which can come in handy in case the network admin decides to block port 22 too. 

But what if you don't have a server outside of the firewall? Tor is one of the resource that you can leverage with their network of Tor bridges.

To setup Tor, first, download it from [here](https://www.torproject.org/download/download-easy.html.en)

Go to the installation folder. In your `./Data/Tor/torrc` config file, update these entry: 

    #!bash
	ReachableAddresses *:80,*:443
	ReachableAddresses reject *:*
	SocksListenAddress 127.0.0.1
	SocksPort 9150

The ReachableAddresses are addresses your firewall allows you to connect. 
`SocksListenAddress` and `SocksPort` are the host and port your Tor client listens on. Data sent here will be route to the Tor network using one of the reachable addresses and then to the desired destination. 

After that, start Tor client by running the script in the installation folder. Then set your application's proxy to point to 127.0.0.1:9150

I think, however, Tor is a project with great cause. So consider contributing to the project by adding your Tor relay server to the network too: [https://cloud.torproject.org](https://cloud.torproject.org)
