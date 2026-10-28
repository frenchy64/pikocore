import glob
import os

fnames = glob.glob("easings/*txt")
fnames = list(fnames)
fnames.sort()

ee = []
for i, fname in enumerate(fnames):
    x = []
    y = [0]
    name = os.path.basename(fname).split(".")[0]
    with open(fname, "r") as f:
        for line in f:
            line = line.strip()
            if line == "":
                continue
            nums = line.split()
            if len(nums) != 2:
                continue
            if int(nums[1]) < 0:
                continue
            x.append(int(nums[0]))
            y.append(min(255, int(nums[1])))
    ee.append({"x": x, "y": y, "name": name})

for i, ease in enumerate(ee):
    xs = ease["x"]
    ys = ease["y"]
    name = ease["name"]
    xlen = len(xs)
    first_change = None
    npoints = len(xs) # ys has an extra element
    xmin = xs[0]
    xmax = xs[npoints-1]
    xmin_val = ys[0]
    xmax_val = ys[npoints-1]
    lookup_len = xmax-xmin+1
    lookup = [None] * lookup_len
    # set the known values
    for i in range(0, xlen):
        lookup[xs[i]-xmin] = ys[i]
    # fill in the intermediate values
    for i in range(lookup_len-2, -1, -1):
        if not lookup[i]:
            lookup[i] = lookup[i+1]
    print(f"uint8_t ease_{name}(uint16_t v) {{")
    print(f"\tv=v/8;")
    print(f"\tuint8_t lookup[] {{")
    for y in lookup:
        print(f"\t{y},")
    print("};")
    print(f"\tif (v < {xmin}) {{ return {xmin_val}; }}")
    print(f"\tif (v >= {xmax}) {{ return {xmax_val}; }}")
    print(f"\treturn lookup[v-{xmin}];")
    print("}")


try:
    import matplotlib.pyplot as plt
    import numpy as np
except ImportError:
    plt = None
    np = None

if plt is not None and np is not None:
    for i, ease in enumerate(ee):
        xs = np.multiply(ease["x"], 8 / 4095)
        ys = ease["y"]
        name = ease["name"]
        plt.plot(xs, ys[1:], alpha=0.4)
        plt.fill_between(xs, ys[1:], alpha=0.2, label=name)
        # plt.gca().add_patch(patch1)
    plt.legend(
        loc="upper center", bbox_to_anchor=(0.25, 1.1), ncol=1, fancybox=True, shadow=True
    )
    plt.xlabel("knob")
    plt.ylabel("result")
    plt.savefig("easings.png")
