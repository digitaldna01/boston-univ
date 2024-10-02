/*******************************************************************************
* Dual-Threaded FIFO Server Implementation w/ Queue Limit
*
* Description:
*     A server implementation designed to process client requests in First In,
*     First Out (FIFO) order. The server binds to the specified port number
*     provided as a parameter upon launch. It launches a secondary thread to
*     process incoming requests and allows to specify a maximum queue size.
*
* Usage:
*     <build directory>/server -q <queue_size> <port_number>
*
* Parameters:
*     port_number - The port number to bind the server to.
*     queue_size  - The maximum number of queued requests
*
* Author:
*     Renato Mancuso
*
* Affiliation:
*     Boston University
*
* Creation Date:
*     September 29, 2023
*
* Last Update:
*     September 25, 2024
*
* Notes:
*     Ensure to have proper permissions and available port before running the
*     server. The server relies on a FIFO mechanism to handle requests, thus
*     guaranteeing the order of processing. If the queue is full at the time a
*     new request is received, the request is rejected with a negative ack.
*
*******************************************************************************/

#define _GNU_SOURCE
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <sched.h>
#include <signal.h>
#include <unistd.h>

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
	"Usage: %s -q <queue size> <port_number>\n"


/* START - Variables needed to protect the shared queue. DO NOT TOUCH */
sem_t * queue_mutex;
sem_t * queue_notify;
/* END - Variables needed to protect the shared queue. DO NOT TOUCH */

/* Declare a global termination flag */
volatile bool terminate_thread = false;

struct queue {
    /* IMPLEMENT ME */
	struct request_meta *buffer;
	int front;
	int rear;
	int count;
	int size;
};

struct worker_params {
    /* IMPLEMENT ME */
	struct queue *the_queue;
	int conn_socket;
};

/* Queue Helper function */
struct queue* queue_init(size_t queue_size) {
    struct queue *the_queue = (struct queue *)malloc(sizeof(struct queue));
    if (the_queue == NULL) {
        perror("Failed to allocate memory for the_queue");
        ERROR_INFO();
    }

    the_queue->buffer = (struct request_meta *)malloc(queue_size * sizeof(struct request_meta));
    if (the_queue->buffer == NULL) {
        perror("Failed to allocate memory for the_queue->buffer");
        ERROR_INFO();
    }

    the_queue->front = 0;
    the_queue->rear = 0;
    the_queue->count = 0;
    the_queue->size = queue_size;

    return the_queue;
}

/* Function to free the allocated memory */
void queue_free(struct queue *the_queue) {
    if (the_queue) {
        free(the_queue->buffer);
        free(the_queue);
    }
}

/* Add a new request <request> to the shared queue <the_queue> */
int add_to_queue(struct request_meta to_add, struct queue * the_queue)
{
	int retval = 0;
	/* QUEUE PROTECTION INTRO START --- DO NOT TOUCH */
	sem_wait(queue_mutex);
	/* QUEUE PROTECTION INTRO END --- DO NOT TOUCH */

	/* WRITE YOUR CODE HERE! */
	/* MAKE SURE NOT TO RETURN WITHOUT GOING THROUGH THE OUTRO CODE! */

	/* Make sure that the queue is not full */
	if (the_queue->count == the_queue->size) {
		/* What to do in case of a full queue */
		/* DO NOT RETURN DIRECTLY HERE */
		retval = -1;
	} else {
		/* If all good, add the item in the queue */
		/* IMPLEMENT ME !!*/
		the_queue->buffer[the_queue->rear] = to_add;
		the_queue->rear = (the_queue->rear + 1) % the_queue->size;
		the_queue->count++;

		/* QUEUE SIGNALING FOR CONSUMER --- DO NOT TOUCH */
		sem_post(queue_notify);
	}

	/* QUEUE PROTECTION OUTRO START --- DO NOT TOUCH */
	sem_post(queue_mutex);
	/* QUEUE PROTECTION OUTRO END --- DO NOT TOUCH */
	return retval;
}

/* Add a new request <request> to the shared queue <the_queue> */
struct request_meta get_from_queue(struct queue * the_queue)
{
	struct request_meta retval;
	/* QUEUE PROTECTION INTRO START --- DO NOT TOUCH */
	sem_wait(queue_notify);
	sem_wait(queue_mutex);
	/* QUEUE PROTECTION INTRO END --- DO NOT TOUCH */

	/* WRITE YOUR CODE HERE! */
	/* MAKE SURE NOT TO RETURN WITHOUT GOING THROUGH THE OUTRO CODE! */
	retval = the_queue->buffer[the_queue->front];
	the_queue->front = (the_queue->front + 1) % the_queue->size;
	the_queue->count--;
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
		index = (the_queue->front + i) % the_queue->size;
		printf("R%ld", the_queue->buffer[index].req.req_id);

		if(i < the_queue->count - 1){
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
	struct worker_params* worker_parameter = (struct worker_params *)worker_param;
	int send_message;
	struct request_meta work_req;
	struct response res;
	struct timespec timestamp,  start_timestamp, completion_timestamp;

	printf("INFO: Worker thread started. Thread ID = %lu\n", pthread_self());

	// Output the string "[#WORKER#] <timestamp> Worker Thread Alive!"
	clock_gettime(CLOCK_MONOTONIC, &timestamp);
	printf("[#WORKER#] %f Worker Thread Alive!\n", TSPEC_TO_DOUBLE(timestamp));

	// take queue input
	// struct worker_params* worker_parameter = (struct worker_params*)worker_param;
	struct queue* the_queue = worker_parameter->the_queue;
	int connection = worker_parameter->conn_socket;

	while(!terminate_thread){
		
		// Retrive a request from the queue
		if (the_queue->count > 0){
			work_req = get_from_queue(the_queue);
			// get the start timestamp
			clock_gettime(CLOCK_MONOTONIC, &start_timestamp);

			// Process the request if valid 
			//busy wait requested length
			get_elapsed_busywait(work_req.req.req_length.tv_sec, work_req.req.req_length.tv_nsec);

			res.req_id = work_req.req.req_id;
			res.reserved = 0;
			res.ack = RESP_COMPLETED;

			send_message = send(connection, &res, sizeof(struct response), 0);
			if(send_message <= 0){
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
void handle_connection(int conn_socket, int q_size)
{
	struct request * req;
	struct request_meta *req_meta;
	struct queue * the_queue;
	size_t in_bytes;
	struct timespec receipt_timestamp, reject_timestamp;
	pthread_t thread;
	struct response res;
	int send_message;

	/* The connection with the client is alive here. Let's
	 * initialize the shared queue. */
	
	/* IMPLEMENT HERE ANY QUEUE INITIALIZATION LOGIC */
	the_queue = queue_init(q_size);

	if(the_queue == NULL){
		ERROR_INFO();
		perror("Error creating queue\n");
		return;
	}
	
	/* Queue ready to go here. Let's start the worker thread. */

	/* IMPLEMENT HERE THE LOGIC TO START THE WORKER THREAD. */
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
			if (add_to_queue(*req_meta, the_queue) == -1){
				/* HANDLE REJECTION IF NEEDED */
				// Queue is full, handle rejection
				// Reject timestamp
				clock_gettime(CLOCK_MONOTONIC, &reject_timestamp);
				
				res.req_id = req_meta->req.req_id;
				res.reserved = 0;
				res.ack = RESP_REJECTED;

				send_message = send(conn_socket, &res, sizeof(struct response), 0);
				if(send_message < 0){
					ERROR_INFO();
					perror("Unable to send response");
					break;
				}

				printf("X%lu:%f,%f,%f\n", 
					res.req_id, 
					TSPEC_TO_DOUBLE(req_meta->req.req_timestamp), 
					TSPEC_TO_DOUBLE(req_meta->req.req_length), 
					TSPEC_TO_DOUBLE(reject_timestamp)
				);
				dump_queue_status(the_queue);
			}
			
		}else {
			// if in_bytes is closed or error receiving data, stop queuing
			break;
		}
	} while (in_bytes > 0);

	/* PERFORM ORDERLY DEALLOCATION AND OUTRO HERE */
	
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
	/* FREE UP DATA STRUCTURES AND SHUTDOWN CONNECTION WITH CLIENT */
	free(req);
	free(req_meta);
	queue_free(the_queue);
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

	/* Parse all the command line arguments */
	/* IMPLEMENT ME!! */
	/* PARSE THE COMMANDS LINE: */
	/* 1. Detect the -q parameter and set aside the queue size  */
	int opt;
    int size = 0;
    char *port_number;  // Change to char*

	while ((opt = getopt(argc, argv, "q:")) != -1) {
        switch (opt) {
            case 'q':
                size = atoi(optarg);  // Get the <size> value
                break;
            case '?':
                fprintf(stderr, "Usage: %s -q <size> <port_number>\n", argv[0]);
                exit(EXIT_FAILURE);
        }
    }
	// Ensure <port_number> is provided
    if (optind >= argc) {
        fprintf(stderr, "Expected <port_number> after options\n");
        exit(EXIT_FAILURE);
    }
	printf("INFO: setting queue size as: %d\n", size);

	/* 2. Detect the port number to bind the server socket to (see HW1 and HW2) */
	// Convert the remaining argument to port_number
    port_number = argv[optind];

	/* Get port to bind our socket to */
	socket_port = strtol(port_number, NULL, 10);
	printf("INFO: setting server port as: %d\n", socket_port);

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
	handle_connection(accepted, size);

	free(queue_mutex);
	free(queue_notify);

	close(sockfd);
	return EXIT_SUCCESS;

}
