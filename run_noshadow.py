#!/usr/bin/env -S python3 -B

from time import time
from common.tk_drawer import TkDrawer
from noshadow.polyedr import Polyedr


tk = TkDrawer()
try:
    for name in ["ccc", "cube", "box", "king", "cow", "babem"]:
        print("=============================================================")
        print(f"Начало работы с полиэдром '{name}'")
        start_time = time()
        polyedr = Polyedr(f"data/{name}.geom")
        polyedr.draw(tk)
        print(f'Сумма площадей равна {polyedr.sum_area()}')
        delta_time = time() - start_time
        print(f"Изображение полиэдра '{name}' заняло {delta_time} сек.")
        input("Hit 'Return' to continue -> ")
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
