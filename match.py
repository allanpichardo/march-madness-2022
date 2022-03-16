import tensorflow as tf
import os
import pandas as pd
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


def interactive_session(model):
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
        interactive_session(model)


def get_team_name(id):
    con = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'db', 'ncaa.sqlite'))
    cursor = con.cursor()
    result = cursor.execute('select TeamName from Teams where TeamID = ?', (id,)).fetchone()
    return result[0]


def export_bracket(model, version):
    sample_path = os.path.join(os.path.dirname(__file__), 'data', 'mens-march-mania-2022', 'MDataFiles_Stage2',
                               'MSampleSubmissionStage2.csv')
    df = pd.read_csv(sample_path)
    plaintext = []

    print("Beginning Brackets:")
    for i, row in df.iterrows():
        id = row['ID']
        parts = id.split('_')
        team_a = parts[1]
        team_b = parts[2]

        name_a = get_team_name(team_a)
        name_b = get_team_name(team_b)
        print("Predicting {} vs {}".format(name_a, name_b))

        data = get_dataset(int(team_a), 0, int(team_b), 0)
        prediction = model(data)
        probability = prediction.numpy()[0]

        print("{} probability of win: {}".format(team_a, probability[1]))
        df.at[i, 'Pred'] = probability[1]
        plaintext.append("{} vs {} >> {} Probability for {} win".format(name_a, name_b, probability[1] if probability[1] > probability[0] else probability[0], name_a if probability[1] > probability[0] else name_b))

    print("Saving predictions")
    predictions_path = os.path.join(os.path.dirname(__file__), "allan_pichardo_predictions_2022-{}.csv".format(version))
    df.to_csv(predictions_path, index=False)

    plaintext_path = os.path.join(os.path.dirname(__file__), "predictions_2022-{}.txt".format(version))
    with open(plaintext_path, 'x') as f:
        for line in plaintext:
            f.write(line)
            f.write('\n')


if __name__ == '__main__':
    print("Match Simulator.")
    version = input("Select a model version number: ")
    print("Loading model...")
    model = load_model(version)
    print("Ready.")

    print("Select one of these options: ")
    print("1.  Interactive Session")
    print("2.  Export bracket")
    selection = input("> ")

    if int(selection) == 1:
        interactive_session(model)
    else:
        export_bracket(model, version)
