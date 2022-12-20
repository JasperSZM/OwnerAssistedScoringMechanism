import streamlit as st
import numpy as np
import pandas as pd
from prettytable import PrettyTable
import os
from report_game import ReportGame

def collect_report(game_name, game):
    report_path = './game_info/{}/'.format(game_name)

    all_reports = {}
    for file in os.listdir(report_path):
        r = np.load(report_path + file, allow_pickle=True)
        id = file[12:]
        id = id[:-4]
        id = int(id)
        all_reports[id] = r.item()

    report_matrix = np.zeros(shape=(game.player_number, game.player_number))
    for id in all_reports.keys():
        for to_id in all_reports[id].keys():
            try:
                to_id = int(to_id)
            except:
                pass
            if isinstance(to_id, int):
                report_matrix[id][to_id] = 1.0 if 'My value is larger' == all_reports[id][to_id] else -1.0

    return report_matrix


if __name__ == "__main__":
    game_name = 'test'
    game = ReportGame(player_number=20)
    if game_name == 'test':
        game.load_game('./game_info/test.npy')
    elif game_name == 'default':
        game.load_game('./game_info/default.npy')

    game.show_info()

    report_matrix = collect_report(game_name, game)
    print(report_matrix)

