from abc import ABC

import tensorflow as tf
import keras
from keras import layers

from datasets import GamesValidationDataset


class MatchPredictorModel(keras.Model, ABC):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.model = self._get_network()

    def _get_conv_block(self, inputs):
        a = layers.Conv1D(64, 3, padding='same', activation='elu')(inputs)
        a = layers.Conv1D(64, 3, padding='same', activation='elu')(a)
        a = layers.BatchNormalization(1)(a)
        a = layers.Dropout(0.5)(a)
        a = layers.MaxPool1D()(a)  # 36
        a = layers.Conv1D(128, 3, padding='same', activation='elu')(a)
        a = layers.Conv1D(128, 3, padding='same', activation='elu')(a)
        a = layers.BatchNormalization(1)(a)
        a = layers.Dropout(0.5)(a)
        a = layers.MaxPool1D()(a)  # 18
        a = layers.Conv1D(256, 3, padding='same', activation='elu')(a)
        a = layers.Conv1D(256, 3, padding='same', activation='elu')(a)
        a = layers.BatchNormalization(1)(a)
        a = layers.Dropout(0.5)(a)
        a = layers.MaxPool1D()(a)  # 18
        a = layers.Conv1D(512, 3, padding='same', activation='elu')(a)
        a = layers.Dropout(0.5)(a)
        a = layers.GlobalAveragePooling1D()(a)  # 128
        return a

    def _get_network(self):
        stats_a = layers.Input((35, 9))
        home_a = layers.Input((2,))
        stats_b = layers.Input((35, 9))
        home_b = layers.Input((2,))

        x = layers.Concatenate()([stats_a, stats_b])
        x = layers.Conv1D(8, 7, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        x = layers.Conv1D(16, 5, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        x = layers.Conv1D(32, 3, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.ReLU()(x)
        x = layers.GlobalMaxPool1D()(x)
        # x = layers.LSTM(256, return_sequences=True)(x)
        # x = layers.LSTM(256, return_sequences=False)(x)
        # a = self._get_conv_block(stats_a)
        # b = self._get_conv_block(stats_b)

        # x = tf.stack([a, b], 3)
        # x = layers.Concatenate(3)([a, b])
        # x = layers.Conv2D(64, 3, padding='same', activation='tanh')(x)
        # x = layers.Flatten()(x)
        # x = layers.LSTM(64, return_sequences=False)(x)

        # ha = layers.Concatenate()([home_a, a])
        # hb = layers.Concatenate()([home_b, b])

        x = layers.Concatenate()([x, home_a, home_b])
        x = layers.Dense(64, activation='elu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(64, activation='elu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(64, activation='elu')(x)
        x = layers.Dropout(0.5)(x)
        x = layers.Dense(2, activation='softmax')(x)

        return keras.Model([stats_a, home_a, stats_b, home_b], x)

    def call(self, inputs, training=None, mask=None):
        stats_a = inputs['stats_1']
        home_a = inputs['home_1']
        stats_b = inputs['stats_2']
        home_b = inputs['home_2']

        return self.model([stats_a, home_a, stats_b, home_b])


if __name__ == '__main__':
    model = MatchPredictorModel()
    dataset = GamesValidationDataset()

    model.model.summary()

    model.compile(optimizer='adam', loss='categorical_crossentropy')

    model.fit(dataset.batch(8))
