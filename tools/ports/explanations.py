"""Beginner explanations shared by documentation and native code comments."""
# Each entry: a one-sentence purpose and small steps in everyday language.
EXPLANATIONS = {
'fixed-timestep': ('Make the game take equal-sized time steps, even when the screen draws at different speeds.', [
    'Imagine a bucket collecting seconds as the game runs.', 'Take one scoop of time for each game update.', 'Keep the leftover time for the next update.', 'After a big pause, throw away excess time so the game does not spend forever catching up.']),
'player-movement': ('Move a player in the direction they press, without making diagonal movement faster.', [
    'Read where the player is and which direction they want to go.', 'If the direction arrow is too long, shrink it to length one.', 'Multiply that direction by speed and the time that passed.', 'Add the result to the old position.']),
'aabb-collision': ('Tell whether two upright rectangular boxes touch or overlap.', [
    'Look at the left and right edges of both boxes.', 'Look at the top and bottom edges too.', 'If there is a gap on either side-to-side or up-and-down check, they do not touch.', 'Return one for touching and zero for separate. Touching edges count.']),
'grid-pathfinding': ('Find the shortest walking route through a small square-tile map.', [
    'Start on the player tile and put it in a waiting line.', 'Check nearby tiles: right, left, down, and up. Skip walls and already checked tiles.', 'Remember which tile led to each new tile.', 'When the target is found, follow those memories backward and reverse them to get the route.']),
'raycasting': ('Send an invisible straight line through a tile map and report the first wall it hits.', [
    'Start the line at a position and choose its direction.', 'Calculate which tile edge the line will cross next.', 'Move into that next tile and check whether it is a wall.', 'Stop at a wall, the map edge, or the step limit. The returned time-like number tells how far along the line the hit occurred.']),
'rigid-body-integration': ('Update a moving point when a force-like acceleration, such as gravity, changes its speed.', [
    'Start with position and speed in each direction.', 'Acceleration changes speed during the time step.', 'Use the new speed to change position.', 'This moves a point; it does not stop that point from falling through floors.']),
'steering-arrival': ('Make an enemy or vehicle slow down as it reaches its target.', [
    'Draw an arrow from the object to the target.', 'Measure how far away the target is.', 'Far away means full speed. Nearby means a smaller speed.', 'Return the wanted speed in each direction; another controller must actually apply it.']),
'finite-state-machine': ('Let a character switch between named situations, such as idle and jumping, using clear rules.', [
    'Keep one current state, represented here by a number.', 'Read the next event, such as a jump button press.', 'Find a rule matching the current state and that event.', 'Switch to the rule destination. If no rule matches, keep the old state.']),
'inventory': ('Put items into piles without making any pile or backpack too full.', [
    'Fill existing piles of the same item first.', 'Put leftover items into new piles while free backpack slots remain.', 'Never put more than the pile limit into one pile.', 'Return the new piles and how many items could not fit. Item numbers are labels, not quantities.']),
'ascii-world': ('Draw a tiny world using keyboard characters instead of pictures.', [
    'Read the map one row at a time.', 'Turn a floor tile into a dot and a wall tile into a hash sign.', 'Put an at sign where the player stands.', 'Put a new line between rows. The native ports return character numbers: 46 is dot, 35 is hash, and 64 is at sign.']),
'procedural-maze': ('Build a new maze by digging paths through a wall-filled map.', [
    'Fill the map with walls and open one starting square.', 'Pick a nearby unopened room using a repeatable number generator.', 'Break the wall between the old room and the new room.', 'When stuck, walk back through the remembered rooms until another path can be dug.']),
'camera-follow': ('Make the camera catch up gently instead of snapping straight to its target.', [
    'Find the gap between the camera and its target.', 'Use the time step and follow strength to choose how much of that gap to close.', 'Move part of the way across the gap.', 'Repeat next update. Bigger strength catches up faster.']),
'spatial-hash': ('Find nearby objects by grouping their positions into imaginary square boxes.', [
    'Choose the size of each imaginary box.', 'Work out which box contains the search position.', 'Find objects in that box or any of its eight neighboring boxes.', 'These are possible neighbors, not guaranteed touching objects. Check exact distance afterward.']),
'racing-bicycle-model': ('Move a simple car forward and bend its direction when the wheels steer.', [
    'Move the car along its current facing direction.', 'Use steering angle, speed, and axle spacing to decide how much it turns.', 'Update the facing direction for the next step.', 'This is a simple no-skidding model, not a realistic tire or suspension simulation.']),
'snapshot-interpolation': ('Draw another player between two known positions so their movement looks less jumpy.', [
    'Read an older position and a newer position, each with a time.', 'Find where the drawing time sits between those times.', 'Move the same fraction of the way between the two positions.', 'If drawing time is outside the pair, use the nearest endpoint rather than guessing ahead.']),
'replay-window': ('Reject a repeated or very old network message while still allowing slightly late messages.', [
    'Each message carries a counting number.', 'Remember recently accepted numbers and the biggest number seen.', 'Reject numbers already remembered or too far behind the biggest number.', 'Only do this AFTER the network security layer proves the message is genuine. This code does not encrypt anything.']),
'level-editor-undo': ('Let a map editor undo and redo painting a tile.', [
    'Before painting, remember the old tile and the new tile.', 'Undo restores the old tile and moves backward in the edit history.', 'Redo puts the new tile back and moves forward.', 'Painting after undo throws away the abandoned future edits.']),
'cad-extrusion': ('Give a flat outline height to make a simple solid-looking 3D shape.', [
    'Copy the outline at floor height and at the requested top height.', 'Cover the bottom and top with triangles.', 'Connect matching bottom and top edges with more triangles.', 'Return points and triangle point-numbers. The outline must be simple, convex, and listed counterclockwise.']),
'score-lives': ('Count points, award extra lives, and remove a life after a mistake.', [
    'Add each points award to the total.', 'Count how many extra-life marks the score crossed.', 'Give one life for each mark crossed, even if one big award crosses several.', 'A death removes one life, but lives never go below zero.']),
'jump-controller': ('Make jumping feel forgiving when the button press is slightly early or slightly late.', [
    'Remember the last time the character touched the ground.', 'Remember the last time the jump button was pressed.', 'Allow a jump if those memories are still recent enough.', 'Use up that jump so one press cannot keep creating jumps in mid-air. A new landing restores it.']),
'projectile-sweep': ('Check whether a fast bullet passed through a box between two updates.', [
    'Draw the entire line from the bullet old position to its new position.', 'Find the part of that line that is inside the box left-to-right.', 'Find the part that is inside the box bottom-to-top.', 'If those parts overlap, return the first hit point as a fraction of the move. A fraction of 0.4 means 40 percent along.']),
'combat-frames': ('Split an attack into wind-up, dangerous time, and recovery time.', [
    'During wind-up the attack is not ready to hurt anyone.', 'During active frames an overlapping target may be hit.', 'Remember each target already hit so one swing does not hit it every update.', 'During recovery or after the attack, do not accept new hits.']),
'line-of-sight': ('Tell whether a character can see another tile without a wall blocking the view.', [
    'Walk a straight line from the starting tile center to the target tile center.', 'Check every tile touched by the line.', 'When the line crosses a corner, check both side tiles too.', 'Any wall blocks sight. This prevents seeing through two walls that meet diagonally.']),
'rpg-progression': ('Turn experience points into a level and calculate a very simple damage amount.', [
    'Store the experience amount needed to start each level.', 'Count how many level marks the player has reached.', 'Subtract armor from attack power to get damage.', 'Never let damage fall below zero. You can replace this simple rule with your own balance formula.']),
'quest-objectives': ('Track jobs such as collecting two logs and talking to one villager.', [
    'Give each job a target count.', 'Add progress when its event happens.', 'Stop each counter at its target; extra logs do not make the counter run forever.', 'The quest is complete only when every job is complete. Persistent reward claiming needs extra storage rules.']),
'dialogue-graph': ('Choose which conversation options are allowed and where the conversation goes next.', [
    'Keep the current conversation node and simple yes-or-no story flags.', 'Look for the chosen event among options leaving that node.', 'Require the necessary flags before allowing the choice.', 'Grant new flags and move to the next node. Flag values 1, 2, and 4 are separate switches; adding them can store several switches together.']),
 'turn-order': ('Decide whose turn comes next and remove characters who leave the fight.', [
    'Put faster characters first.', 'If speeds tie, use the smaller character number first so the result is repeatable.', 'Advance to the next character and wrap around at the end.', 'When someone leaves, keep the right next character rather than accidentally skipping them.']),
'resource-economy': ('Buy or produce something only if you can pay its whole cost.', [
    'Check every required resource before changing anything.', 'If any resource is short, leave the balances alone.', 'Otherwise subtract all costs and add all outputs.', 'This is local arithmetic; a shared online economy needs a real database transaction too.']),
'fog-of-war': ('Hide unexplored parts of a map while remembering places the player has already seen.', [
    'Find tiles close enough to each observer.', 'Mark those tiles visible right now.', 'Keep old explored marks even when the observer moves away.', 'The portable version checks distance only; add wall blocking separately.']),
'wave-spawner': ('Release enemies at planned times without accidentally releasing them twice.', [
    'Keep a time-ordered list of enemies to create.', 'On each update, compare the game clock with the next enemy time.', 'Release every enemy whose time has arrived, including several after a slow frame.', 'Move the list cursor forward so released enemies are not repeated.']),
'event-scheduler': ('Do planned simulation jobs in time order.', [
    'Give each job a time and a job number.', 'Sort the jobs from early to late.', 'Keep original order when two jobs share the same time.', 'Return jobs due by the requested time. The portable kernel processes a batch rather than maintaining a live clock service.']),
'racing-checkpoints': ('Count a racing lap only after the driver visits every checkpoint in order.', [
    'Start by expecting checkpoint zero.', 'Ignore a checkpoint reached out of order.', 'Do not count the same overlap again until the car leaves it.', 'After the last checkpoint, add one lap and expect checkpoint zero again.']),
'ball-reflection': ('Make a ball bounce off a wall or floor.', [
    'Describe which way the surface faces using a short arrow called a normal.', 'If the ball is already moving away, do not bounce it again.', 'Reverse the part of its speed going into the surface.', 'Use restitution, a number from zero to one, to choose how much bounce remains. Sideways speed stays unchanged.']),
'match-grid': ('Remove matching rows or columns of tiles, then let the remaining tiles fall down.', [
    'Find long enough runs of identical nonempty tiles.', 'Mark each matching tile once, even where a row and column cross.', 'Remove all marked tiles together.', 'Slide surviving tiles to the bottom of each column without changing their order.']),
'rhythm-judgement': ('Tell whether a music-game button press was close enough to a note time.', [
    'Correct the recorded press time for measured input delay.', 'Compare it with the planned note time.', 'A very small gap means perfect; a larger allowed gap means good.', 'Ignore presses too far away. A separate audio-clock rule must mark notes missed after their deadline.']),
'crafting-recipes': ('Turn ingredients into products, such as two pieces of wood becoming three planks.', [
    'Multiply ingredient and product counts by the number of batches.', 'Check that the backpack has every ingredient.', 'If anything is missing, change nothing.', 'Otherwise take the ingredients first, then add the products. Products cannot pay for their own ingredients.']),
'chunk-coordinates': ('Find which big map piece owns a world tile, and where that tile sits inside the piece.', [
    'Divide the world coordinate by the piece size and round downward.', 'That gives the chunk, or big piece, number.', 'Subtract the chunk start to get the local tile number.', 'Rounding downward matters: world tile -1 is in chunk -1, at the last local tile.']),
'interest-management': ('Send a player only nearby objects they are allowed to know about.', [
    'The trusted server decides which objects this player may see.', 'Check how far each allowed object is from the player.', 'Keep only the ones inside the chosen range.', 'Return their IDs. This does not encrypt data or decide authorization by itself.']),
'shrinking-zone': ('Shrink a battle-royale safe circle and hurt players standing outside it.', [
    'Find how far the current time is through this shrinking phase.', 'Move the circle center and radius partway from the old values to the new ones.', 'Check whether the player is outside the circle.', 'If outside, apply damage rate times the update duration.']),
'ballot-resolution': ('Count a vote and choose one player to remove only when there is a clear winning choice.', [
    'Accept at most one vote from each eligible voter.', 'Count votes for eligible candidates; minus one means skip.', 'Find the largest vote count.', 'A tie, no votes, or a winning skip vote removes nobody.']),
'deck-draw': ('Shuffle a card pile, draw cards, and reuse discarded cards when the pile runs out.', [
    'Shuffle by swapping cards using a repeatable number generator.', 'Drawing removes the last card from the pile.', 'If the pile is empty, shuffle the discard pile into a new draw pile.', 'If both piles are empty, return the no-card marker. This predictable shuffle is not secure against cheaters.']),
'spaced-repetition': ('Choose when a learning question should be asked again.', [
    'Read the previous waiting period and whether the answer was correct.', 'A correct answer doubles the wait, starting at one day.', 'An incorrect answer resets the wait to one day.', 'Add that wait to the current time to get the next review time. This is a simple teaching example, not a proven learning model.']),
'offline-progress': ('Give an idle-game player resources for time spent away, up to a limit.', [
    'Subtract the last saved time from the current time.', 'If the clock moved backward, count zero time.', 'Limit the counted time so a very long absence does not give unlimited rewards.', 'Multiply counted seconds by production rate. Online games must use trusted time and prevent claiming twice.']),
'save-migration': ('Update an old decoded save record into the current small save format.', [
    'Read the format version and the gold count.', 'Accept supported old/current versions only.', 'Reject negative or fractional gold counts.', 'Return version two with the same gold amount. Reading and validating JSON text is a separate job in these native kernels.']),
'ability-cooldown': ('Stop an ability from being used again until a charge has recovered.', [
    'Each use spends one available charge.', 'Remember the time when that charge will return.', 'Before the next attempt, restore charges whose waiting time has ended.', 'Allow the attempt only if at least one charge is available. Each charge waits independently.']),
'loot-table': ('Choose an item from a weighted prize list.', [
    'Imagine each item owns a strip of numbered raffle tickets.', 'Bigger weights give an item more tickets.', 'Find which item owns the supplied ticket number.', 'Return that item. Another part of the game must choose a fair ticket; this code does not generate secure randomness.']),
'rollback-resimulation': ('Fix an old game state, then redo later moves so the present agrees with that correction.', [
    'Keep the state before and after each numbered update.', 'Replace the state at the corrected update with the trusted value.', 'Apply every later recorded input again.', 'Return the corrected history. Do not replay real-world side effects such as charging money.']),
'server-input-validation': ('Let the server move a player from allowed directions instead of trusting a claimed player position.', [
    'Require a newer whole-number message sequence.', 'Reject direction arrows longer than one.', 'Use server-owned speed and update time to calculate movement.', 'Ignore rejected commands. Network parsing, authentication, finite-number checks and one-command-per-tick limits belong at the server boundary.']),
'animation-timeline': ('Choose which picture of an animation should be shown at a given time.', [
    'Give every picture a positive display duration.', 'Add durations until reaching the requested time.', 'Choose the picture covering that moment.', 'Loop back to the beginning for repeating animation, or hold the last picture for a one-shot animation.']),
'building-placement': ('Place a building footprint on a tile map only if every required square is free.', [
    'Rotate the footprint by the requested number of quarter turns.', 'Move it to the chosen anchor tile.', 'Check that every square is inside the map and unoccupied.', 'If any square fails, place nothing. Otherwise mark all footprint squares occupied together.']),
}

HELPERS = {
'length':'Count how many numbers are in this list.',
'get':'Read one number at a zero-based position; stop if that position does not exist.',
'put':'Replace a number at an existing position in the list.',
'push':'Add one number to the end of the list.',
'pop_value':'Remove the last number from the list and return it.',
'index':'Check that a position is a whole number inside the list before using it.',
'copy':'Make a separate list so editing it cannot change the old list.',
'minimum':'Choose the smaller of two numbers.',
'maximum':'Choose the larger of two numbers.',
'floor_num':'Round down to a whole number; minus 0.1 becomes minus 1.',
'sqrt_num':'Find the number that multiplies by itself to make the input; useful for distance.',
'abs_num':'Remove a negative sign so a distance or size is not negative.',
'exp_num':'Calculate exponential growth/decay, used here to make smooth catching-up motion.',
'sin_num':'Get the up/down part of a unit direction from an angle measured in radians.',
'cos_num':'Get the left/right part of a unit direction from an angle measured in radians.',
'tan_num':'Convert a steering angle into a turning ratio; angles here are in radians.',
'mod_num':'Return the remainder after dividing one number by another.',
}
