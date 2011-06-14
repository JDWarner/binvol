import mahotas
import numpy as np
from scipy import ndimage

def perim(image):
    return mahotas.labeled.borders(image, np.ones((3, 3)))

def smooth(image):
    dt = 1/6.0
    u = image.astype('float64')
    A0 = perim(image)
    A1 = perim(A0)
    A2 = perim(A1)
    A3 = perim(A2)
    A = A0 | A1 | A2 | A3

    for i in xrange(10):
        gy, gx = np.gradient(u)

        # gradient magnitude
        g_mag = np.sqrt(gx**2 + gy**2)

        n_gy = gy / (g_mag + (g_mag == 0))
        n_gx = gx / (g_mag + (g_mag == 0))

        dy_n_gx, dx_n_gx = np.gradient(n_gx)
        dy_n_gy, dx_n_gy = np.gradient(n_gy)
        
        # mean curvature
        k = dx_n_gx + dy_n_gy

        # H is the gradient magnitude times the mean curvature
        H = g_mag * k

        nu = u.copy()
        temp_u = u + dt * H
        print temp_u
        nu[image] = np.fmax(temp_u[image], 0)
        nu[~image] = np.fmin(temp_u[~image], 0)

        u = nu.copy()

    return nu


def binvol(image):
    # image must be binary
    B = perim(image)
    return B

def main():
    from scipy.misc.common import lena
    from scipy.misc import imsave
    l = lena().astype('uint8')
    o = mahotas.otsu(l)
    #bl = np.empty(l.shape, dtype='uint8')
    bl = l >= o
    s = smooth(bl) * 255
    imsave('test.png', s)

if __name__ == '__main__':
    main()