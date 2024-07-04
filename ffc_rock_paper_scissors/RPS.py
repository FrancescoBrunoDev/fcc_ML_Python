import random
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Embedding

# Generate a dataset of simulated RPS games
def generate_rps_data(num_games=10000):
    choices = ['R', 'P', 'S']
    data = []
    for _ in range(num_games):
        prev_play = random.choice(choices)
        next_play = random.choice(choices)
        data.append((prev_play, next_play))
    return data

data = generate_rps_data()

# Manual encoding and decoding
move_to_int = {'R': 0, 'P': 1, 'S': 2}
int_to_move = {0: 'R', 1: 'P', 2: 'S'}

# Prepare the data for training
def prepare_data(data):
    prev_moves = [move[0] for move in data]
    next_moves = [move[1] for move in data]

    prev_moves_encoded = np.array([move_to_int[move] for move in prev_moves]).reshape(-1, 1)
    next_moves_encoded = np.array([move_to_int[move] for move in next_moves])

    return prev_moves_encoded, next_moves_encoded

prev_moves_encoded, next_moves_encoded = prepare_data(data)

# Build the model
model = Sequential([
    Embedding(input_dim=3, output_dim=10, input_length=1),
    LSTM(50, return_sequences=False),
    Dense(3, activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train the model
model.fit(prev_moves_encoded, next_moves_encoded, epochs=20, batch_size=15)

# Save the model
model.save('./models/rps_model.keras')

# Load the model
# model = tf.keras.models.load_model('./models/rps_model.keras')

# Player function using the trained model
def player(prev_play, opponent_history=[]):
    if not prev_play:
        prev_play = 'R'
        
    opponent_history.append(prev_play)
    
    if len(opponent_history) < 2:
        return random.choice(['R', 'P', 'S'])
    
    # Prepare the input for the model
    prev_play_encoded = np.array([move_to_int[prev_play]]).reshape(-1, 1)
    
    # Predict the opponent's next move
    prediction = model.predict(prev_play_encoded)
    predicted_move = int_to_move[np.argmax(prediction)]

    # Choose a move that beats the predicted move
    ideal_response = {'P': 'S', 'R': 'P', 'S': 'R'}
    return ideal_response[predicted_move]

# Example function calls for playing the game
# The play function would be defined elsewhere, as requested
# win_rate = play(player, random_player, num_games=1000, verbose=True)
