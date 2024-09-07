# Makefile

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra

# Build target
all: echo reverse

# Linking and creating the echo executable
echo: echo.o
	$(CC) -o $@ $@.o

# Linking and creating the reverse executable
reverse: reverse.o
	$(CC) -o $@ $@.o

# Generic rule to compile .c files into .o files
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up
clean:
	rm -f echo reverse *.o
