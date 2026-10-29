import glob
import os

fnames = glob.glob("easings/*txt")
fnames = list(fnames)
fnames.sort()

knob_bits = 12
min_knob_value = 50
max_knob_value = 2**knob_bits-1
max_input_value = int(max_knob_value / 8)
min_input_value = int((min_knob_value/max_knob_value)*max_input_value)

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
            next_x = int(nums[0])
            if next_x < min_input_value:
                continue
            x.append(next_x)
            y.append(min(255, int(nums[1])))
            last_point = len(x)-1
            if next_x > max_input_value:
                x[last_point] = max_input_value
                y[last_point] = y[last_point-1]
                break;

    del y[-1]
    ee.append({"x": x, "y": y, "name": name})

total_const_bytes = 0

for ease in ee:
    xs = ease["x"]
    ys = ease["y"]
    name = ease["name"]
    npoints = len(xs)
    xmin = xs[0]
    xmax = xs[npoints-1]
    xmin_val = ys[0]
    xmax_val = ys[npoints-1]
    lookup_len = xmax-xmin+1
    total_const_bytes += lookup_len
    lookup = [None] * lookup_len
    # set the known values
    for i in range(0, npoints):
        lookup[xs[i]-xmin] = ys[i]
    # fill in the intermediate values
    for i in range(lookup_len-2, -1, -1):
        if not lookup[i]:
            lookup[i] = lookup[i+1]
    print(f"// v = {min_input_value}..{max_input_value}")
    print(f"uint8_t ease_{name}(uint16_t v) {{")
    print(f"\tconstexpr uint8_t lookup[{lookup_len}] {{")
    for y in lookup:
        print(f"\t{y},")
    print("};")
    if xmin > min_input_value:
        print(f"\tif (v < {xmin}) {{ return {xmin_val}; }}")
    if xmax < max_input_value:
        print(f"\tif (v > {xmax}) {{ return {xmax_val}; }}")
    print(f"\t// {xmin}..{xmax} => {xmin-xmin}..{xmax-xmin}")
    print(f"\treturn lookup[v-{xmin}];")
    print("}")

print(f"// const arrays = {total_const_bytes} bytes")

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
