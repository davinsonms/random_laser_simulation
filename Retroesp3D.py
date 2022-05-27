"""
Simulação de Monte Carlo para aplicações em Random Lasers em 3D

Possibilidade de simular dois livres caminhos médios para os fótons

Autor: Davinson Mariano da Silva
Data: 15/05/2022
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from Photon3D import *

# Determinar a região de contorno (unidades: micrometros)

xx = (-1000, 1000)
yy = (-1000, 1000)
zz = (-1000, 1000)

# Determinar a região da da sperfície sólido

solid_pos = 0

# varíavel que simula a concentração de íons

conc = 0.01


# Condições da Simulação

"""
Nesta simulação são considerados dois livres caminhos médios. Desta forma, é possível simular materiais 
nos quais as reflexões podem ocorrer via distâncias longas, como interfaces entre partículas e o ar e 
distâncias curtas, como reflexões internas às partículas.
"""

n_fotons = 50                     # número de fótons incidentes
n_iteracoes = 100000                 # número de interações (reflexões) máximo
fmp_1 = 10                           # livre caminho médio 1 (um)
fmp_2 = np.linspace(0, 10, 20)     # livre caminho médio 2 (um)
prob = 0.99                          # probabilidade de ocorrência do livre caminho médio 2


# Inicialização das Arrays

primary_photons = np.array([Photon3D((xx[1]-xx[0]) / 2, (yy[1] - yy[0]) / 2, solid_pos) for i in range(n_fotons)])
secondary_photons = [[] for i in range(len(fmp_2))]
emitted_photons = [[] for i in range(len(fmp_2))]
t_res = [[] for i in range(len(fmp_2))]
t_res_mean =[]
t_res_std = []
bsc = []

# Loop da simulação

for n, f in enumerate(fmp_2):
    for p in primary_photons:
        p.Propagate(f, -np.pi, 0)
        for i in range(n_iteracoes):
            p.PropagRandomLevy(fmp_1, f, prob)
            r = np.random.uniform(0,1)
            if r < conc and p.isInside == True:
                secondary_photons[n].append(Photon3D(p.x, p.y, p.z))
                break
            if p.z > solid_pos:
                break

    for s in secondary_photons[n]:
        for i in range(n_iteracoes):
            s.PropagRandomLevy(fmp_1, f, prob)
            if s.z > solid_pos:
                emitted_photons[n].append(s)
                t_res[n].append(s.ResidenceTime(2))
                break

    bsc.append(len(emitted_photons[n])/len(secondary_photons[n]))
    t_res_mean.append(np.mean(t_res[n]))
    t_res_std.append(np.std(t_res[n]))
    primary_photons = np.array([Photon3D((xx[1]-xx[0]) / 2, (yy[1] - yy[0]) / 2, solid_pos) for i in range(n_fotons)])

    print(100*n/len(fmp_2))    # Imprime a porcentagem para a finalização da execução da simulação

# Plotagens

# Plotagem espacial para partículas

fig, ax = plt.subplots(1, 2)

for i in range(len(emitted_photons)):

    ax[0].plot(emitted_photons[i][-1].x_history, emitted_photons[i][-1].z_history)
    ax[1].plot(emitted_photons[i][-1].y_history, emitted_photons[i][-1].z_history)

    ax[0].set_xlabel('x')
    ax[1].set_xlabel('y')
    ax[0].set_ylabel('z')
    ax[1].set_ylabel('z')

plt.show()

# Plotagem para:
# 1) o histograma de tempo de residência dos fótons
# 2) a propabilidade de emissão de fótons espontâneos em função do número de fótons gerados no interior do material
# 3) tempo de residência médio em função do parâmetro simulado (geralmente é o livre caminho médio)

fig, ax = plt.subplots(1, 3)

ax[0].hist(t_res[-1], 10, log=True)
ax[1].plot(fmp_2, bsc, 'bo')
ax[2].plot(fmp_2, t_res_mean, 'bo')

ax[0].set_xlabel('tempo de residência(ps)')
ax[0].set_ylabel('N fótons')

ax[1].set_xlabel('fmp2 (um)')
ax[1].set_ylabel('Ns/N0')

ax[2].set_xlabel('fmp2 (um)')
ax[2].set_ylabel('tempo de residência (ps)')

plt.subplots_adjust(left=0.1,
                    bottom=0.1,
                    right=0.9,
                    top=0.9,
                    wspace=0.6,
                    hspace=0.6)
plt.show()


# Salva os arquivos com os dados e para o relatório

resultados = np.array([fmp_2, bsc, t_res_mean])
arquivo = pd.DataFrame(resultados.T, columns=['p(lt_1)/p(lt_2)', 'N fótons emitidos/N fótons gerados',
                                              'tempo de residência médio (ps)'])
arquivo.to_csv("resultados.csv")


# Salva arquivo com as condições da simulação

f = open('parametros.txt', 'w')
f.write('Condições da Simulação: \r')
f.write('número de fótons incidentes: %d \r' %n_fotons)
f.write('número máximo de reflexões: %d \r' %n_iteracoes)
f.write('livre caminho médio 1 (um): %f \r' %fmp_1)
f.write('livre caminho médio 2 inicial (um): %f \r' %fmp_2[0])
f.write('livre caminho médio 2 final (um): %f \r' %fmp_2[-1])
f.write('livre caminho médio 2 passo (um): %f \r' %(fmp_2[1]-fmp_2[0]))
f.write('probabilidade de reflexões devido ao livre caminho médio 2 (um): %f \r' %prob)
f.close()
