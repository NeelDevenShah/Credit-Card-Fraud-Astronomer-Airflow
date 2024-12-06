import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping
import joblib

def train_model():
    # Load preprocessed data
    X = pd.read_csv('/tmp/X.csv')
    y = pd.read_csv('/tmp/y.csv')

    # Define the Neural Network model
    model = Sequential([
        Dense(64, input_dim=X.shape[1], activation='relu'),
        Dropout(0.3),
        Dense(32, activation='relu'),
        Dense(1, activation='sigmoid')
    ])

    # Compile the model
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    # Train the model
    early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)
    model.fit(X, y, validation_split=0.2, epochs=50, batch_size=32, callbacks=[early_stopping])

    # Save the model
    model.save('/tmp/model_nn.h5')
