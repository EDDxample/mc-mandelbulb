
import numpy as np

# Big overhaul to make it work for the video, check like the 1st-2nd commit for datapack version


# if true generates a .mcfunction full of commands
# otherwise returns the coords in a binary file
DATAPACK = False 

COLORS = ['black', 'gray', 'white']

SIZE = 128
ITERS = 20
N = 8
LIMIT = 2
ZOOM = 1.5


def getInt(n):
    larr = 16 # hardcoded COLORS length
    i = n % (larr * 2 - 2)
    if i < larr: return i
    i %= larr
    return larr - i - 2


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

def compare_and_print(v):
    global ITERS, COLORS, CUBE, LIMIT, SIZE
    
    if 3 < v[0] and np.linalg.norm(v[4:7]) >= LIMIT:

        color = COLORS[int(np.linalg.norm(v[1:4])) % len(COLORS)]
        
        r = int(np.linalg.norm(v[1:4]))

        CUBE[int(v[1] + SIZE), int(v[3] + SIZE), int(v[2] + SIZE)] = getInt(r)


space = np.mgrid[-SIZE:SIZE+1, -SIZE:SIZE+1, -SIZE:SIZE+1].reshape(3,-1).astype(np.float).T
c = space * ZOOM / SIZE
z = np.zeros_like(c)
i = np.zeros((c.shape[0], 1), dtype=np.int)

for it in range(ITERS):
    print(f'{it * 100 // ITERS }%' )
    z2, mask = step(z.copy())
    z2 = z2 + c
    rows = np.where(mask)
    z[rows] = z2[rows]
    i[rows] += 1

print('100%')

iter_pos = np.concatenate((i, space, z), 1)

CUBE = np.full((255,255,255), 16, dtype=np.byte)

np.apply_along_axis(compare_and_print, 1, iter_pos)


print('spiral')
# gen spiral iteration
Xs = []
Zs = []

for r in range(SIZE):
    prev = r - 1
    for x in range(-r,r+1):
        for z in range(-r,r+1):
            if prev * prev <= x*x + z*z < r*r:
                Xs.append(x + SIZE)
                Zs.append(z + SIZE)

print('out')

with open('mandelbulb.bin', 'wb') as out:
    for y in range(255):
        print(y)
        for x, z in zip(Xs, Zs): # 50613
            if CUBE[x, y, z] < 16:
                print(x,y,z)
                out.write(
                    (x - SIZE).to_bytes(1, 'big', signed=True)+
                    (y - SIZE).to_bytes(1, 'big', signed=True)+
                    (z - SIZE).to_bytes(1, 'big', signed=True)+
                    int(CUBE[x, y, z]).to_bytes(1, 'big', signed=True)
                )
