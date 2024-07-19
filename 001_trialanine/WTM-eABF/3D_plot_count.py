import numpy as np
from mayavi import mlab
from scipy.spatial import cKDTree

PMF_FILE = "output/free_energy.abf1.zcount"                    # The input count file containing samples in each bin
CONTOUR_LEVELS = [1000, 500, 200]                              # Contour levels corresponding to count values
CONTOUR_COLOR_RANGE = [100, 1500]                              # Color range for contour levels
CONTOUR_OPACITIES = [0.1, 0.3, 0.5]                            # Opacity for each contour level

AXIS_NAME = ["phi_1", "phi_2", "phi_3"]                        # Labels for each axis
AXIS_RANGE = [-180, 180, -180, 180, -180, 180]                 # Range for each axis
NUM_BINS = [72j,72j,72j]                                       # Number of bins

data = np.loadtxt(PMF_FILE)

x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
f = data[:, 3]

grid_x, grid_y, grid_z = np.mgrid[
    x.min():x.max():NUM_BINS[0],
    y.min():y.max():NUM_BINS[1],
    z.min():z.max():NUM_BINS[2]
]

tree = cKDTree(np.c_[x, y, z])
distances, indices = tree.query(np.c_[grid_x.ravel(), grid_y.ravel(), grid_z.ravel()])
grid_f = f[indices].reshape(grid_x.shape)

fig = mlab.figure('3D Contour', bgcolor=(1, 1, 1))

for i, level in enumerate(CONTOUR_LEVELS):
    contour = mlab.contour3d(grid_x, grid_y, grid_z, grid_f, contours=[level], opacity=CONTOUR_OPACITIES[i])

lut_manager = contour.module_manager.scalar_lut_manager

lut_manager.data_range = [f.min(), f.max()]

lut_manager.lut.scale = 'linear'
lut_manager.lut.range = (CONTOUR_COLOR_RANGE[0], CONTOUR_COLOR_RANGE[1])

axes = mlab.axes(contour, xlabel=AXIS_NAME[0], ylabel=AXIS_NAME[1], zlabel=AXIS_NAME[2], color=(0, 0, 0), line_width=0.1)

axes.axes.bounds = AXIS_RANGE

axes.label_text_property.color = (0, 0, 0)
axes.title_text_property.color = (0, 0, 0)

outline = mlab.outline(color=(0, 0, 0), line_width=2.5)
outline.bounds = AXIS_RANGE

mlab.view(azimuth=0, elevation=90, distance='auto', focalpoint=(0, 0, 0))
fig.scene.camera.parallel_projection = True

mlab.show()