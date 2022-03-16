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
        a = layers.Conv1D(16, 7, padding='same', activation='relu')(inputs)
        a = layers.BatchNormalization()(a)
        a = layers.MaxPool1D()(a)  # 36
        a = layers.Conv1D(32, 5, padding='same', activation='relu')(a)
        a = layers.BatchNormalization()(a)
        a = layers.MaxPool1D()(a)  # 18
        a = layers.Conv1D(64, 3, padding='same', activation='relu')(a)
        a = layers.BatchNormalization()(a)
        a = layers.MaxPool1D()(a)  # 18
        a = layers.Conv1D(128, 3, padding='same', activation='relu')(a)
        a = layers.GlobalAveragePooling1D()(a)  # 128
        return a

    def _get_network(self):
        stats_a = layers.Input((36, 6))
        home_a = layers.Input(())
        stats_b = layers.Input((36, 6))
        home_b = layers.Input(())

        a = self._get_conv_block(stats_a)
        b = self._get_conv_block(stats_b)

        ha = layers.Add()([home_a, a])
        hb = layers.Add()([home_b, b])

        x = layers.Concatenate()([ha, hb])
        x = layers.Dense(512, activation='relu')(x)
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

    model.compile(optimizer='adam', loss='categorical_crossentropy')

    model.fit(dataset.batch(8))
