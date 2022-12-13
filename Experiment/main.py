import streamlit as st
import numpy as np
import pandas as pd
from prettytable import PrettyTable
import os
from report_game import ReportGame

if __name__ == "__main__":
    game = ReportGame(player_number=20)

    game_name = st.selectbox('Select the game to be played:', ['test', 'default', ])
    if game_name == 'test':
        game.load_game('./game_info/test.npy')
    elif game_name == 'default':
        game.load_game('./game_info/default.npy')

    #game.show_info()

    id = st.number_input('Insert your player ID', min_value=min(game.player_ID),\
                    max_value=max(game.player_ID), value=min(game.player_ID), step=1)
    check_id = st.checkbox('Please click: I confirm that this is my player ID and I will not change it.')
    pair = np.array(np.where(game.pairs[id] == 1))[0]
    pair_show = ' '.join([str(p) for p in pair])
    if check_id:
        st.subheader('Please submit your report at the bottom of the page, thank you!')
        st.subheader('Your groundtruth value is ' + str(game.R[id]))
        st.subheader('Compared with players ' + pair_show)
        report = {}
        report['game_name'] = game_name
        report['ID'] = id
        for i in pair:
            r = st.radio('Compare with player ' + str(i) + ' with groundtruth value ' + str(game.R[i]), ['My value is larger', 'My value is smaller'])
            report[i] = r

        report_save = st.button('Submit or upload my reports now!')
        if report_save:
            if not os.path.exists('./game_info/{}/'.format(game_name)):
                os.mkdir('./game_info/{}/'.format(game_name))
            np.save('./game_info/{}/{}_report_{}'.format(game_name, game_name, str(id)), report)
            st.text('Save!')

