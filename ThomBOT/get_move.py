def _get_move(ai,m):
    import numpy as np
    own = ai.you.pos
    m.prev_pos.append(own)
    opp_dict = {0:2, 1:3, 2:0, 3:1}
    #if len(m.prev_pos) > 3:
    #    if len(set(m.prev_pos[-3:]))==1:
    #        return opp_dict[m.prev_move[-1]]
    move = -1
    #neighbors = list(m.get_neighbours_of(own))
    #valid_nextpos =[n for n in neighbors if n in m.game_positions]
    #valid_moves = [m.get_move_between(own, n) for n in valid_nextpos]
    #print("Valid_moves", valid_moves)
    random_move = np.random.choice(4, 1)
    print("Own pos:", own)
    if ai.states.no_danger:
        print("NO DANGER OR BOTH DANGEROUS")
        if m.super_pellets_left > 0:
            paths = [(len(m.get_astar_path(own, x)),m.get_astar_path(own, x))  for x in list(m.super_pellets_positions)]
            shortest = list(sorted(paths, key=lambda x: x[0]))[0]
            path = shortest[1]
            nextpos = path[0]
            print("Next pos: ", nextpos)
            move = m.get_move_between(own, nextpos)
            print("Move: ", move)
            return move
        if m.pellets_left > 0:
            if len(list(m.pellet_positions))>1:
                goal = list(m.pellet_positions)
                paths = [(m.get_manhattan_dist(own, x),m.get_astar_path(own, x))  for x in goal]
                shortest = list(sorted(paths, key=lambda x: x[0]))[0]
                path = shortest[1]
                nextpos = path[0]
                print("Next pos: ", nextpos)
                move = m.get_move_between(own, nextpos)
                print("Move: ", move)
                return move
            else:
                return random_move
                
    if ai.states.you_are_dangerous and not ai.states.enemy_is_dangerous:
        print("YOU ARE DANGEROUS BOT NOT ENEMY. GET HIM")
        goal = ai.enemy.pos
        path = m.get_astar_path(own, goal)
        nextpos = path[0]
        print("Next pos: ", nextpos)
        move = m.get_move_between(own, nextpos)
        print("Move: ", move)
        return move
    
    if ai.states.enemy_is_dangerous and not ai.states.you_are_dangerous:
        print("ENEMY IS DANGEROUS")
        goal = ai.enemy.pos
        path = m.get_astar_path(own, goal)
        nextpos = path[0]
        print("Next pos: ", nextpos)
        opp_move = m.get_move_between(own, nextpos)
        move = opp_dict[opp_move]
        print("Move: ", move)
        return move

    
    if ai.states.monster_on_map:
        print("MONSTER IN MAP")
        try:
            goal = list(m.pellet_positions)
        except:
            return random_move
        paths = [(m.get_manhattan_dist(own, x),m.get_astar_path(own, x))  for x in goal]
        shortest = list(sorted(paths, key=lambda x: x[0]))[0]
        path = shortest[1]
        nextpos = path[0]
        print("Next pos: ", nextpos)
        move = m.get_move_between(own, nextpos)
        print("Move: ", move)
        return move
    return random_move
