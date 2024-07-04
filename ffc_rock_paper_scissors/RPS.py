def player(prev_play, opponent_history=[]):
    if not prev_play:
        opponent_history.clear()
        player.play_order = {}
        player.my_history = []
    
    opponent_history.append(prev_play)
    
    # Track patterns of opponent's plays
    if len(opponent_history) > 4:
        key = ''.join(opponent_history[-5:])
        player.play_order[key] = player.play_order.get(key, 0) + 1

    # Predict next move based on observed patterns
    if len(opponent_history) > 4:
        potential_plays = [
            ''.join(opponent_history[-4:] + [r]) for r in ['R', 'P', 'S']
        ]
        
        sub_order = {
            k: player.play_order.get(k, 0)
            for k in potential_plays
        }

        if max(sub_order.values()) > 0:
            prediction = max(sub_order, key=sub_order.get)[-1:]
        else:
            prediction = ['R', 'P', 'S'][len(opponent_history) % 3]
    else:
        prediction = ['R', 'P', 'S'][len(opponent_history) % 3]

    # Choose counter move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    counter_move = ideal_response[prediction]

    player.my_history.append(counter_move)
    return counter_move