import cv2, numpy as np, mandelbulb as mandel

WHITE = (209,215,216)
ORANGE = (226,97,0)
MAGENTA = (169,43,159)
LIGHT_BLUE = (30,138,199)
YELLOW = (243,178,15)
LIME = (93,169,16)
PINK = (214,100,143)
GRAY = (51,55,59)
LIGHT_GRAY = (126,126,116)
CYAN = (13,120,136)
BLUE = (40,42,144)
PURPLE = (100,25,157)
GREEN = (72,91,31)
BROWN = (97,58,26)
RED = (144,30,30)
BLACK = (1,2,6)


COLORS = [BLACK, BLUE, LIGHT_BLUE, WHITE]
COLORS = COLORS + COLORS[-2:0:-1]

IMG = np.full((255,255,3), (255,255,255), np.uint8)


r = 255 // 2

space = np.mgrid[-r:r+1, 0:r, -r:r+1].reshape(3,-1).astype(np.float).T
c = space * 1.2 / r
z = np.zeros_like(c)
i = np.zeros((c.shape[0], 1), dtype=np.int)

for _ in range(5):
    z2, mask = mandel.step(z.copy())
    z2 = z2 + c
    rows = np.where(mask)
    z[rows] = z2[rows]
    i[rows] += 1

print('done')

iter_pos = np.concatenate((i, space, z), 1)

for v in iter_pos:
    if 3 < v[0] and np.linalg.norm(v[4:7]) >= 2:

        color = COLORS[int(np.linalg.norm(v[1:4])) // 2 % len(COLORS)]
        
        x,y = int(v[1]),int(v[3])
        
        IMG[y + r,x + r] = color

IMG = cv2.resize(IMG, (500, 500), interpolation=cv2.INTER_NEAREST)
IMG = cv2.cvtColor(IMG, cv2.COLOR_RGB2BGR)
cv2.imshow("a", IMG)
cv2.waitKey()