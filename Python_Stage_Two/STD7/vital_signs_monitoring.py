import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置中文字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号

# 创建示例数据（ICU患者生命体征）
time = pd.date_range('2024-01-01 00:00:00', '2024-01-01 23:59:59', freq='15T')
np.random.seed(42)

# 患者基本信息
patient_id = 'P001'
patient_name = 'John Doe'

# 生命体征数据
heart_rate = 70 + 10 * np.sin(np.linspace(0, 8*np.pi, len(time))) + np.random.normal(0, 3, len(time))
# 收缩压
blood_pressure_systolic = 120 + 15 * np.sin(np.linspace(0, 6*np.pi, len(time))) + np.random.normal(0, 5, len(time))
# 舒张压
blood_pressure_diastolic = 80 + 10 * np.sin(np.linspace(0, 7*np.pi, len(time))) + np.random.normal(0, 3, len(time))
temperature = 36.5 + 1.5 * np.sin(np.linspace(0, 5*np.pi, len(time))) + np.random.normal(0, 0.2, len(time))
# 血氧饱和度（spo2）
spo2 = 98 - 2 * np.sin(np.linspace(0, 4*np.pi, len(time))) + np.random.normal(0, 0.5, len(time))

# 创建图表
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))

# 1. 心率监测
ax1.plot(time, heart_rate, 'b-', linewidth=2, label='心率 (bpm)')
ax1.axhline(y=60, color='red', linestyle='--', alpha=0.5, label='正常下限')
ax1.axhline(y=100, color='red', linestyle='--', alpha=0.5, label='正常上限')
ax1.fill_between(time, 60, 100, alpha=0.1, color='green', label='正常范围')
ax1.set_title(f'患者 {patient_id} - {patient_name} 生命体征监测', fontsize=14, fontweight='bold')
ax1.set_ylabel('心率 (bpm)', fontsize=12)
ax1.legend(loc='upper right', fontsize=10, framealpha=0.9)
ax1.grid(True, alpha=0.3)

# 2. 血压监测
ax2.plot(time, blood_pressure_systolic, 'r-', linewidth=2, label='收缩压')
ax2.plot(time, blood_pressure_diastolic, 'b-', linewidth=2, label='舒张压')
ax2.set_ylabel('血压 (mmHg)', fontsize=12)
ax2.legend(loc='upper right', fontsize=10, framealpha=0.9)
ax2.grid(True, alpha=0.3)

# 3. 体温监测
ax3.plot(time, temperature, 'g-', linewidth=2, label='体温 (°C)')
ax3.axhline(y=37.5, color='orange', linestyle='--', label='发热阈值')
ax3.set_ylabel('体温 (°C)', fontsize=12)
ax3.legend(loc='upper right', fontsize=10, framealpha=0.9)
ax3.grid(True, alpha=0.3)

# 4. SpO2监测
ax4.plot(time, spo2, 'purple', linewidth=2, label='SpO2 (%)')
ax4.axhline(y=95, color='red', linestyle='--', alpha=0.5, label='正常下限')
ax4.set_ylabel('SpO2 (%)', fontsize=12)
ax4.set_xlabel('时间', fontsize=12)
ax4.legend(loc='upper right', fontsize=10, framealpha=0.9)
ax4.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()