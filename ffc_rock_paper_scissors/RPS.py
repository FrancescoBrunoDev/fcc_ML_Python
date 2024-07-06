def player(prev_play, opponent_history=[]):
    global abbey_pattern
    if not prev_play:
        opponent_history.clear()
        player.play_order = {}
        player.my_history = []
        abbey_pattern = {'R': 0, 'P': 0, 'S': 0}
    
    opponent_history.append(prev_play)
    
    # Aggiorna il conteggio delle mosse di abbey
    if prev_play in abbey_pattern:
        abbey_pattern[prev_play] += 1
    
    # Estendi l'analisi dei pattern
    pattern_length = 5
    while pattern_length > 2:
        if len(opponent_history) > pattern_length:
            key = ''.join(opponent_history[-pattern_length:])
            player.play_order[key] = player.play_order.get(key, 0) + 1
        pattern_length -= 1

    prediction = predict_next_move(opponent_history, abbey_pattern)

    # Scegli la contromossa ideale
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    counter_move = ideal_response[prediction]

    player.my_history.append(counter_move)
    return counter_move

def predict_next_move(opponent_history, abbey_pattern):
    if len(opponent_history) < 3:
        # Scegli la mossa meno frequente di abbey per aumentare le possibilità di vittoria
        least_common_move = min(abbey_pattern, key=abbey_pattern.get)
        return {'R': 'P', 'P': 'S', 'S': 'R'}[least_common_move]
    
    potential_plays = [
        ''.join(opponent_history[-3:] + [r]) for r in ['R', 'P', 'S']
    ]
    
    sub_order = {
        k: player.play_order.get(k, 0)
        for k in potential_plays
    }

    if max(sub_order.values()) > 0:
        return max(sub_order, key=sub_order.get)[-1:]
    else:
        # Se non ci sono pattern chiari, usa la strategia contro la mossa meno frequente di abbey
        least_common_move = min(abbey_pattern, key=abbey_pattern.get)
        return {'R': 'P', 'P': 'S', 'S': 'R'}[least_common_move]