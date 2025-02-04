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
*     September 10, 2024
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

/* Needed for wait(...) */
#include <sys/types.h>
#include <sys/wait.h>

/* Needed for semaphores */
#include <semaphore.h>

/* Phtread header file */ 
#include <pthread.h>

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

/* START - Variables needed to protect the shared queue. DO NOT TOUCH */
sem_t * queue_mutex;
sem_t * queue_notify;
/* END - Variables needed to protect the shared queue. DO NOT TOUCH */

/* Max number of requests that can be queued */
#define QUEUE_SIZE 500

/* Declare a global termination flag */
volatile bool terminate_thread = false;

struct queue {
    /* IMPLEMENT ME */
	struct request_meta buffer[QUEUE_SIZE];
	int front;
	int rear;
	int count;
};

struct worker_params {
    /* IMPLEMENT ME */
	struct queue *the_queue;
	int conn_socket;
};

/* Add a new request <request> to the shared queue <the_queue> */
int add_to_queue(struct request_meta to_add, struct queue *the_queue)
{
	int retval = 0;

	/* QUEUE PROTECTION INTRO START --- DO NOT TOUCH */
	sem_wait(queue_mutex);
	/* QUEUE PROTECTION INTRO END --- DO NOT TOUCH */

	/* WRITE YOUR CODE HERE! */
	/* MAKE SURE NOT TO RETURN WITHOUT GOING THROUGH THE OUTRO CODE! */
	if (the_queue->count == QUEUE_SIZE){
		retval = -1;
	} else{
		// add queue
		the_queue->buffer[the_queue->rear] = to_add;
		the_queue->rear = (the_queue->rear + 1) % QUEUE_SIZE;
		the_queue->count++;
	}
	
	/* QUEUE PROTECTION OUTRO START --- DO NOT TOUCH */
	sem_post(queue_mutex);
	sem_post(queue_notify);
	/* QUEUE PROTECTION OUTRO END --- DO NOT TOUCH */
	return retval;
}

/* Get a new request <request> to the shared queue <the_queue> */
struct request_meta get_from_queue(struct queue *the_queue)
{
	struct request_meta retval;
	/* QUEUE PROTECTION INTRO START --- DO NOT TOUCH */
	sem_wait(queue_notify);
	sem_wait(queue_mutex);
	/* QUEUE PROTECTION INTRO END --- DO NOT TOUCH */

	/* WRITE YOUR CODE HERE! */
	/* MAKE SURE NOT TO RETURN WITHOUT GOING THROUGH THE OUTRO CODE! */
	if (the_queue->count == 0){
		return retval;
	} else{
		retval = the_queue->buffer[the_queue->front];
		the_queue->front = (the_queue->front + 1) % QUEUE_SIZE;
		the_queue->count--;
	}

	/* QUEUE PROTECTION OUTRO START --- DO NOT TOUCH */
	sem_post(queue_mutex);
	/* QUEUE PROTECTION OUTRO END --- DO NOT TOUCH */
	return retval;
}

/* Implement this method to correctly dump the status of the queue
 * following the format Q:[R<request ID>,R<request ID>,...] */
void dump_queue_status(struct queue * the_queue)
{
	int i, index;

	/* QUEUE PROTECTION INTRO START --- DO NOT TOUCH */
	sem_wait(queue_mutex);
	/* QUEUE PROTECTION INTRO END --- DO NOT TOUCH */

	/* WRITE YOUR CODE HERE! */
	/* MAKE SURE NOT TO RETURN WITHOUT GOING THROUGH THE OUTRO CODE! */
	printf("Q:[");
	for (i = 0; i < the_queue->count; i++){
		index = (the_queue->front + i) % QUEUE_SIZE; 
		printf("R%ld", the_queue->buffer[index].req.req_id);

		if(i < the_queue->count - 1) {
			printf(",");
		}
	}
	printf("]\n");
	/* QUEUE PROTECTION OUTRO START --- DO NOT TOUCH */
	sem_post(queue_mutex);
	/* QUEUE PROTECTION OUTRO END --- DO NOT TOUCH */
}


/* Main logic of the worker thread */
/* IMPLEMENT HERE THE MAIN FUNCTION OF THE WORKER */
void *worker_main(void *worker_param){
	// Define the variable
	struct worker_params* worker_parameter = (struct worker_params *)worker_param;
	int send_message;
	struct request_meta work_req;
	struct response res;
	struct timespec start_timestamp, completion_timestamp;
	
	// take queue input
	// struct worker_params* worker_parameter = (struct worker_params*)worker_param;
    struct queue* the_queue = worker_parameter->the_queue; // Adjusted to point correctly
    int connection = worker_parameter->conn_socket;
	
	while(!terminate_thread){
		// Retrive a request from the queue
		if (the_queue->count == 0){
			break;
		} else{
			work_req = get_from_queue(the_queue);
			// get the start timestamp
			clock_gettime(CLOCK_MONOTONIC, &start_timestamp);
		
			// Process the request if valid 
			//busy wait requested length
			get_elapsed_busywait(work_req.req.req_length.tv_sec, work_req.req.req_length.tv_nsec);

			res.req_id = work_req.req.req_id;
			res.reserved = 0;
			res.ack = 0;

		send_message = send(connection, &res, sizeof(struct response), 0);
		if(send_message < 0){
			ERROR_INFO();
			perror("Unable to send response");
			break;
		}
			
		// get the completion timestamp
		clock_gettime(CLOCK_MONOTONIC, &completion_timestamp);

		printf("R%lu:%f,%f,%f,%f,%f\n", 
				work_req.req.req_id, 
				TSPEC_TO_DOUBLE(work_req.req.req_timestamp), 
				TSPEC_TO_DOUBLE(work_req.req.req_length), 
				TSPEC_TO_DOUBLE(work_req.receipt_timestamp), 
				TSPEC_TO_DOUBLE(start_timestamp), 
				TSPEC_TO_DOUBLE(completion_timestamp)
		);

		dump_queue_status(the_queue);
		}
	}
	return NULL;
}

/* Main function to handle connection with the client. This function
 * takes in input conn_socket and returns only when the connection
 * with the client is interrupted. */
void handle_connection(int conn_socket)
{

	struct request *req;
	struct request_meta *req_meta;
	size_t in_bytes;
	struct timespec receipt_timestamp;
	pthread_t thread;


	/* The connection with the client is alive here. Let's
	 * initialize the shared queue. */

	/* IMPLEMENT HERE ANY QUEUE INITIALIZATION LOGIC */
	struct queue *the_queue = (struct queue*)malloc(sizeof (struct queue));
	if (the_queue == NULL){
		ERROR_INFO();
		perror("Error creating queue\n");
		return;
	}

	//initial the queue
	the_queue->front = 0;
	the_queue->rear = 0;
	the_queue->count = 0;

	/* Queue ready to go here. Let's start the worker thread. */
	
	/* IMPLEMENT HERE THE LOGIC TO START THE WORKER THREAD. */
	// Wrap queue with worker paramter to pass to worker thread
	struct worker_params *params = (struct worker_params*)malloc(sizeof (struct worker_params));
	if (params == NULL){
		perror("Failed to allocate memory for worker_params");
        free(the_queue);
        return;
	}

	// set the work parameter variable
	params->the_queue = the_queue;
	params->conn_socket = conn_socket;

	if (pthread_create(&thread, NULL, worker_main, (void*)params) < 0){
		ERROR_INFO();
		perror("Error creating thread\n");
		return;
	}
	/* We are ready to proceed with the rest of the request
	 * handling logic. */

	/* REUSE LOGIC FROM HW1 TO HANDLE THE PACKETS */

	// Create req and req_meta
	req = (struct request *)malloc(sizeof(struct request));
	req_meta = (struct request_meta *)malloc(sizeof(struct request_meta));

	do {
		in_bytes = recv(conn_socket, req, sizeof(struct request), 0);
		/* SAMPLE receipt_timestamp HERE */
		clock_gettime(CLOCK_MONOTONIC, &receipt_timestamp);

		req_meta->req = *req;
		req_meta->receipt_timestamp = receipt_timestamp;

		/* Don't just return if in_bytes is 0 or -1. Instead
		 * skip the response and break out of the loop in an
		 * orderly fashion so that we can de-allocate the req
		 * and resp varaibles, and shutdown the socket. */
		if (in_bytes > 0) {
			add_to_queue(*req_meta, the_queue);
		}else {
			// if in_bytes is closed or error receiving data, stop queuing
			break;
		}
	} while (in_bytes > 0);

	/* Ask the worker thead to terminate */
	/* ASSERT TERMINATION FLAG FOR THE WORKER THREAD */
    terminate_thread = true;
	/* Make sure to wake-up any thread left stuck waiting for items in the queue. DO NOT TOUCH */
	sem_post(queue_notify);

	/* Wait for orderly termination of the worker thread */	
	/* ADD HERE LOGIC TO WAIT FOR TERMINATION OF WORKER */
	if (pthread_join(thread, NULL) != 0){
		ERROR_INFO();
		perror("Error joining thread\n");
	}

	/* PERFORM ORDERLY DEALLOCATION AND OUTRO HERE */
	free(req);
	free(req_meta);
	free(the_queue);
	free(params);
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

	/* Initialize queue protection variables. DO NOT TOUCH. */
	queue_mutex = (sem_t *)malloc(sizeof(sem_t));
	queue_notify = (sem_t *)malloc(sizeof(sem_t));
	retval = sem_init(queue_mutex, 0, 1);
	if (retval < 0) {
		ERROR_INFO();
		perror("Unable to initialize queue mutex");
		return EXIT_FAILURE;
	}
	retval = sem_init(queue_notify, 0, 0);
	if (retval < 0) {
		ERROR_INFO();
		perror("Unable to initialize queue notify");
		return EXIT_FAILURE;
	}
	/* DONE - Initialize queue protection variables. DO NOT TOUCH */

	/* Ready to handle the new connection with the client. */
	handle_connection(accepted);

	free(queue_mutex);
	free(queue_notify);

	close(sockfd);
	return EXIT_SUCCESS;

}
