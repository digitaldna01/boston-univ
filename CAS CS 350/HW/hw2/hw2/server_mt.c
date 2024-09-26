/*******************************************************************************
* Simple FIFO Order Server Implementation
*
* Description:
*     A server implementation designed to process client requests in First In,
*     First Out (FIFO) order. The server binds to the specified port number
*     provided as a parameter upon launch.
*
* Usage:
*     <build directory>/server <port_number>
*
* Parameters:
*     port_number - The port number to bind the server to.
*
* Author:
*     Renato Mancuso
*
* Affiliation:
*     Boston University
*
* Creation Date:
*     September 10, 2023
*
* Last Changes:
*     September 16, 2024
*
* Notes:
*     Ensure to have proper permissions and available port before running the
*     server. The server relies on a FIFO mechanism to handle requests, thus
*     guaranteeing the order of processing. For debugging or more details, refer
*     to the accompanying documentation and logs.
*
*******************************************************************************/

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <sched.h>
#include <signal.h>

/* Phtread header file */ 
#include <pthread.h>

/* Needed for wait(...) */
#include <sys/types.h>
#include <sys/wait.h>

/* for termination flag */
#include <stdbool.h> 

/* Include struct definitions and other libraries that need to be
 * included by both client and server */
#include "common.h"

#define BACKLOG_COUNT 100
#define USAGE_STRING				\
	"Missing parameter. Exiting.\n"		\
	"Usage: %s <port_number>\n"

/* 4KB of stack for the worker thread */
#define STACK_SIZE (4096)

/* Declare a global termination flag */
volatile bool terminate_thread = false;

/* Main logic of the worker thread */
/* IMPLEMENT HERE THE MAIN FUNCTION OF THE WORKER */
void* worker_main(void* arg){
	(void)arg;
	// Define the variable
	struct timespec timestamp;

	// stamp at which the worker entered the worker fucntion

	// Output the string "[#WORKER#] <timestamp> Worker Thread Alive!"
	clock_gettime(CLOCK_MONOTONIC, &timestamp);
	printf("[#WORKER#] %f Worker Thread Alive!\n", TSPEC_TO_DOUBLE(timestamp));

	// enter a forever loop and follow iteration
	while(!terminate_thread){
		// (1) busywait for exactly 1 second
		get_elapsed_busywait(1, 0);

		// (2) print out "[#WORKER#] <timestamp> Still Alive!"
		clock_gettime(CLOCK_MONOTONIC, &timestamp);
		printf("[#WORKER#] %f Worker Still Alive!\n", TSPEC_TO_DOUBLE(timestamp));

		// (3) sleep for exactly 1 second, rinse and repeat
		get_elapsed_sleep(1, 0);
	}
	return NULL;
}

/* Main function to handle connection with the client. This function
 * takes in input conn_socket and returns only when the connection
 * with the client is interrupted. */
void handle_connection(int conn_socket) {	
	// define the variables
	// child process variable
	pthread_t thread;

	// parent process variable
	int recv_message, send_message;
	struct request req;
	struct response res;
	struct timespec receipt_timestamp, completion_timestamp;

	/* The connection with the client is alive here. Let's start
	 * the worker thread. */
	
	/* IMPLEMENT HERE THE LOGIC TO START THE WORKER THREAD. */
	if(pthread_create(&thread, NULL, worker_main, NULL) != 0){
		ERROR_INFO();
		perror("Error creating thread\n");
		return;
	}
	
	/* We are ready to proceed with the rest of the request
	 * handling logic. */

	/* REUSE LOGIC FROM HW1 TO HANDLE THE PACKETS */
	while(1){
		recv_message = recv(conn_socket, &req, sizeof(struct request), 0);

		// stamp at which the server received the request
		clock_gettime(CLOCK_MONOTONIC, &receipt_timestamp);

		if(recv_message < 0) {
			ERROR_INFO();
			perror("Unable to read request");
			break;
		}

		// Check if clients closed the socket
		if(recv_message == 0){
			// The requested number of bytes to receive from a stream socket is 0
			break;
		}

		//busy wait requested length
		get_elapsed_busywait(req.req_length.tv_sec, req.req_length.tv_nsec);

		res.req_id = req.req_id;
		res.reserved = 0;
		res.ack = 0;

		send_message = send(conn_socket, &res, sizeof(struct response), 0);
		if(send_message < 0){
			ERROR_INFO();
			perror("Unable to send response");
			close(conn_socket);
			break;
		}

		// stamp at which the server complete the request
		clock_gettime(CLOCK_MONOTONIC, &completion_timestamp);

		printf("R%lu:%f,%f,%f,%f\n", req.req_id, TSPEC_TO_DOUBLE(req.req_timestamp), TSPEC_TO_DOUBLE(req.req_length), TSPEC_TO_DOUBLE(receipt_timestamp), TSPEC_TO_DOUBLE(completion_timestamp));
	} 

	// Signal the worker thread to terminate
    terminate_thread = true;

	if (pthread_join(thread, NULL) !=0){
		ERROR_INFO();
		perror("Error joining thread\n");
	}
}


/* Template implementation of the main function for the FIFO
 * server. The server must accept in input a command line parameter
 * with the <port number> to bind the server to. */
int main (int argc, char ** argv) {
	int sockfd, retval, accepted, optval;
	in_port_t socket_port;
	struct sockaddr_in addr, client;
	struct in_addr any_address;
	socklen_t client_len;

	/* Get port to bind our socket to */
	if (argc > 1) {
		socket_port = strtol(argv[1], NULL, 10);
		printf("INFO: setting server port as: %d\n", socket_port);
	} else {
		ERROR_INFO();
		fprintf(stderr, USAGE_STRING, argv[0]);
		return EXIT_FAILURE;
	}

	/* Now onward to create the right type of socket */
	sockfd = socket(AF_INET, SOCK_STREAM, 0);

	if (sockfd < 0) {
		ERROR_INFO();
		perror("Unable to create socket");
		return EXIT_FAILURE;
	}

	/* Before moving forward, set socket to reuse address */
	optval = 1;
	setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (void *)&optval, sizeof(optval));

	/* Convert INADDR_ANY into network byte order */
	any_address.s_addr = htonl(INADDR_ANY);

	/* Time to bind the socket to the right port  */
	addr.sin_family = AF_INET;
	addr.sin_port = htons(socket_port);
	addr.sin_addr = any_address;

	/* Attempt to bind the socket with the given parameters */
	retval = bind(sockfd, (struct sockaddr *)&addr, sizeof(struct sockaddr_in));

	if (retval < 0) {
		ERROR_INFO();
		perror("Unable to bind socket");
		return EXIT_FAILURE;
	}

	/* Let us now proceed to set the server to listen on the selected port */
	retval = listen(sockfd, BACKLOG_COUNT);

	if (retval < 0) {
		ERROR_INFO();
		perror("Unable to listen on socket");
		return EXIT_FAILURE;
	}

	/* Ready to accept connections! */
	printf("INFO: Waiting for incoming connection...\n");
	client_len = sizeof(struct sockaddr_in);
	accepted = accept(sockfd, (struct sockaddr *)&client, &client_len);

	if (accepted == -1) {
		ERROR_INFO();
		perror("Unable to accept connections");
		return EXIT_FAILURE;
	}

	/* Ready to handle the new connection with the client. */
	handle_connection(accepted);

	close(sockfd);
	return EXIT_SUCCESS;
}
