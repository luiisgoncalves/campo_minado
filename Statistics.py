from collections import Counter
import numpy as np
import pandas as pd


class Statistics:
    def __init__(self):
        self.log = self.read_log()

    def victory(self) -> None:
        """verifica e mostra quais jogadores foram mais vitoriosos em cada nivel de dificuldade"""
        if self.verify_log():
            try:
                print('\nJOGADORES QUE MAIS VENCERAM POR DIFICULDADE:')
                for i in range(1, 10):
                    mat, maximo = self.max_min(i)[0]
                    self.print_victory_loss(mat, 'vitoria', maximo, i)

            except IndexError:
                pass
        else:
            self.message()

    def loss(self) -> None:
        """verifica e mostra quais jogadores foram mais derrotados em cada nivel de dificuldade"""
        if self.verify_log():
            try:
                print('\nJOGADORES QUE MAIS PERDERAM POR DIFICULDADE:')
                for i in range(1, 10):
                    mat, minimo = self.max_min(i)[1]
                    self.print_victory_loss(mat, 'derrota', minimo, i)

            except IndexError:
                pass
        else:
            self.message()

    def razao(self) -> None:
        """verifica e mostra a razao entre vitorias e total de partidas de cada jogador
        (apenas sao contabilizadas partidas terminadas com vitoria ou derrota)"""
        if self.verify_log():
            players = np.array(self.log.query(f'win==1 | lose == 1').player)
            dic_players = Counter(players)

            winners = np.array(self.log.query(f'win==1').player)
            dic_winners = Counter(winners)

            print('\nPORCENTAGEM DE VITORIAS:')
            for player in dic_players:
                razao = round(dic_winners[player] / dic_players[player] * 100, 2)
                print(f'Com total de {dic_players[player]} partidas, o(a) {player} vence em {razao}% das vezes')
        else:
            self.message()

    def time_sum(self) -> None:
        """mostra a quantidade de tempo (em segundos) que cada jogador passou jogando
        (apenas sao contabilizadas partidas terminadas com vitoria ou derrota)"""
        games = self.log.query('win == 1 | lose == 1').groupby('player').sum()
        games['total_time'] = games.win + games.lose
        games.drop(games.columns.drop(['time', 'total_time']), axis=1, inplace=True)
        games['mean_time'] = games.time / games.total_time
        print('\nTEMPO TOTAL DE JOGO DE CADA PLAYER (em segundos):')
        for player in games.time.index:
            media = int(games.mean_time[player])
            print(f'{player} passou {round(games.time[player])} segundos em partidas com média de {media} segundos por partida')

    def max_min(self, dificuldade) -> tuple[tuple[np.ndarray, int], tuple[np.ndarray, int]]:
        """retorna os jogadores, e suas respectivas quantidades, que mais venceram e os que mais perderam"""
        victory = np.array(self.filter_df(dificuldade))          # pega todos os players que jogaram na dificuldade dada e venceram
        loss = np.array(self.filter_df(dificuldade, win=False))  # pega todos os players que jogaram na dificuldade dada e perderam

        mat_victorious = np.array(list(Counter(victory).items()))  # matriz contendo o nome de cada jogador e quantas vezes venceu
        mat_loss = np.array(list(Counter(loss).items()))           # matriz contendo o nome de cada jogador e quantas vezes perdeu

        max_win = np.max(mat_victorious[:, 1].astype(int))  # pega o maior numero de vitorias
        max_loss = np.min(mat_loss[:, 1].astype(int))        # pega o maior numero de derrotas

        return (mat_victorious, max_win), (mat_loss, max_loss)

    def filter_df(self, difficulty: int, win=True) -> pd.Series:
        """retorna uma Series do arquivo de log filtrado por pela dificuldade passada como parametro"""
        if win:
            filters = self.log.query(f'difficulty==0.{difficulty} & win==1').player
        else:
            filters = self.log.query(f'difficulty==0.{difficulty} & lose==1').player
        return filters

    def verify_log(self) -> bool:
        """doc"""
        return True if len(self.log) > 0 else False

    @staticmethod
    def print_victory_loss(mat: np.ndarray, action: str, limit: int, difficulty: int) -> None:
        """mostra ao usuario o(s) jogador(es) que mais venceram na dificuldade passada"""
        players = ''
        for player in mat[:, 0][mat[:, 1].astype(int) == limit]:
            players += player + ', '
        print(f'Com {limit} {action}(s) na dificuldade 0.{difficulty} foi: {players[:-2]}')

    @staticmethod
    def read_log() -> pd.DataFrame:
        """responsavel por ler o arquivo de log.csv e transforma-lo em um DataFrame"""
        df = pd.read_csv('log.csv', index_col=0)
        df.index = pd.to_datetime(df.index)
        return df

    @staticmethod
    def message() -> None:
        """chamado quando o arquivo de log ainda esta vazio"""
        print('\nImpossível gerar estatísticas. Log ainda está vazio, jogue pelo menos uma partida para preenche-lo')


if __name__ == '__main__':
    Statistics().razao()
