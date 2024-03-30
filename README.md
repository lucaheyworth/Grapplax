## Grapplax
This a platform game using ursina game engine that involves a character grappling on to platform and getting to the top without running out off grapples or getting killed.

## The code
This is like the main structure of the code:

const > app
const > ground
const > player
const > current_level
const > game_over
const > code_ran
const > code_ran_2
const > grapples
const > grapple_counter
func > update
class > Platform:
    func > __init__
    func > on_click
class > Grapple:
    func > __init__
    func > update
class SuperGrapple:
    func > __init__
    func > update
    const > code_ran_1
class EleKill:
    func > __init__
    func > update
    func > on_click
class levels
