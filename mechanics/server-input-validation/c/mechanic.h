// Original MIT-licensed portable C interface; all linked units must use the same capacity.
#ifndef GAME_SERVER_INPUT_VALIDATION_H
#define GAME_SERVER_INPUT_VALIDATION_H
#include <stddef.h>
#ifndef PORT_CAPACITY
#define PORT_CAPACITY 4096
#endif
#ifndef GAME_PORT_VECTOR_DEFINED
#define GAME_PORT_VECTOR_DEFINED
typedef struct { double values[PORT_CAPACITY]; size_t count; } PortVector;
#endif
PortVector game_server_input_validation_compute(PortVector input);
#endif
