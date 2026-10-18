// Original MIT-licensed portable C interface; all linked units must use the same capacity.
#ifndef GAME_WAVE_SPAWNER_H
#define GAME_WAVE_SPAWNER_H
#include <stddef.h>
#ifndef PORT_CAPACITY
#define PORT_CAPACITY 4096
#endif
#ifndef GAME_PORT_VECTOR_DEFINED
#define GAME_PORT_VECTOR_DEFINED
typedef struct { double values[PORT_CAPACITY]; size_t count; } PortVector;
#endif
PortVector game_wave_spawner_compute(PortVector input);
#endif
