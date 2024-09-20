#include <sys/types.h>
#include <sys/socket.h>
#include <sys/time.h>
#include <math.h>

/* Includes that are specific for TCP/IP */
#include <netinet/in.h>
#include <netinet/ip.h> /* superset of previous */

/* Includes that are specific for TCP/IP */
#include <netinet/in.h>
#include <netinet/ip.h> /* superset of previous */

/* Include our own timelib */
#include "timelib.h"

/* This is a handy definition to print out runtime errors that report
 * the file and line number where the error was encountered. */
#define ERROR_INFO()							\
	fprintf(stderr, "Runtime error at %s:%d\n", __FILE__, __LINE__)

/* A simple macro to convert between a struct timespec and a double
 * representation of a timestamp. */
#define TSPEC_TO_DOUBLE(spec)				\
    ((double)(spec.tv_sec) + (double)(spec.tv_nsec)/NANO_IN_SEC)

/* Request payload as sent by the client and received by the
 * server. */
struct request {
	/* ADD REQUEST FIELDS. */
	uint64_t id; //Id of request
	struct timespec timestamp; // timestamp at which the client sent the request
	struct timespec length; // length of the request
};

/* Response payload as sent by the server and received by the
 * client. */
struct response {
	/* ADD RESPONSE FIELDS. */
	uint64_t id; // Id of handled request
	uint64_t reserved; // Reserved 64-bit field
	uint8_t ack; // 8-bit acknowledgment value

};
