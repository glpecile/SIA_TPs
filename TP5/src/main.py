import sys

import numpy as np

from algorithms.Autoencoder import Autoencoder
from algorithms.fonts import font_2
from utils.Config_A import Config_A
from utils.utils import to_bin_array, resize_letter
from utils import SeaGraphV2


def __main__():
    print('Argument List:', str(sys.argv))
    assert len(sys.argv) == 2, 'Missing arguments'
    f = open(sys.argv[1])
    config: Config_A = Config_A(f.read())
    f.close()
    data = []
    letters_patterns = []
    letters = ['@', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
               'U', 'V', 'W', 'X', 'Y', 'Z', '[', '\\', ']', '^', '_']
    for letter in font_2:
        aux = to_bin_array(letter)
        data.append(np.concatenate(aux))
        letters_patterns.append(aux)

    letters_dict = dict(zip(letters, letters_patterns))

    autoencoder = Autoencoder(config, len(data[0]), config.layers, config.latent_code_len)
    autoencoder.train(data, data)
    a = autoencoder.encode(data[0])
    b = autoencoder.decode(a)
    c = autoencoder.get_output(data[0])

    x = []
    y = []
    for key, value in letters_dict.items():
        res = autoencoder.encode(np.concatenate(value))
        x.append(res[0])
        y.append(res[1])
    SeaGraphV2.graph_points(x, y, list(letters_dict.keys()), title="Capa Latente")

    graphs = []
    for i, l in enumerate(letters):
        graphs.append(letters_dict[l])  # letra original
        res = autoencoder.get_output(np.concatenate(letters_dict['A']))
        res = np.array(res)
        res = np.array(list(map(resize_letter, [res])))
        graphs.append(res[0])
        if (i + 1) % 8 == 0:
            SeaGraphV2.graph_multi_heatmap(graphs, title='Letters', c_map="Greys", cols=4)
            graphs = []



if __name__ == "__main__":
    __main__()
