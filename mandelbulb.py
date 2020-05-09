
import numpy as np


# if true generates a .mcfunction full of commands
# otherwise returns the coords in a binary file
DATAPACK = True 

COLORS = ['black', 'gray', 'white']
COLORS = COLORS + COLORS[-2:0:-1] # transforms palette into a loop pattern

SIZE = 40
ITERS = 20
N = 8
LIMIT = 2
ZOOM = 1.5


def step(z):
    r = np.linalg.norm(z, axis=1)
    theta = np.arctan2(np.linalg.norm(z[:,:2], axis=1), z[:,2])
    phi = np.arctan2(z[:,1],z[:,0])
    
    rn = r**N
    thetan = theta * N
    phin = phi * N
    rn_sin_thetan = rn * np.sin(thetan)

    z[:,0] = rn_sin_thetan * np.cos(phin)
    z[:,1] = rn_sin_thetan * np.sin(phin)
    z[:,2] = rn * np.cos(thetan)
    return z, r <= LIMIT


space = np.mgrid[-SIZE:SIZE+1, -SIZE:SIZE+1, -SIZE:SIZE+1].reshape(3,-1).astype(np.float).T
c = space * ZOOM / SIZE
z = np.zeros_like(c)
i = np.zeros((c.shape[0], 1), dtype=np.int)

for _ in range(ITERS):
    z2, mask = step(z.copy())
    z2 = z2 + c
    rows = np.where(mask)
    z[rows] = z2[rows]
    i[rows] += 1


iter_pos = np.concatenate((i, space, z), 1)

with open('mandelbulb.mcfunction' if DATAPACK else 'mandelbulb.bin', 'w' if DATAPACK else 'wb') as OUT:
    def compare_and_print(v):
        global ITERS, COLORS, OUT, LIMIT
        
        if 3 < v[0] and np.linalg.norm(v[4:7]) >= LIMIT:

            color = COLORS[int(np.linalg.norm(v[1:4])) % len(COLORS)]

            if DATAPACK:
                OUT.write(f'setblock ~{v[1]} {int(v[3]) + SIZE - 1} ~{v[2]} {color}_concrete\n')
            else:
                rho = int(np.linalg.norm(v[1:4]))
                OUT.write(rho.to_bytes(4, 'big', signed=True) + int(v[1]).to_bytes(4, 'big', signed=True) + int(v[3]).to_bytes(4, 'big', signed=True) + int(v[2]).to_bytes(4, 'big', signed=True))        
    np.apply_along_axis(compare_and_print, 1, iter_pos)
