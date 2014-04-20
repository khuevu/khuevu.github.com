Title: Bypass port block by firewall with Tor
Tags: firewall, tunnel

Your network adminstrator often configure the firewall to only allow certain port for outgoing TCP connection like 80 (HTTP), 443 (HTTPS), 22 (SSH)

It is a problem if you are using other protocol to communicate to outside world, for example, IRC, git. 

One solution is to find an alternative endpoint (use https for git, webchat programs for irc), but they are not always available. 

The second solution is to have a generic program to wrap your packages in another TCP connection using an allowed port; and have a server of yours outside the firewall, listening on that port, unwrap the connection to get the original packages and send it using the desired protocol. This method is called tunneling, you can use existing program like SSH. I have written a [tunnel program](http://khuevu.github.io/2012/09/17/http-tunnel.html) using HTTP connection. 

But what if you don't have a server outside of the firewall? 

The solution I want to discuss here is using Tor client and leverage on their network of Tor bridges.

First, Download Tor [here](https://www.torproject.org/download/download-easy.html.en)

Go to the installation folder. In your `./Data/Tor/torrc` config file, update these entry: 

    #!bash
	ReachableAddresses *:80,*:443
	ReachableAddresses reject *:*
	SocksListenAddress 127.0.0.1
	SocksPort 9150

The ReachableAddresses are addresses your firewall allows you to connect. 
`SocksListenAddress` and `SocksPort` are the host and port your Tor client listens on. Data sent here will be route to the Tor network using one of the reachable addresses and then to the desired destination. 

You can add the proxy information if you uses a proxy here as well. 

The last step is to start Tor client by running the script in the installation folder. 

The point of this article is to rely on existing tor network instead of setting your own external server. I think, however, Tor is a project with great cause. So consider contributing to the project by adding your Tor relay server to the network too: [https://cloud.torproject.org](https://cloud.torproject.org)


