from datasets import GamesTrainingDataset, GamesValidationDataset
from models import MatchPredictorModel
import os
import keras
import tensorflow as tf


def main():
    training_data = GamesTrainingDataset()
    val_data = GamesValidationDataset()

    batch_size = 32
    epochs = 100
    version = '1'
    log_dir = os.path.join(os.path.dirname(__file__), 'logs')
    checkpoint_dir = os.path.join(os.path.dirname(__file__), 'checkpoints', version)
    save_path = os.path.join(os.path.dirname(__file__), 'saved_models', version)

    model = MatchPredictorModel()

    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    if not os.path.exists(checkpoint_dir):
        os.makedirs(checkpoint_dir)
    else:
        print("Found checkpoint. Loading weights")
        model.load_weights(checkpoint_dir)

    model.compile(optimizer='adam', loss='categorical_crossentropy')

    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=5),
        tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_dir),
        tf.keras.callbacks.TensorBoard(log_dir=log_dir)
    ]

    training_data = training_data.shuffle(4000).cache().batch(batch_size)
    val_data = val_data.shuffle(1000).cache().batch(batch_size)

    model.fit(training_data, epochs=epochs, validation_data=val_data, callbacks=callbacks)

    model.save(save_path, overwrite=True, include_optimizer=False)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()