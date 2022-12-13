import streamlit as st
import numpy as np
import pandas as pd
from prettytable import PrettyTable
import os

class ReportGame():

    def __init__(self, player_number=None):
        self.game_info = {}
        if not (player_number is None):
            self.player_number = player_number
            self.game_info['player_number'] = player_number
            self.player_ID = [i for i in range(0, self.player_number, 1)]
            self.game_info['player_ID'] = self.player_ID

    def load_game(self, game_path='./game_info/default.npy'):
        self.game_info = np.load(game_path, allow_pickle=True).item()
        self.player_number = self.game_info['player_number']
        self.player_ID = self.game_info['player_ID']
        self.R = self.game_info['R']
        self.noise = self.game_info['noise']
        self.observed_Y = self.game_info['observed_Y']
        self.pairs = self.game_info['pairs']
        print('Game Load:', game_path)

    def uniform_R(self, min=1, max=100, step=1):
        self.R = np.random.randint(low=min, high=max + 1, size=self.player_number)
        self.game_info['R'] = self.R
        return self.R

    def gaussian_noise(self, sigma=10):
        self.noise = np.random.normal(loc=0, scale=sigma, size=self.player_number)
        self.noise = np.round(self.noise, 1)
        self.game_info['noise'] = self.noise
        return self.noise

    def update_Y(self):
        self.observed_Y = self.game_info['R'] + self.game_info['noise']
        self.observed_Y = np.round(self.observed_Y, 1)
        self.game_info['observed_Y'] = self.observed_Y
        return self.observed_Y

    def fully_connected_pairs(self):
        self.pairs = np.ones((self.player_number, self.player_number))
        for i in range(self.player_number):
            self.pairs[i][i] = 0
        self.game_info['pairs'] = self.pairs
        return self.pairs

    def show_info(self):
        tab = PrettyTable()
        tab.add_column('Player ID:', self.game_info['player_ID'])
        tab.add_column('Groundtruth R:', self.game_info['R'])
        tab.add_column('Observed Y:', self.game_info['observed_Y'])
        show_pairs = []
        for i in range(self.game_info['player_number']):
            show_pair = ''
            for j in range(self.game_info['player_number']):
                if self.game_info['pairs'][i][j]:
                    show_pair += str(j) + ' '
            show_pairs.append(show_pair)
        tab.add_column('Compare:', show_pairs)
        print(tab)

    def save_game(self, name='./game_info/default.npy'):
        np.save(name, self.game_info)

def default_game():
    _game = ReportGame(player_number=20)
    _game.uniform_R()
    _game.gaussian_noise()
    _game.update_Y()
    _game.fully_connected_pairs()
    _game.save_game()
    _game.show_info()
    return _game

if __name__ == "__main__":
    default_game()
