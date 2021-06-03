import matplotlib.pyplot as plt

# fre = [0.18556, 0.18556, 0.23974, 0.23974, 0.27902, 0.27902, 0.29154, 0.29154, 0.29566, 0.29566, 0.35092, 0.35092, 0.35754, 0.35754, 0.81442, 0.81442, 1]
# # fat = [9.5,26.5,7.8,17.8,31.4,25.9,27.4,27.2,31.2,34.6,42.5,28.8,33.4,30.2,34.1,23.9,35.7]

# plt.xlabel("Fre")
# plt.ylabel("Frequency")
# plt.boxplot(fre,sym="o",whis=1.5)
# plt.show()

x_values = [0.3516, 0.2938, 0.8078, 0.3546, 0.1922, 0.2931, 0.2931, 0.2375, 0.2375, 0.8078, 0.2772, 0.2772]
y_values = [1,1,1,1,1,0.8265, 0.8265,  0.80837,  0.80837, 0.8078, 0.78839, 0.78839]
'''
scatter() 
x:横坐标 y:纵坐标 s:点的尺寸
'''
plt.scatter(x_values, y_values, s=50)
 
# 设置图表标题并给坐标轴加上标签
plt.title('The support and the configure.', fontsize=15)
plt.xlabel('Support', fontsize=12)
plt.ylabel('Conf', fontsize=12)
 
# 设置刻度标记的大小
plt.tick_params(axis='both', which='major', labelsize=10)
plt.show()

# plt.xlabel("fat")
# plt.ylabel("value")
# plt.boxplot(fat,sym="o",whis=1.5)
# plt.show()