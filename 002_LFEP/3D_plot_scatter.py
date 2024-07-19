import numpy as np
from mayavi import mlab
from scipy.spatial import cKDTree

# 文件路径和参数
PMF_FILE = "free_energy.abf1.czar.pmf"                  # 自由能数据文件
TRAJ_FILE = "free_energy.abf1.czar.traj"                # 散点数据文件
CONTOUR_LEVELS = [1.5, 4, 7]                                   # 轮廓水平
CONTOUR_COLOR_RANGE = [1, 10]                                  # 轮廓颜色范围
CONTOUR_OPACITIES = [0.9, 0.4, 0.3]                            # 轮廓不透明度
AXIS_NAME = ["phi_1", "phi_2", "phi_3"]                        # 轴标签
AXIS_RANGE = [-180, 180, -180, 180, -180, 180]                 # 轴范围
NUM_BINS = [72j, 72j, 72j]                                     # 网格点数量

# 加载自由能数据
data = np.loadtxt(PMF_FILE)
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
f = data[:, 3]

# 生成网格
grid_x, grid_y, grid_z = np.mgrid[
    x.min():x.max():NUM_BINS[0],
    y.min():y.max():NUM_BINS[1],
    z.min():z.max():NUM_BINS[2]
]

# 使用最近邻插值生成网格上的自由能数据
tree = cKDTree(np.c_[x, y, z])
distances, indices = tree.query(np.c_[grid_x.ravel(), grid_y.ravel(), grid_z.ravel()])
grid_f = f[indices].reshape(grid_x.shape)

# 创建图形
fig = mlab.figure('3D Contour', bgcolor=(1, 1, 1))

# 绘制等高线
for i, level in enumerate(CONTOUR_LEVELS):
    contour = mlab.contour3d(grid_x, grid_y, grid_z, grid_f, contours=[level], opacity=CONTOUR_OPACITIES[i])

# 配置颜色映射
lut_manager = contour.module_manager.scalar_lut_manager
lut_manager.data_range = [f.min(), f.max()]
lut_manager.lut.scale = 'linear'
lut_manager.lut.range = (CONTOUR_COLOR_RANGE[0], CONTOUR_COLOR_RANGE[1])

# 添加轴标签
axes = mlab.axes(contour, xlabel=AXIS_NAME[0], ylabel=AXIS_NAME[1], zlabel=AXIS_NAME[2], color=(0, 0, 0), line_width=0.1)
axes.axes.bounds = AXIS_RANGE
axes.label_text_property.color = (0, 0, 0)
axes.title_text_property.color = (0, 0, 0)

# 添加轮廓
outline = mlab.outline(color=(0, 0, 0), line_width=2.5)
outline.bounds = AXIS_RANGE

# 设置视角
mlab.view(azimuth=0, elevation=90, distance='auto', focalpoint=(0, 0, 0))
fig.scene.camera.parallel_projection = True

# 加载散点数据
traj_data = np.loadtxt(TRAJ_FILE)
traj_x = traj_data[:, 0]
traj_y = traj_data[:, 1]
traj_z = traj_data[:, 2]

# 绘制散点图
mlab.points3d(traj_x, traj_y, traj_z, color=(0, 0, 0), scale_factor=10)

# 显示图形
mlab.show()