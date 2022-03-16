import os
from abc import ABC

import tensorflow as tf
import numpy as np
import pandas as pd
import sqlite3


class GamesDatasetBuilder:

    def __init__(self,
                 database_path=os.path.join(os.path.dirname(__file__), 'db', 'ncaa.sqlite'),
                 dataset_path=os.path.join(os.path.dirname(__file__), 'dataset'),
                 start_season=2003, end_season=2021
                 ) -> None:
        super().__init__()

        self._database_path = database_path
        self._dataset_path = dataset_path
        self._start_season = start_season
        self._end_season = end_season

        self._connection = sqlite3.connect(self._database_path)
        self._cursor = self._connection.cursor()

    def condense_stats(self):
        print("Generating dataset...")
        self._load_raw_data()

    def _bytes_feature(self, value):
        """Returns a bytes_list from a string / byte."""
        if isinstance(value, type(tf.constant(0))):
            value = value.numpy()  # BytesList won't unpack a string from an EagerTensor.
        return tf.train.Feature(bytes_list=tf.train.BytesList(value=[value]))

    def _float_feature(self, value):
        """Returns a float_list from a float / double."""
        return tf.train.Feature(float_list=tf.train.FloatList(value=[value]))

    def _int64_feature(self, value):
        """Returns an int64_list from a bool / enum / int / uint."""
        return tf.train.Feature(int64_list=tf.train.Int64List(value=[value]))

    def _load_raw_data(self):
        print("Loading database.")

        max_games = self._cursor.execute(
            'select count(TeamID) as c from SeasonStats group by TeamID, Season order by c desc limit 1').fetchone()[0]

        all_stats = []

        print("Iterating through team stats")
        for row in self._cursor.execute('select * from Teams order by TeamID').fetchall():
            id = row[0]
            name = row[1]
            first_season = row[2]
            last_season = 2021

            print("Processing stats for {}".format(name))
            for season in range(first_season, last_season + 1):
                print("Season {}".format(season))
                team_stats = np.array(self._get_stats(id, season))

                if len(team_stats.shape) == 1:
                    print("No games found. Skipping.")
                    continue

                matrix = team_stats[:, 5:-2]
                matrix = np.resize(matrix, (max_games, matrix.shape[1]))
                matrix = tf.convert_to_tensor(matrix, dtype=tf.float32)
                matrix = tf.io.serialize_tensor(matrix)

                all_stats.append((team_stats[0][0], team_stats[0][1], matrix.numpy()))

        print("Got all stats.")
        print("Bulk inserting...")
        self._cursor.executemany("insert into CondensedStats values (?, ?, ?)", all_stats)
        self._connection.commit()
        print("Finished!")


    def _get_stats(self, team_id, season):
        return self._cursor.execute("select * from SeasonStats where TeamID = ? and Season = ?",
                                    (team_id, season)).fetchall()


class GamesTrainingDataset(tf.data.Dataset, ABC):

    @staticmethod
    def get_db_path():
        return os.path.join(os.path.dirname(__file__), 'db', 'ncaa.sqlite')

    @staticmethod
    def get_sql_query():
        return "select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, g.OpponentID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB, g.Outcome from SeasonStats g left join CondensedStats ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season < 2020 order by ca.Season asc"

    def __new__(cls, *args, **kwargs):
        return tf.data.experimental.SqlDataset(
            'sqlite',
            GamesTrainingDataset.get_db_path(),
            GamesTrainingDataset.get_sql_query(),
            (tf.int32, tf.int32, tf.string, tf.int32, tf.int32, tf.string, tf.int32, tf.int32)
        ).map(lambda season, teamA, statsA, homeA, teamB, statsB, homeB, outcome: ({
            "stats_1": tf.io.parse_tensor(statsA, tf.float32),
            "home_1": homeA,
            "stats_2": tf.io.parse_tensor(statsB, tf.float32),
            "home_2": homeB
        }, tf.one_hot(outcome, 2)) ,tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)

class GamesValidationDataset(tf.data.Dataset, ABC):

    @staticmethod
    def get_db_path():
        return os.path.join(os.path.dirname(__file__), 'db', 'ncaa.sqlite')

    @staticmethod
    def get_sql_query():
        return "select g.Season, g.TeamID as TeamA, ca.Stats as StatsA, g.Home as HomeA, g.OpponentID as TeamB, cb.Stats as StatsB, (select Home from SeasonStats where TeamID = cb.TeamID) as HomeB, g.Outcome from SeasonStats g left join CondensedStats ca on ca.TeamID = g.TeamID and ca.Season = g.Season left join CondensedStats cb on cb.TeamID = g.OpponentID and cb.Season = g.Season where ca.Season >= 2020 order by ca.Season asc"

    def __new__(cls, *args, **kwargs):
        return tf.data.experimental.SqlDataset(
            'sqlite',
            GamesValidationDataset.get_db_path(),
            GamesValidationDataset.get_sql_query(),
            (tf.int32, tf.int32, tf.string, tf.int32, tf.int32, tf.string, tf.int32, tf.int32)
        ).map(lambda season, teamA, statsA, homeA, teamB, statsB, homeB, outcome: ({
            "stats_1": tf.io.parse_tensor(statsA, tf.float32),
            "home_1": homeA,
            "stats_2": tf.io.parse_tensor(statsB, tf.float32),
            "home_2": homeB
        }, tf.one_hot(outcome, 2)) ,tf.data.AUTOTUNE).prefetch(tf.data.AUTOTUNE)


if __name__ == '__main__':
    # builder = GamesDatasetBuilder()
    # builder.condense_stats()

    data = GamesTrainingDataset()

    for sample in data:
        print(sample)
