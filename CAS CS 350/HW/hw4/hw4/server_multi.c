/*******************************************************************************
* Multi-Threaded FIFO Server Implementation w/ Queue Limit
*
* Description:
*     A server implementation designed to process client requests in First In,
*     First Out (FIFO) order. The server binds to the specified port number
*     provided as a parameter upon launch. It launches worker threads to
*     process incoming requests and allows to specify a maximum queue size.
*
* Usage:
*     <build directory>/server -q <queue_size> -w <workers> <port_number>
*
* Parameters:
*     port_number - The port number to bind the server to.
*     queue_size  - The maximum number of queued requests
*     workers     - The number of parallel threads to process requests.
*
* Author:
*     Renato Mancuso
*
* Affiliation:
*     Boston University
*
* Creation Date:
*     September 25, 2023
*
* Last Update:
*     September 30, 2024
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
#include <pthread.h>

/* Needed for wait(...) */
#include <sys/types.h>
#include <sys/wait.h>

/* Needed for semaphores */
#include <semaphore.h>

/* for termination flag */
#include <stdbool.h> 

/* Include struct definitions and other libraries that need to be
 * included by both client and server */
#include "common.h"

#define BACKLOG_COUNT 100
#define USAGE_STRING				\
	"Missing parameter. Exiting.\n"		\
	"Usage: %s -q <queue size> -w <number of threads> <port_number>\n"

/* Mutex needed to protect the threaded printf. DO NOT TOUCH */
sem_t * printf_mutex;
/* Synchronized printf for multi-threaded operation */
/* USE sync_printf(..) INSTEAD OF printf(..) FOR WORKER AND PARENT THREADS */
#define sync_printf(...)			\
	do {					\
		sem_wait(printf_mutex);		\
		printf(__VA_ARGS__);		\
		sem_post(printf_mutex);		\
	} while (0)

/* START - Variables needed to protect the shared queue. DO NOT TOUCH */
sem_t * queue_mutex;
sem_t * queue_notify;
/* END - Variables needed to protect the shared queue. DO NOT TOUCH */

struct request_meta {
	struct request request;
	struct timespec receipt_timestamp;
	/* ADD REQUIRED FIELDS */
};

struct queue {
	struct request_meta *buffer;
	int front;
	int rear;
	int count;
	int size;
};

struct connection_params {
	size_t qsize;
	size_t worker_count;
};

struct worker_params {
	/* ADD REQUIRED FIELDS */
	struct queue *the_queue;
	int conn_socket;
	volatile bool worker_done;
	int thread_id;
};

/* Helper function to perform queue initialization */
void queue_init(struct queue * the_queue, size_t queue_size)
{
	/* IMPLEMENT ME !! */
	the_queue->buffer = (struct request_meta *)malloc(queue_size * sizeof(struct request_meta));
    if (the_queue->buffer == NULL) {
        perror("Failed to allocate memory for the_queue->buffer");
        ERROR_INFO();
    }

	the_queue->front = 0;
    the_queue->rear = 0;
    the_queue->count = 0;
    the_queue->size = queue_size;
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
		retval = -1;

		/* DO NOT RETURN DIRECTLY HERE. The
		 * sem_post(queue_mutex) below MUST happen. */
	} else {
		/* If all good, add the item in the queue */
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
	if (the_queue->count == 0) {
		retval.request.req_id = UINT64_MAX;
	} else {
		retval = the_queue->buffer[the_queue->front];
		the_queue->front = (the_queue->front + 1) % the_queue->size;
		the_queue->count--;
	}

	/* QUEUE PROTECTION OUTRO START --- DO NOT TOUCH */
	sem_post(queue_mutex);
	/* QUEUE PROTECTION OUTRO END --- DO NOT TOUCH */
	return retval;
}


void dump_queue_status(struct queue * the_queue)
{
	int index;
	/* QUEUE PROTECTION INTRO START --- DO NOT TOUCH */
	sem_wait(queue_mutex);
	/* QUEUE PROTECTION INTRO END --- DO NOT TOUCH */

	/* WRITE YOUR CODE HERE! */
	/* MAKE SURE NOT TO RETURN WITHOUT GOING THROUGH THE OUTRO CODE! */
	printf("Q:[");
	for (int i = 0; i < the_queue->count; i++){
		index = (the_queue->front + i) % the_queue->size;
		printf("R%ld", the_queue->buffer[index].request.req_id);

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
void * worker_main (void * arg)
{
	struct timespec now, start_timestamp, completion_timestamp;
	struct worker_params * params = (struct worker_params *)arg;
	struct queue * the_queue;
	int conn_socket, thread_id, send_message;
	struct request_meta req;
	struct response res;

	the_queue = params->the_queue;
	conn_socket = params->conn_socket;
	thread_id = params->thread_id;

	/* Print the first alive message. */
	clock_gettime(CLOCK_MONOTONIC, &now);
	sync_printf("[#WORKER#] %lf Worker Thread Alive!\n", TSPEC_TO_DOUBLE(now));

	/* Okay, now execute the main logic. */
	while (!params->worker_done) {
		/* IMPLEMENT ME !! Main worker logic. */
		
		req = get_from_queue(the_queue);

		if(params->worker_done){
			break;
		}

		if (req.request.req_id == UINT64_MAX) {
			continue;
		}

		// get the start timestamp
		clock_gettime(CLOCK_MONOTONIC, &start_timestamp);

		// Process the request if valid
		get_elapsed_busywait(req.request.req_length.tv_sec, req.request.req_length.tv_nsec);

		res.req_id = req.request.req_id;
		res.reserved = 0;
		res.ack = RESP_COMPLETED;

		send_message = send(conn_socket, &res, sizeof(struct response), 0);
		if(send_message <= 0){
			ERROR_INFO();
			perror("Unable to send response");
			break;
		}

		// get the completion timestamp
		clock_gettime(CLOCK_MONOTONIC, &completion_timestamp);

		sync_printf("T%d R%lu:%f,%f,%f,%f,%f\n",
			thread_id,
			req.request.req_id,
			TSPEC_TO_DOUBLE(req.request.req_timestamp), 
			TSPEC_TO_DOUBLE(req.request.req_length), 
			TSPEC_TO_DOUBLE(req.receipt_timestamp), 
			TSPEC_TO_DOUBLE(start_timestamp), 
			TSPEC_TO_DOUBLE(completion_timestamp)
		);

		dump_queue_status(the_queue);

	}

	return EXIT_SUCCESS;
}

// struct worker_params * workers;

/* This function will control all the workers (start or stop them). 
 * Feel free to change the arguments of the function as you wish. */
int control_workers(int start_stop_cmd, size_t worker_count, struct worker_params * common_params)
{
	/* IMPLEMENT ME !! */
	static pthread_t * worker_threads = NULL;
	static struct worker_params * workers;

	if (start_stop_cmd == 0) { // Starting all the workers
		/* IMPLEMENT ME !! */
		worker_threads = malloc(worker_count * sizeof(pthread_t));
		workers = (struct worker_params *)malloc(worker_count * sizeof(struct worker_params));
		for (size_t i = 0; i < worker_count; i++){
			workers[i].worker_done = false;
			workers[i].thread_id = i;
			workers[i].the_queue = common_params->the_queue;
			workers[i].conn_socket = common_params->conn_socket;

			//Create Worker Thread
			if (pthread_create(&worker_threads[i], NULL, worker_main, (void*)&workers[i]) != 0){
				ERROR_INFO();
    			perror("Error creating thread\n");
    			return -1;
			} 
		}
	} else { // Stopping all the workers
		/* IMPLEMENT ME !! */
		printf("Control workers stopping started\n");
		for (size_t i = 0; i < worker_count; i++){
			workers[i].worker_done = true;
			sem_post(queue_notify);
		}

		printf("pthread_join phase\n");

		for (size_t i = 0; i < worker_count; i++){
			if (pthread_join(worker_threads[i], NULL) != 0){
				ERROR_INFO();
				perror("Error joining thread\n");
				return -1;
			}
		}
		free(worker_threads);

		printf("control workers done\n");
	}

	/* IMPLEMENT ME !! */
	return 0;
}

/* Main function to handle connection with the client. This function
 * takes in input conn_socket and returns only when the connection
 * with the client is interrupted. */
void handle_connection(int conn_socket, struct connection_params conn_params)
{
	struct request_meta * req;
	struct queue * the_queue;
	struct worker_params * params;
	size_t in_bytes, worker_count;
	struct timespec receipt_timestamp, reject_timestamp;
	struct response res;
	int send_message;


	/* IMPLEMENT ME!! Start and initialize all the
	 * worker threads ! */
	
	// initiate the queue
	the_queue = (struct queue *)malloc(sizeof(struct queue));
	queue_init(the_queue, conn_params.qsize); 

	if(the_queue == NULL){
		ERROR_INFO();
		perror("Error creating queue\n");
		return;
	}

	worker_count = conn_params.worker_count;

	params = (struct worker_params*)malloc(sizeof(struct worker_params));
	if (params == NULL){
		perror("Failed to allocate memory for worker_params");
        free(the_queue);
        return;
	}

	params->the_queue = the_queue;
	params->conn_socket = conn_socket;

	// // Initiate the params parameter
	// for (size_t i = 0; i < worker_count; i++){
	// 	params[i].the_queue = the_queue;
	// 	params[i].conn_socket = conn_socket;
	// 	params[i].worker_done = false;
	// }

	if (control_workers(0, worker_count, params) != 0){
		perror("Failed to start thread workers");
        free(the_queue);
		free(params);
        return;
	}

	/* We are ready to proceed with the rest of the request
	 * handling logic. */


	req = (struct request_meta *)malloc(sizeof(struct request_meta));

	do {
		/* IMPLEMENT ME: Receive next request from socket. */
		in_bytes = recv(conn_socket, &req->request, sizeof(struct request), 0);

		printf("Got request with size %d\n", in_bytes);

		clock_gettime(CLOCK_MONOTONIC, &receipt_timestamp);
		req->receipt_timestamp = receipt_timestamp;
		/* Don't just return if in_bytes is 0 or -1. Instead
		 * skip the response and break out of the loop in an
		 * orderly fashion so that we can de-allocate the req
		 * and resp varaibles, and shutdown the socket. */
		if (in_bytes > 0){
			// Queue is full, handle rejection
			if (add_to_queue(*req, the_queue) == -1){
				// Reject timestamp
				clock_gettime(CLOCK_MONOTONIC, &reject_timestamp);

				// Rejection Response
				res.req_id = req->request.req_id;
				res.reserved = 0;
				res.ack = RESP_REJECTED;

				send_message = send(conn_socket, &res, sizeof(struct response), 0);
				if(send_message < 0){
					ERROR_INFO();
					perror("Unable to send response");
					break;
				}

				sync_printf("X%lu:%f,%f,%f\n", 
					req->request.req_id, 
					TSPEC_TO_DOUBLE(req->request.req_timestamp), 
					TSPEC_TO_DOUBLE(req->request.req_length), 
					TSPEC_TO_DOUBLE(reject_timestamp)
				);
				dump_queue_status(the_queue);
			}
		} else {
			// if in_bytes is closed or error receiving data, stop queuing
			break;
		}

		/* IMPLEMENT ME: Attempt to enqueue or reject request! */
	} while (in_bytes > 0);

	printf("out of the loop\n");

	for (size_t i = 0; i < worker_count; i++) {
        sem_post(queue_notify);  // Wake up all worker threads to check termination
    }

	printf("calling control_workers\n");

	/* IMPLEMENT ME!! Gracefully terminate all the worker threads ! */
	if (control_workers(1, worker_count, params) != 0){
		perror("Failed to end thread workers");
        queue_free(the_queue);
		free(params);
        return;
	}

	printf("ready to shutdown\n");

	free(req);
	queue_free(the_queue);
	free(params);

	shutdown(conn_socket, SHUT_RDWR);
	close(conn_socket);
	sync_printf("INFO: Client disconnected.\n");
}




/* Template implementation of the main function for the FIFO
 * server. The server must accept in input a command line parameter
 * with the <port number> to bind the server to. */
int main (int argc, char ** argv) {
	int sockfd, retval, accepted, optval, opt;
	in_port_t socket_port;
	struct sockaddr_in addr, client;
	struct in_addr any_address;
	socklen_t client_len;

	struct connection_params conn_params;

	/* Parse all the command line arguments */
	char *port_number;

	while ((opt = getopt(argc, argv, "q:w:")) != -1){
		/* PARSE THE COMMANDS LINE: */
		switch (opt) {
			/* 1. Detect the -q parameter and set aside the queue size in conn_params */
			case 'q':
				conn_params.qsize = atoi(optarg);; // Get the <size> value
				break;
			/* 2. Detect the -w parameter and set aside the number of threads to launch */
			case 'w':
				conn_params.worker_count = atoi(optarg); // Get the <workers> value
				break;
			case '?':
				fprintf(stderr, "Usage: %s -q <size> -w <workers> <port_number>\n", argv[0]);
                exit(EXIT_FAILURE);
		}
	}

	if (optind >= argc) {
		fprintf(stderr, "Expected <port_number> after options\n");
		exit(EXIT_FAILURE);
	}

	printf("INFO: setting queue size as: %ld\n", conn_params.qsize);
	printf("INFO: setting thread number as: %ld\n", conn_params.worker_count);

	port_number = argv[optind];

	/* 3. Detect the port number to bind the server socket to (see HW1 and HW2) */
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

	/* Initilize threaded printf mutex */
	printf_mutex = (sem_t *)malloc(sizeof(sem_t));
	retval = sem_init(printf_mutex, 0, 1);
	if (retval < 0) {
		ERROR_INFO();
		perror("Unable to initialize printf mutex");
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
	/* DONE - Initialize queue protection variables */


	/* Ready to handle the new connection with the client. */
	handle_connection(accepted, conn_params);

	free(queue_mutex);
	free(queue_notify);
	free(printf_mutex);


	close(sockfd);
	return EXIT_SUCCESS;
}
