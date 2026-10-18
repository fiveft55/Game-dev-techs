// Original MIT-licensed portable C interface; all linked units must use the same capacity.
#ifndef GAME_COMBAT_FRAMES_H
#define GAME_COMBAT_FRAMES_H
#include <stddef.h>
#ifndef PORT_CAPACITY
#define PORT_CAPACITY 4096
#endif
#ifndef GAME_PORT_VECTOR_DEFINED
#define GAME_PORT_VECTOR_DEFINED
typedef struct { double values[PORT_CAPACITY]; size_t count; } PortVector;
#endif
PortVector game_combat_frames_compute(PortVector input);
#endif
