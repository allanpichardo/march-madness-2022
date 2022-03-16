import tensorflow as tf
import os
from models import MatchPredictorModel
import sqlite3


def get_dataset(id_a, home_a, id_b, home_b):
    con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db', 'ncaa.sqlite'))
    cursor = con.cursor()
    query = "select a.TeamID as TeamA, a.Stats as StatsA, b.TeamID as TeamB, b.Stats as StatsB from CondensedStats2022 a left join CondensedStats2022 b on b.TeamID = ? where a.TeamID = ?;"

    row = cursor.execute(query, (id_b, id_a)).fetchone()

    return {
        "home_1": tf.expand_dims(tf.one_hot(home_a, 2), 0),
        "home_2": tf.expand_dims(tf.one_hot(home_b, 2), 0),
        "stats_1": tf.expand_dims(tf.io.parse_tensor(row[1],
                                                     tf.float32), 0),
        "stats_2": tf.expand_dims(tf.io.parse_tensor(row[3],
                                                     tf.float32), 0)
    }


def load_model(version):
    model = tf.keras.models.load_model(os.path.join(os.path.dirname(__file__), 'saved_models', version))
    return model


def main(model):
    team_a = input("Enter ID for team A: ")
    home_a = input("Is team A playing at home? 1=yes, 0=no")
    team_b = input("Enter ID for team B: ")
    home_b = input("Is team B playing at home? 1=yes, 0=no")

    data = get_dataset(int(team_a), int(home_a), int(team_b), int(home_b))

    prediction = model(data)
    probability = prediction.numpy()[0]

    if probability[1] > probability[0]:
        print("Team A wins with probability {}".format(probability[1]))
    else:
        print("Team B wins with probability {}".format(probability[0]))

    continue_flag = input("Would you like to enter another? 1=yes, 0=no")
    if int(continue_flag) == 0:
        exit(0)
    else:
        main(model)


if __name__ == '__main__':
    print("Match Simulator.")
    version = input("Select a model version number: ")
    print("Loading model...")
    model = load_model(version)
    print("Ready.")
    main(model)
