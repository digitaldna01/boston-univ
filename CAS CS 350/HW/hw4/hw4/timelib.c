/*******************************************************************************
* Time Functions Library (implementation)
*
* Description:
*     A library to handle various time-related functions and operations.
*
* Author:
*     Renato Mancuso <rmancuso@bu.edu>
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
*     Ensure to link against the necessary dependencies when compiling and
*     using this library. Modifications or improvements are welcome. Please
*     refer to the accompanying documentation for detailed usage instructions.
*
*******************************************************************************/

#include "timelib.h"

/* Return the number of clock cycles elapsed when waiting for
 * wait_time seconds using sleeping functions */
uint64_t get_elapsed_sleep(long sec, long nsec)
{
	uint64_t start_clock, end_clock;
	
	// Initiate timespec struct
	struct timespec sleep_time;
	sleep_time.tv_sec = sec;
	sleep_time.tv_nsec = nsec;

	// function to snapshot start TSC
	get_clocks(start_clock);

	if(nanosleep(&sleep_time, NULL) == -1){
		perror("Unable to nanosleep");
		return EXIT_FAILURE;
	};
	
	// funtion to snapshot end TSC
	get_clocks(end_clock);
	// return the difference between the second and first TSC value
	return (end_clock - start_clock);
}

/* Return the number of clock cycles elapsed when waiting for
 * wait_time seconds using busy-waiting functions */
uint64_t get_elapsed_busywait(long sec, long nsec)
{
	struct timespec delay;
	delay.tv_sec = sec;
	delay.tv_nsec = nsec;

	return busywait_timespec(delay);
}

/* Utility function to add two timespec structures together. The input
 * parameter a is updated with the result of the sum. */
void timespec_add (struct timespec * a, struct timespec * b)
{
	/* Try to add up the nsec and see if we spill over into the
	 * seconds */
	time_t addl_seconds = b->tv_sec;
	a->tv_nsec += b->tv_nsec;
	if (a->tv_nsec > NANO_IN_SEC) {
		addl_seconds += a->tv_nsec / NANO_IN_SEC;
		a->tv_nsec = a->tv_nsec % NANO_IN_SEC;
	}
	a->tv_sec += addl_seconds;
}

/* Utility function to compare two timespec structures. It returns 1
 * if a is in the future compared to b; -1 if b is in the future
 * compared to a; 0 if they are identical. */
int timespec_cmp(struct timespec *a, struct timespec *b)
{
	if(a->tv_sec == b->tv_sec && a->tv_nsec == b->tv_nsec) {
		return 0;
	} else if((a->tv_sec > b->tv_sec) ||
		  (a->tv_sec == b->tv_sec && a->tv_nsec > b->tv_nsec)) {
		return 1;
	} else {
		return -1;
	}
}

/* Busywait for the amount of time described via the delay
 * parameter */
uint64_t busywait_timespec(struct timespec delay)
{
	uint64_t start_clock, end_clock;

	// Initiate timespec struct
	struct timespec begin_timestamp, current_time, target_time;

	// Retrieve the current system time and save it to begin_timestamp
	clock_gettime(CLOCK_MONOTONIC, &begin_timestamp);

	// Add delay time to begin_timestamp to find out target time
	target_time = begin_timestamp;
	timespec_add(&target_time, &delay);

	// Snapshot the start TSC value
	get_clocks(start_clock);
	
	//wait given time
	while(1){

		// Retrieve the current system time
		clock_gettime(CLOCK_MONOTONIC, &current_time);

		// Compare the current time and target time and check if the target time is passed
		if(timespec_cmp(&current_time, &target_time) >= 0){
			break;
		}
	}

	// Snapshot the end TSC value
	get_clocks(end_clock);

	// return the difference between the second and first TSC value
	return (end_clock - start_clock);
}
