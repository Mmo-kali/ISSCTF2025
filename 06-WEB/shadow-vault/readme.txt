The goal of this challenge is for the contestants to be able to login to the crypto wallet account of the user name shadowMan. This shadowMan in his crypto wallet (located at the directory '/cypt-wallet') which is accessible when he is logged into the made up crypto trading platform will contain the flag. 


The users will be given the user name and password of shadowMan but inorder to login to the account they need to know his secret 2fa code which user will not have access to and will not be able to brute force. 

the way the web app works is it doesn't track when a user logged in or out it just creates a static cookie using HTTP basic authetication. 



**** chatGPT explination of HTTP basic AUTH for anyone who doesn't know... ****

HTTP Basic Authentication is a simple authentication scheme built into the HTTP protocol. The client sends a request with an `Authorization` header that contains the word `Basic` followed by a space and a base64-encoded string `username:password`. 

For example, if the username is `shadowMan` and the password is `password`, the client would send:

```
Authorization:

 Basic

 c2hhZG93TWFuOnBhc3N3b3Jk
```

The server decodes the base64 string and splits it into a username and password. If the username and password match the records on the server, the server considers the client authenticated. 

This method is not very secure because the credentials are sent in plain text (just base64 encoded, which is easily decoded). It's recommended to use HTTPS to encrypt the entire HTTP traffic when Basic Authentication is used.
____________________________________________________________________________________________________________________________________________________________________________________________________________________________________

therfore since the users aren't able to generate the HTTP authenticated token because they dont know the 2fa code the only other soulition they have is to create the auth token and because they already have his username and password all they need to do it use burpsuite encoder then pass the encoded string into repeater or to the proxy and with the inserted cookie request /cypt-wallet then they can get the user flag and solve the challenge 