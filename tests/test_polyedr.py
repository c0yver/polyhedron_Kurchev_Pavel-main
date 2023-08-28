from pytest import approx
from shadow.polyedr import Polyedr

i = 0
a = [0]*6
a[0] = 25.0
for j in range(5):
    a[j+1] = 0

for name in ["ccc", "cube", "box", "king", "cow", "babem"]:
    polyedr = Polyedr(f"data/{name}.geom")
    assert polyedr.sum_area() == approx(a[i])
    i += 1
