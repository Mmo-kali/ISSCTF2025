#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/socket.h>

#define PORT 666
#define BUFFER_SIZE 444

void authenticate(int clientSck) {	
    char username[BUFFER_SIZE];
    char password[BUFFER_SIZE];

    send(clientSck, "Enter your alias: ", 17, 0);

    recv(clientSck, username, BUFFER_SIZE * 5, 0); // Potential buffer overflow here

    if (strcmp(username, "Pixy\n") != 0) {
        send(clientSck, "I don't know anybody with that name!\n", 36, 0);
        goto noUser;
    }

    send(clientSck, "Enter your password: ", 22, 0);
    recv(clientSck, password, BUFFER_SIZE, 0);

    if (strcmp(password, "V2isTheSolution\n") == 0) {
        send(clientSck, "Congratulations! you achieved absolutely nothing XD\n", 51, 0);
    } else {
        send(clientSck, "Access denied! :P\n", 17, 0);
    }

    noUser:
    __asm("mov \%ebp,\%eax\n\t");
}

int main() {
    int serverSck, clientSck;
    struct sockaddr_in server_addr, client_addr;
    socklen_t addr_size;

    signal(SIGCHLD, SIG_IGN); // OS reaping zombies

    serverSck = socket(AF_INET, SOCK_STREAM, 0);
    if (serverSck < 0) {
        perror("Socket creation failed");
        exit(1);
    }

    int reuse = 1;
    if (setsockopt(serverSck, SOL_SOCKET, SO_REUSEADDR, &reuse, sizeof(reuse)) < 0) {
        perror("Setsockopt failed");
        close(serverSck);
        exit(1);
    }

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(PORT);

    if (bind(serverSck, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
        perror("Bind failed");
        close(serverSck);
        exit(1);
    }

    if (listen(serverSck, 60) < 0) {
        perror("Listen failed");
        close(serverSck);
        exit(1);
    }

    printf("Server listening on port %d...\n", PORT);

    while (1) {
        addr_size = sizeof(client_addr);
        clientSck = accept(serverSck, (struct sockaddr *)&client_addr, &addr_size);
        if (clientSck < 0) {
            perror("Accept failed");
            continue;
        }
	
        pid_t pid = fork();
        
	if (pid < 0) {
            perror("Fork failed");
            close(clientSck);
        } else if (pid == 0) {
            close(serverSck);
	    printf("Connection established with %s:%d\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
            char banner[] = "\n ____  _            _    _    _       _     ____\
		     \n|  _ \\| |          | |  | |  | |     | |   |  _ \\\
		     \n| |_) | | __ _  ___| | _| |__| | __ _| |_  | |_) |_   _ _ __ ___  __ _ _   _ \
		     \n|  _ <| |/ _` |/ __| |/ /  __  |/ _` | __| |  _ <| | | | '__/ _ \\/ _` | | | |\
		     \n| |_) | | (_| | (__|   <| |  | | (_| | |_  | |_) | |_| | | |  __/ (_| | |_| |\
		     \n|____/|_|\\__,_|\\___|_|\\_\\_|  |_|\\__,_|\\__| |____/ \\__,_|_|  \\___|\\__,_|\\__,_|\n";

            send(clientSck, banner, strlen(banner), 0);
	    authenticate(clientSck);
	    close(clientSck);
            exit(0); 
        } else {
            close(clientSck); 
        }
    }

    close(serverSck);
    return 0;
}


void asmFun(){
	__asm__ ("call *%eax\n\n"); 
}

