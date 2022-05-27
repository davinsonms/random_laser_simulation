"""
Simulação de Monte Carlo para aplicações em Random Lasers em 3D

Possibilidade de simular dois livres caminhos médios para os fótons

OBS: Este arquivo contém as rotinas para as simulações de Monte Carlo

Autor: Davinson Mariano da Silva
Data: 15/05/2022
"""


import numpy as np

class Photon3D:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.isInside = False
        self.x_history = [self.x]
        self.y_history = [self.y]
        self.z_history = [self.z]

    def PropagRandom(self, free_mean_path):
        self.free_mean_path = np.random.normal(free_mean_path, free_mean_path)
        phi = np.random.uniform(0, 2 * np.pi)
        theta = np.random.uniform(0, 2 * np.pi)
        self.x = self.x + np.sin(phi) * np.cos(theta) * free_mean_path
        self.y = self.y + np.sin(phi) * np.sin(theta) * free_mean_path
        self.z = self.z + np.cos(phi) * free_mean_path
        self.x_history.append(self.x)
        self.y_history.append(self.y)
        self.z_history.append(self.z)

    def PropagRandomLevy(self, fmp1, fmp2, p):
        self.fmp1 = np.random.normal(fmp1, fmp1)
        self.fmp2 = np.random.normal(fmp2, fmp2)
        self.p = p          # probabilidade de ocorrer espalhamento com menor livre caminho
        phi = np.random.uniform(0, 2 * np.pi)
        theta = np.random.uniform(0, 2 * np.pi)
        free_mean_path = np.random.choice([self.fmp1, self.fmp2], p = [1-self.p, self.p])
        if free_mean_path == self.fmp2 and self.isInside == False:
            self.isInside = True
        elif free_mean_path == self.fmp1 and self.isInside == True:
            self.isInside = False
        self.x = self.x + np.sin(phi) * np.cos(theta) * free_mean_path
        self.y = self.y + np.sin(phi) * np.sin(theta) * free_mean_path
        self.z = self.z + np.cos(phi) * free_mean_path
        self.x_history.append(self.x)
        self.y_history.append(self.y)
        self.z_history.append(self.z)

    def Propagate(self, phi, theta, free_mean_path):
        self.free_mean_path = np.random.normal(free_mean_path, free_mean_path)
        self.x = self.x + np.sin(phi) * np.cos(theta) * free_mean_path
        self.y = self.y + np.sin(phi) * np.sin(theta) * free_mean_path
        self.z = self.z + np.cos(phi) * free_mean_path
        self.x_history.append(self.x)
        self.y_history.append(self.y)
        self.z_history.append(self.z)

    def DeleteLastPos(self):
        self.x_history.pop()
        self.y_history.pop()
        self.z_history.pop()

    def Total_Path(self):
        total = 0
        for i in range(len(self.x_history)-1):
            dx = self.x_history[i+1]-self.x_history[i]
            dy = self.y_history[i+1]-self.y_history[i]
            dz = self.z_history[i+1]-self.z_history[i]
            total += np.sqrt(dx**2 + dy**2 + dz**2)
        return total

    def ResidenceTime(self, n):
        c = 300  # velocidade da luz em µm/fs
        return self.Total_Path()*n/c

    def n_Reflexions(self):
        return len(self.x_history)



