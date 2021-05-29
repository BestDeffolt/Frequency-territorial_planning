from tkinter import *
from tkinter import scrolledtext
import numpy as np
import scipy.integrate as integrate
from math import inf

window = Tk()
window.title("Приложение для частотно – территориальное планирование сетей подвижной связи")
window.geometry('980x560')

def f(x):
    return np.exp(-x ** 2 / 2)


def clicked():
    lbl1 = Label(window, text="      Определение размера кластера      ")
    lbl1.grid(column=0, row=1)
    txt = scrolledtext.ScrolledText(window, width=102, height=10)
    txt.grid(column=0, row=0)
    txt2 = scrolledtext.ScrolledText(window, width=102, height=10)
    txt2.grid(column=0, row=2)
    txt3 = scrolledtext.ScrolledText(window, width=102, height=10)
    txt3.grid(column=0, row=4)
    N = int(enter1.get())  # int(input("Введите свой вариант: "))
    mn = int(enter2.get())  # int(input("Введите две последние цифра студака: "))
    K = int(enter3.get())  # int(input("Введите размер кластера: "))
    M = int(enter4.get())  # int(input("Введите размер секторов (3 или 6): "))
    Nn = 50
    S = 300 + 40 * N  # Площадь зоны обслуживания
    Na = 25000 + 3000 * N  # Планируемое число абонентов сети
    Betta_ab = 0.022 + 0.0005 * N  # Активность абонента в ЧНН
    Pv = 0.02 - 0.0005 * N  # Допустимая вероятность блокировки вызова
    if (N % 2 == 0):
        Nc = 2
    else:
        Nc = 1
    sigma = 4 + 0.6 * N  # Отклонение величины уровня сигнала в месте приема
    ci = 9  # Требуемое отношение сигнал/шум
    pK = 8 + 0.25 * N  # Допустимая вероятность невыполнения требований по отношению сигнал/шум.
    LTE_min = 2540
    LTE_max = 2850
    q = np.sqrt(3*K)
    txt = scrolledtext.ScrolledText(window, width=100, height=10)
    txt.grid(column=0, row=0)
    txt.insert(INSERT, f"Ослабление мешающих сигналов: {q}")
    # print(f"Ослабление мешающих сигналов: {q}")
    if (M == 3):
        j = 2
        Betta_1 = round((q+0.7)**-4, 3)
        Betta_2 = round(q**-4)
        txt.insert(INSERT, f"\nКоличество секторов: M = {M} => j = {j}; B1 = {Betta_1}; B2 = {Betta_2}")
        # print(f"Количество секторов: M = {M} => j = {j}; B1 = {Betta_1}; B2 = {Betta_2}")
    elif (M == 6):
        j = 1
        Betta_1 = round((q+1)**-4, 3)
        txt.insert(INSERT, f"\nКоличество секторов: M = {M} => j = {j}; B1 = {Betta_1}")
        # print(f"Количество секторов: M = {M} => j = {j}; B1 = {Betta_1}")
    else:
        raise("Неверно указано кол-во кластеров")
    signa_e = np.round(1/0.053 * np.log(1+(np.exp(0.053*sigma**2)-1)*Betta_1**2 / Betta_1 ** 2), 2)
    txt.insert(INSERT, f"\nОтклонение величины уровня суммарной помехи по основному каналу приема: {signa_e}")
    # print(f"Отклонение величины уровня суммарной помехи по основному каналу приема: {signa_e}")
    Betta = Betta_1 * np.exp(0.053 * (sigma**2 - signa_e)/2)
    txt.insert(INSERT, f"\nОтносительный уровень суммарной помехи по основному каналу приема: {Betta}")
    # print(f"Относительный уровень суммарной помехи по основному каналу приема: {Betta}")
    x_1 = (10 * np.log10(1/Betta) - ci) / np.sqrt(sigma**2 + signa_e)
    # print({np.round(x_1, 3)})
    integr, err = integrate.quad(f, x_1, inf)
    pk = np.round(1 / np.sqrt(2*np.pi) * integr * 100, 2)
    txt.insert(INSERT, f"\nВероятность невыполнения требований по отношению C/I: {pk}%")
    txt.insert(INSERT, f"\nПроверим условие p_d(K) <= p(K) < 2%")
    # print(f"Вероятность невыполнения требований по отношению C/I: {pk, 2}%")
    # print(f"Проверим условие p_d(K) <= p(K) < 2%")
    if(pK <= pk or pk > 2):
        txt.insert(INSERT, f"\n{pK}% <= {pk}% < 2%")
        txt.insert(INSERT, "\nКластер подобран правильно")
        # print(f"{pK}% <= {pk}% < 2%")
        # print("Кластер подобран правильно")
    else:
        txt.insert(INSERT, "\nКластер подобран неправильно")
        txt.insert(INSERT, f"\n{pK}% <= {pk}% < 2%")
        raise("Кластер подобран неверно!!!")
    lbl1 = Label(window, text="Расчет общего числа частотных каналов, выделяемых для развертывания сети")
    lbl1.grid(column=0, row=3)
    nk = M*K*Nc
    txt2.insert(INSERT, f"Общее число частотных каналов, выделяемых для развертывания сети: {nk}")
    fk = 10
    delta_F = nk * fk
    txt2.insert(INSERT, f"\nМинимальная полоса частот необходимая для развертывания сети: {delta_F}Гц")
    na = 1
    Ns = na * Nc
    txt2.insert(INSERT, f"\nОбщее число разговорных каналов в одном секторе: {Ns}")
    A = np.round(Nn * 1 - np.sqrt(1-(Pv * np.sqrt((Nn * np.pi) / 2))**(1/Nn)) - 9.235, 3)
    txt2.insert(INSERT, f"\nТелефонная нагрузка: {A}")
    N_ab = int(A / Betta_ab * M)
    txt2.insert(INSERT, f"\nРасчет количества абонентов в одной ячейке: {N_ab}")
    Na1 = 30165
    Na2 = 3150
    Na3 = 1049
    N_bc_1 = np.round(Na1 / N_ab)
    N_bc_2 = np.round(Na2 / N_ab + 0.5)
    N_bc_3 = np.round(Na3 / N_ab + 0.5)
    txt2.insert(INSERT, f"\nРасчет общего числа базовых станций: [{int(N_bc_1)}, {int(N_bc_2)}, {int(N_bc_3)}]")
    S1 = 16
    S2 = 25
    S3 = 30
    Rc1 = np.round(np.sqrt(2 / (3 * np.sqrt(3)) * S1 / N_bc_1), 3)
    Rc2 = np.round(np.sqrt(2 / (3 * np.sqrt(3)) * S2 / N_bc_2), 3)
    Rc3 = np.round(np.sqrt(2 / (3 * np.sqrt(3)) * S3 / N_bc_3), 3)
    txt2.insert(INSERT, f"\nРасчет радиуса зоны покрытия одной базовой станции: [{Rc1}, {Rc2}, {Rc3}]")
    lbl2 = Label(window, text="Оценка энергетического бюджета линий")
    lbl2.grid(column=0, row=5)
    Lb = 7.00 + 0.02 * mn
    Wa = 2.50 + 0.01 * mn
    Ci = 2.72
    Z = np.round(Lb + Wa + Ci, 2)
    txt3.insert(INSERT, f"Расчет запаса Z = Z_АС-БС = Z_БС-АС = {Z}")
    P_bcac = 10 + 0.3 * mn
    P_acbc = 0.50 + 0.01 * mn
    Gi = 10 + 0.1 * mn
    nf = 0.50 + 0.01 * mn
    ndf = 2.50 + 0.02 * mn
    n_dip = 3 + 0.05 * mn
    P_bc_izl = np.round(P_bcac + Gi + 0 + nf + ndf + n_dip, 2)  # Вт
    P_ac_izl = np.round(P_acbc + Gi + 0 + nf + ndf + n_dip, 2)  # Вт
    txt3.insert(INSERT,
                f"\nЭквивалентная изотропно излучаемая мощность ЭИИМ: P_бс_изл = {P_bc_izl} и P_ас_изл = {P_ac_izl}")
    CN = 9
    NF_bcac = -100.0 + 0.05 * mn
    NF_acbc = -100.0 + 0.05 * mn
    P_ac_ch = -174 + 10 * np.log10(fk) + CN + NF_acbc
    P_bc_ch = -174 + 10 * np.log10(fk) + CN + NF_bcac
    txt3.insert(INSERT, f"\nЧувствительность приемника: P_бс_ч = {P_bc_ch} и P_ас_ч = {P_ac_ch}")
    Pmin_bc = P_bc_ch - Gi + nf + n_dip
    Pmin_ac = P_ac_ch - Gi + nf + n_dip
    txt3.insert(INSERT, f"\nЧувствительность приемника: P_бс_ч = {P_bc_ch} и P_ас_ч = {P_ac_ch}")
    h_trans = 60
    h_rec = 0.01
    d = 14
    A_bc = np.round((1.1 * np.log10(LTE_max - 0.7) * h_rec - (1.56 * np.log10(LTE_max) - 0.8)), 2)
    A_ac = np.round((1.1 * np.log10(LTE_min - 0.7) * h_rec - (1.56 * np.log10(LTE_min) - 0.8)), 2)
    L_bc_r = np.round(46.3 + 33.91 * np.log10(LTE_max) - A_bc + (44.9 - 6.55 * np.log10(h_trans)) * np.log10(d) - 3, 2)
    L_ac_r = np.round(46.3 + 33.91 * np.log10(LTE_min) - A_ac + (44.9 - 6.55 * np.log10(h_trans)) * np.log10(d) - 3, 2)
    txt3.insert(INSERT, f"\nЗатухание в больших городах: A_бс = {A_bc} и A_ас = {A_ac}")
    txt3.insert(INSERT, f"\nСреднее затухание в городе: P_бс_г = {L_bc_r} и P_ас_г = {L_ac_r}")
    L_bc_pr = np.round(L_bc_r - 2 * (np.log10(LTE_max/28) ** 2 - 5.4), 3)
    L_ac_pr = np.round(L_ac_r - 2 * (np.log10(LTE_min / 28) ** 2 - 5.4), 3)
    txt3.insert(INSERT, f"\nСреднее затухание в пригородных районах: P_бс_пр = {L_bc_pr} и P_ас_пр = {L_ac_pr}")
    L_bc_c = np.round(L_bc_r - 4.78 * (np.log10(LTE_max)) ** 2 + 17.33 * np.log10(LTE_max) - 40.94, 3)
    L_ac_c = np.round(L_ac_r - 4.78 * (np.log10(LTE_min)) ** 2 + 17.33 * np.log10(LTE_min) - 40.94, 3)
    txt3.insert(INSERT, f"\nСреднее затухание радиосигнала в сельской местности: P_бс_с = {L_bc_c} и P_ас_с = {L_ac_c}")
    L_bcac = np.round(P_bc_izl - Pmin_ac - Z, 2)
    L_acbc = np.round(P_ac_izl - Pmin_bc - Z, 2)
    txt3.insert(INSERT, f"\nСуммарные потери радиосигнала при распространении радиоволн"
                        f" от базовой станции к абонентской станции:"f" P_бс-ac = {L_bcac} и P_ас-bc = {L_acbc}")


btn = Button(window, text='Рассчитать', command=clicked)
btn.grid(column=2, row=0)
lbl1 = Label(window, text="Введите свой вариант: ")
lbl1.grid(column=0, row=0)
lbl2 = Label(window, text="Введите две последние цифра студака: ")
lbl2.grid(column=0, row=1)
lbl3 = Label(window, text="Введите размер кластера: ")
lbl3.grid(column=0, row=2)
lbl4 = Label(window, text="Введите размер секторов (3 или 6): ")
lbl4.grid(column=0, row=3)
enter1 = Entry(window, width=10)
enter1.grid(column=1, row=0)
enter1.focus()
enter2 = Entry(window, width=10)
enter2.grid(column=1, row=1)
enter3 = Entry(window, width=10)
enter3.grid(column=1, row=2)
enter4 = Entry(window, width=10)
enter4.grid(column=1, row=3)
window.mainloop()
