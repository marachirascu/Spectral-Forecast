import numpy as np
from glob import glob
import matplotlib.pyplot as plt

class SpectralForecast:
    def __init__(self, d=100):
        self.A_mats = []
        self.B_mats = []
        self.P_mats = []
        self.M_states = []
        self.d = d
        self.S_all = []

        self.read_input_data()
        self.create_matrices()
        self.generate_M_states()
        self.test_P_matrices()
        self.print_results()
    
    def read_input_data(self):  # reads the input in the A, B, P folders
        for path in glob('input/A/*'):
            with open(path, 'r') as f:
                self.A_mats.append([list(map(float, line.split(' '))) for line in f.read().split('\n')[:-1]])

        for path in glob('input/B/*'):
            with open(path, 'r') as f:
                self.B_mats.append([list(map(float, line.split(' '))) for line in f.read().split('\n')[:-1]])

        for path in glob('input/P/*'):
            with open(path, 'r') as f:
                self.P_mats.append([list(map(float, line.split(' '))) for line in f.read().split('\n')[:-1]])

    
    def create_matrices(self):  # creates the A and B average matrices
        self.A = sum(list(map(np.array, self.A_mats))) / float(len(self.A_mats))
        self.B = sum(list(map(np.array, self.B_mats))) / float(len(self.B_mats))


    def generate_M_states(self):    # calculates the prediction matrix M
        max_A = self.A.max()
        max_B = self.B.max()

        element_gen = lambda a,b,d: (float(d) / max_A) * a + (float((self.d - d)) / max_B) * b

        for d in range(self.d):
            Md = np.zeros_like(self.A)
            for i in range(len(self.A)):
                for j in range(len(self.A[i])):
                    Md[i][j] = element_gen(self.A[i][j], self.B[i][j], d)

            self.M_states.append(Md)


    def test_P_matrices(self):  # calculates the similarity indices S(d)

        for P in self.P_mats:
            S = []
            for d in range(self.d):
                MP = np.sum(np.multiply(self.M_states[d], P))
                MM = np.sum(np.multiply(self.M_states[d], self.M_states[d]))
                PP = np.sum(np.multiply(P, P))

                S.append((MP ** 2) / (MM * PP))

            self.S_all.append(S)

    def print_results(self):    # prints the indices and plots data for 10 patients
        for S in self.S_all:
              print('Patient ', self.S_all.index(S), ': ', S)
        
        fig, axs = plt.subplots(2, 5, sharey=True)
        fig.suptitle('Spectral Forecast')
        
        z = 0
        for i in range(2):
            for j in range(5):
                axs[i, j].plot(self.S_all[z])
                z += 1
            

        z = 0
        for ax in axs.flat:
            ax.set(xlabel='distance', ylabel='Similarity index', title='Patient '+str(z))
            ax.set_xticks(np.arange(0, self.d + 1, self.d / 10))
            if z < 10:
                ymax = max(self.S_all[z])
                ymin = min(self.S_all[z])
                xpos = self.S_all[z].index(ymax)
                ytextpos = ymax - (ymax - ymin) / 2
                ax.annotate('Maximum similarity\nvalue: '+str(ymax)+'\ndistance: '+str(xpos), xy=(xpos, ymax), xytext=(xpos - 10, ytextpos), arrowprops=dict(arrowstyle='->'))
                z += 1
                ax.label_outer()

        plt.show()
    
SpectralForecast()
