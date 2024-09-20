/*******************************************************************************
* CPU Clock Measurement Using RDTSC
*
* Description:
*     This C file provides functions to compute and measure the CPU clock using
*     the `rdtsc` instruction. The `rdtsc` instruction returns the Time Stamp
*     Counter, which can be used to measure CPU clock cycles.
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
* Last Update:
*     September 9, 2024
*
* Notes:
*     Ensure that the platform supports the `rdtsc` instruction before using
*     these functions. Depending on the CPU architecture and power-saving
*     modes, the results might vary. Always refer to the CPU's official
*     documentation for accurate interpretations.
*
*******************************************************************************/

#include <stdio.h>
#include <string.h>
#include <time.h>
#include <stdint.h>
#include <stdlib.h>
#include <unistd.h>

#include "timelib.h"

double wait_time(long sec, long nsec){
	return (double)sec + (double)nsec / NANO_IN_SEC;
}

int main (int argc, char ** argv)
{
	/* IMPLEMENT ME! */
	long sec, nsec;
	char method;
	uint64_t elapsed_clock_cycles;
	double clock_speed;

	// Check Input Parameter
	if (argc != 4){
		perror("Need 3 parameters: seconds, nanoseconds, waitMethod");
		return EXIT_FAILURE;
	}

	// Take Input Parameter
	sec = strtol(argv[1], NULL, 10);
	nsec = strtol(argv[2], NULL, 10);
	method = argv[3][0];

	if (method != 's' && method != 'b'){
		perror("Invalid wait method. Need to use right method");
		return EXIT_FAILURE;
	}

	switch (method){
		case 's':
			printf("WaitMethod: SLEEP\n");
			printf("WaitTime: %ld %ld\n", sec, nsec);
			elapsed_clock_cycles = get_elapsed_sleep(sec, nsec);
			break;
		case 'b':
			printf("WaitMethod: BUSYWAIT\n");
			printf("WaitTime: %ld %ld\n", sec, nsec);
			elapsed_clock_cycles = get_elapsed_busywait(sec, nsec);
			break;
	}
	double elapsed_wait_time = wait_time(sec, nsec);
	if (elapsed_wait_time > 0) {
        clock_speed = (double)elapsed_clock_cycles / elapsed_wait_time;
		clock_speed = clock_speed / 1e6; //Convert Hz to MHz
        printf("ClocksElapsed: %llu\n", (unsigned long long)elapsed_clock_cycles);
        printf("ClockSpeed: %f\n", clock_speed);
    } else {
        fprintf(stderr, "Error calculating elapsed wait time.\n");
        return EXIT_FAILURE;
    }

	return EXIT_SUCCESS;
}

