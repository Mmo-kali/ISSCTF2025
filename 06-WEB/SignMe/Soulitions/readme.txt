Summary of the Provided Information
User Credentials:

Username: shadowAgent (from another challenge involving whitespace)
Password: blackhats
Flag:

SolvingJWTwithTOOLS_isCool2024
Admin Login:

Username: StarLight (found as a comment in login.html)
Secret Key:

276c628ce33a59b398e4bc8f961874f454c57cfcc77cd0c27e4efc429095bd52945f465786371701f96ec5782d9379b287fe8aa6b5d00ce47f65f89fd12bc665
Brute Force List:

A common JWT list known in the web security community.
Provided file: jwtList.txt
GitHub list URL: JWT Secrets List
Instructions for the CTF Participants
Login Credentials:

Use the following credentials to log in:
Username: shadowAgent
Password: blackhats
Flag:

The flag for this challenge is: SolvingJWTwithTOOLS_isCool2024
Admin Login:

To log in as an admin, use the username StarLight. This information is hidden as a comment in the login.html file.
Secret Key:

The secret key for JWT is: 276c628ce33a59b398e4bc8f961874f454c57cfcc77cd0c27e4efc429095bd52945f465786371701f96ec5782d9379b287fe8aa6b5d00ce47f65f89fd12bc665

Brute Force List:

    - WE PROVIDED A COPY OF LIST DO NOT GIVE TO CONTESTANTS the provided jwtList.txt file to brute force JWT tokens.
    - The list is also available on GitHub: https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list

Example Usage of jwtList.txt
    - To brute force JWT tokens using the provided list, you can use tools like jwt-cracker or custom scripts. Here is an example using a Python script:

        using hashcat -->  hashcat -a 0 -m 16500 <YOUR-JWT> /path/to/jwt.secrets.list