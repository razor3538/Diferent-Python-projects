import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

def f_1(x, p, e):
	h = p / (1 + e * np.cos(x)) - 6371000

	a0 = -19.023
	h0 = 104000
	O = 0.01594

	ro = np.exp(a0 - O * np.sqrt(h - h0))

	return(ro)

def f1(x, p, e):
	ro = f_1(x, p, e)

	return(ro * np.sqrt(1 + e * e + 2 * e * np.cos(x)) / pow(1 + e * np.cos(x), 2))

def f2(x, p, e):
	ro = f_1(x, p, e)

	return(ro * np.sqrt(1 + e * e + 2 * e * np.cos(x)) * (e + np.cos(x)) / pow(1 + e * np.cos(x), 2))

def f3(x, p, e):
	ro = f_1(x, p, e)

	return(ro * np.sqrt(1 + e * e + 2 * e * np.cos(x)) * np.sin(x) / pow(1 + e * np.cos(x), 2))






Cxa, m, Sa, U, Om, ha, hp, i, MM = 3.5, 1200, 12, 10, 40, 640000, 250000, 32.4, 398600445000000

A, B, h, WW, N = 0, 6.2831, 0.001, 0, 1

ra = ha + 6371000
rp = hp + 6371000

SSk = Sa * Cxa / (2 * m)

w = U

a = (ra + rp) / 2

e = (ra - rp) / (ra + rp)

p = a * (1 - e * e)

T = 2 * np.pi * pow(a, 1.5) / np.sqrt(MM)


BaseData = "Начальные данные: a = {} e = {} p = {} rp = {} ra = {} T = {}"
print(BaseData.format(a / 1000, e, p / 1000, rp / 1000, ra / 1000, T))

mass = {}
while (N <= 50):
	print('\n\n' + str(N) + '\n')

	n = int((B - A) / h)

	Integral1 = h * (f1(A, p, e) + f1(B, p, e)) / 6

	for i in range(1, n + 1):
		Integral1 += 4 / 6 * h * f1(A + h * (i  - 0.5), p, e)
	for i in range(1, n):
		Integral1 += 2 / 6 * h * f1(A + h * i, p, e)

	dp = -2 * pow(p, 2) * SSk * Integral1

	Integral2 = h * (f2(A, p, e) + f2(B, p, e)) / 6

	for i in range(1, n + 1):
		Integral2 += 4 / 6 * h * f2(A + h * (i  - 0.5), p, e)
	for i in range(1, n):
		Integral2 += 2 / 6 * h * f2(A + h * i, p, e)

	de = -2 * p * SSk * Integral2

	Integral3 = h * (f3(A, p, e) + f3(B, p, e)) / 6

	for i in range(1, n + 1):
		Integral3 += 4 / 6 * h * f3(A + h * (i  - 0.5), p, e)
	for i in range(1, n):
		Integral3 += 2 / 6 * h * f3(A + h * i, p, e)

	dw = -2 * p * SSk * Integral3 / e
	da = p * (dp / p + 2 * e * de / (1 - e * e)) / (1 - e* e)

	a += da
	tmp = "Изменение апоцентного параметра: за виток: {} стало: {}"
	print(tmp.format(da / 1000, a / 1000))

	dT = 3 * np.pi * da * np.sqrt(a / MM)

	T += dT
	tmp = "Изменение периода: за виток: {} стало: {} "
	print(tmp.format(dT, T))

	dhp = p * (dp / p - de / (1 + e)) / (1 + e)
	
	rp += dhp
	tmp = "Изменение высоты перицентра: за виток: {} стало: {}"
	print(tmp.format(dhp / 1000, rp / 1000))

	dha = p * (dp / p + de / (1 + e)) / (1 - e)
	
	ra += dha	
	tmp = "Изменение высоты апоцентра: за виток: {} стало: {}"
	print(tmp.format(dha / 1000, ra / 1000))

	p += dp
	tmp = "Изменение фокального параметра: за виток: {} стало: {}"
	print(tmp.format(dp / 1000, p / 1000))

	e += de
	tmp = "Изменение эксцентриситета: за виток: {} стало: {}"
	print(tmp.format(de, e))

	w += dw
	tmp = "Изменение угла парицентра: за виток: {} стало: {}"
	print(tmp.format(dw, w))

	mass[N] = dict(a = a, T = T, rp = rp, ra = ra, p = p, e = e, w = w)
	exel = pd.DataFrame(mass)
	N += 1

writer = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')

	  
exel.to_excel(writer, 'Sheet1')


writer.save()