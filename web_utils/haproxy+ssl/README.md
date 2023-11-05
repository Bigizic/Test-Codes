## This direcotry contains files concerning loadbalancer and haproxy and ssl certificates

### To generate a ssl certificate, install certbot after that run this to generate a 2048 bits certificate

    sudo certbot certonly --rsa-key-size 2048 -d {domain_name} in my case - www.isaacajibola.tech

### To generate the normal 1024 bits certificate

    sudo certbot certonly --standalone -d {domain_name} in my case - www.isaacajibola.tech

### Note in your dns configuration on your domain, make sure the subdomain www resolves to the ip of the machine you're using as
### the load balancer and you're using to host them certificates, this would move all www.isaacajibola.tech domain names to the
### ip of the machine that has a secured ssl certificarte, if you want to use isaacajibola.tech alone without a sub-domain like 
    ``www`` or ``io``
### or whatever you can edit the subdomain in the dns configuration in the domain service

Now this enbales all traffic from ``io.isaacajibola.tech`` or ``www.isaacajibola.tech`` or ``isaacajibola.tech`` to that local machine

Now to make sure haproxy works well you'll need to disable Nginx or i'm not sure if you disable Nginx from using port 80 maybe Nginx stops
Haproxy from using port 80 but i notice if haproxy and Nginx are enabled Nginx would work but haproxy would have conflicts unless you stop
Nginx or disable it. It seems like both service are configured to listen to port 80 so HAPROXY should listen to port 8080 for better service
and Nginx can run while Haproxy runs.

In the Haproxy config file have it like this

    frontend www-http
          bind *:8080
          http-request add-header X-Forwarded-Proto http
          default_backend web-backend
          redirect scheme https code 301 if !{ ssl_fc }

This above would forward all http request to port 8080 allowing Nginx to use port 80 for http request and HAproxy to use port 8080 for http request.

Not the http request is been sent to the default backend which is     ``web-backend``


### Haproxy https configuration

    frontend www-https
            bind *:443 ssl crt /etc/letsencrypt/live/www.isaacajibola.tech/fullchain.pem
            http-request add-header X-Forwarded-Proto https
            acl     letsencrypt-acl path_beg /.well-known/acme-challenge/
            use_backend letsencrypt-backend if letsencrypt-acl
            default_backend web-backend

in this above script it'd forward all https requests to the default_backend but to make the https reauest more secure and it's a most for all https website to
have an ssl certificate to function well... So in the above script the path to the ssl certificate is passed alongside the bind *:443 which means bind all hosts on
that machine on port 443, normally it'd be bind localhost for more clarity but it's ok like this

The acl   letsencrypt path_beg    This means if a well-known/acme-challenge/    is passed like this www.isaacajibola.tech/.well-known/acme-challenge/ it'll resolve to
the backend_server for it... This is the point of ACME

## Begin point of ACME
The .well-known/acme-challenge directory and its associated files are part of the Automatic Certificate Management Environment (ACME) protocol,
which is used by certificate authorities like Let's Encrypt to automate the process of obtaining and renewing SSL/TLS certificates.
This directory serves a specific purpose:

* Domain Ownership Verification: During the process of issuing or renewing an SSL/TLS certificate,
  the certificate authority (CA) needs to verify that the entity requesting the certificate has control over the domain for which the certificate
  is being requested. This verification is a crucial security measure to prevent unauthorized certificate issuance.

* Challenge-Response Mechanism: To perform domain ownership verification, the CA challenges the requesting party to prove that they control the domain.
  This challenge is usually presented as a random file that needs to be hosted on the web server under the .well-known/acme-challenge directory within the
  domain's document root.

* Unique and Temporary Files: The challenge files under .well-known/acme-challenge are unique and temporary.
  They are generated for each certificate issuance or renewal request and contain information that demonstrates control over the domain.
  They are not meant to be used for any other purpose and have short lifespans.

* Non-Intrusive Verification: The .well-known/acme-challenge directory and its files do not affect your website's normal operation.
  They are used exclusively for domain verification and are not meant for public consumption. They don't impact the functionality or appearance of your website.

* By serving the challenge files from the .well-known/acme-challenge directory, you demonstrate to the CA that you have the necessary control
  and access to the web server for the domain in question. Once the CA successfully accesses and verifies the challenge file, it can proceed with issuing or
  renewing the SSL/TLS certificate for your domain. This process ensures the security and authenticity of the certificate issuance.

  ## BACKEND CONFIG

      backend web-backend
            balance roundrobin
            redirect scheme https if !{ ssl_fc }
            server 297651-web-01 100.26.155.102:80 check
            server 297651-web-02 100.24.235.105:80 check backup

      backend letsencrypt-backend
            server letsencrypt 0.0.0.0:80

This backend configuration use round robin algorithm to distribute requests to the two servers, below is the meaning of roundrobin algorithm:

Round-robin is a simple and widely used load-balancing algorithm that distributes incoming requests or connections equally in a cyclic manner
among a group of servers. The term "round-robin" implies that each server in the group takes its turn in serving a request, with no consideration
of server load or other factors. Here's how round-robin load balancing works:

* Request Distribution: When a new request or connection comes in, the load balancer routes it to the next server in the list.
  The load balancer keeps track of the order of servers, and it cycles through the list for each new request, starting from the first server
  and looping back to the beginning when it reaches the end of the list.

* Equal Distribution: Round-robin ensures that each server in the group receives an approximately equal share of requests over time.
  It's a "fair" distribution method because all servers get an equal opportunity to process incoming traffic.

* Simplicity: Round-robin is simple to implement and doesn't require complex algorithms or real-time monitoring of server health and
* performance. This makes it an easy and cost-effective solution for load balancing.


Other algorithm includes:

* Leastconn:
  balance leastconn distributes requests to the server with the least number of active connections.
  his helps to distribute traffic more evenly, and when a server becomes overloaded or unresponsive, HAProxy will naturally send fewer requests to that server.

* Source IP Hashing (source):
  balance source uses a hash of the source IP address to determine which server to send traffic to.
  This ensures that requests from the same client are consistently directed to the same server.
  If one server becomes unreachable, requests from clients that were previously routed to that server will be distributed to the other available servers.

The load-balancing algorithm that ensures the first server is used as the primary choice and the second server is used only
if the first server is unavailable is called "failover" or "backup" configuration. In HAProxy, you can achieve this behavior by using
the backup keyword in your backend server configuration.


Here's an example of how to set up a failover configuration in HAProxy:

      backend your-backend
            server server1 192.168.1.100:80 check
            server server2 192.168.1.101:80 check backup


* In this configuration:
  server1 is the primary server, and server2 is the backup server.
  The check option ensures that HAProxy continuously monitors the health of both servers.
  If server1 becomes unavailable, HAProxy will automatically fail over to server2 to handle incoming traffic.
  When server1 is back online and healthy, HAProxy will automatically switch back to using it as the primary server.



# SSL CERTIFICATE

In this guide i'd explain how the SSL work with the HAProxy configuration file

In your ssl certificate, after creating a new certificate, and remember before you can create a certificate, your domain name must resolve to the right ip address

You'd get a message like this after creation that the fullchain.pem file is in the live folder and a directory called your domain name has been created there:

      /etc/letsencrypt/live/www.isaacajibola.tech/fullchain.pem

Now if you try to access this path without specifying the full path it wouldn't let you so you need to enter full path to access it,

If you try  ``sudo ls -l /etc/letsencrypt/live/www.isaacajibola.tech/fullchain.pem`` YOu'd notice that directory is only a symbolic link and the real file is in
``/etc/letsencrypt/archive/www.isaacajibola.tech/fullchain.pem``

the same applies to the  ``/etc/letsencrypt/live/www.isaacajibola.tech/privkey.pem`` file

      sudo ls -l /etc/letsencrypt/live/www.isaacajibola.tech/privkey.pem
      lrwxrwxrwx 1 root root 48 Nov  5 09:36 /etc/letsencrypt/live/www.isaacajibola.tech/privkey.pem -> ../../archive/www.isaacajibola.tech/privkey2.pem

Now to make the haproxy serve the ssl certificate go to the original privkey.pem file in the archive dir, copy the private file contents and paste it in the original
archive fullchain.pem file it'd look like this:

        -----BEGIN PRIVATE KEY-----
        blah blah blah blah blah
        blah blah blah blah
        blah blah blah
        -----END PRIVATE KEY-----
        
        -----BEGIN CERTIFICATE-----
        blah blah blah blah blah
        blah blah blah blah
        blah blah blah
        -----END CERTIFICATE-----



This will allow the haproxy to load the private and certificate from the fullchain.pem file at once. If you don't do it like that, you might encounter this error:

      sudo haproxy -c -f /etc/haproxy/haproxy.cfg
      [ALERT] 308/104013 (67055) : parsing [/etc/haproxy/haproxy.cfg:43] : 'bind *:443' : unable to load SSL private key from PEM file '/etc/letsencrypt/live/www.isaacajibola.tech/fullchain.pem'.

This mean the haproxy is unable to read the private key from the fullchain.pem file


Another alternative is to copy the contents of the certifcate and the private key and paste it in a file somewhere secured then have haproxy link to that path


Haproxy should be fine after this configurations
