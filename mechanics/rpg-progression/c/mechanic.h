// Original MIT-licensed portable C interface; all linked units must use the same capacity.
#ifndef GAME_RPG_PROGRESSION_H
#define GAME_RPG_PROGRESSION_H
#include <stddef.h>
#ifndef PORT_CAPACITY
#define PORT_CAPACITY 4096
#endif
#ifndef GAME_PORT_VECTOR_DEFINED
#define GAME_PORT_VECTOR_DEFINED
typedef struct { double values[PORT_CAPACITY]; size_t count; } PortVector;
#endif
PortVector game_rpg_progression_compute(PortVector input);
#endif
