# 导入必要库
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
import pandas as pd
# 加载示例数据集（鸢尾花数据集）
iris = datasets.load_iris()
X = iris.data[:, :2]  # 使用前两个特征
y = iris.target




url = "https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv"
df = pd.read_csv(url)

# 显示数据前5行
print("原始数据示例：")
print(df.head())

# 数据概览
print("\n数据概览：")
print(f"数据维度：{df.shape}")
print("\n各列信息：")
print(df.info())
print("\n统计摘要：")
print(df.describe())

# ======================
# 2. 数据预处理
# ======================
# 处理缺失值
df['Age'].fillna(df['Age'].median(), inplace=True)
df['Fare'].fillna(df['Fare'].median(), inplace=True)

# 特征选择
features = ['Pclass', 'Sex', 'Age', 'Siblings/Spouses Aboard', 'Parents/Children Aboard', 'Fare']
target = 'Survived'

# 转换分类特征
df['Sex'] = df['Sex'].map({'male': 0, 'female': 1})

# 创建特征矩阵和目标向量
X = df[features]
y = df[target]

# ======================
# 3. 数据分割
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y  # 保持类别分布
)

# ======================
# 4. 特征工程
# ======================
# 标准化数值特征
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)












# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# 数据标准化
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 创建SVM分类器
# 常用参数：
# - C: 正则化参数（默认1.0）
# - kernel: 核函数（'linear', 'poly', 'rbf', 'sigmoid'）
# - gamma: 核系数（'scale'或'auto'）
svm = SVC(kernel='linear', C=1.0, random_state=42)

# 训练模型
svm.fit(X_train, y_train)

# 预测测试集
y_pred = svm.predict(X_test)

# 评估模型
accuracy = accuracy_score(y_test, y_pred)
print(f"Test accuracy: {accuracy:.2f}")

# 可视化决策边界（可选，仅适用于2D特征）
import matplotlib.pyplot as plt
import numpy as np


def plot_decision_boundary(clf, X, y):
    x_min, x_max = X[:, 0].min() - 1, X[:, 0].max() + 1
    y_min, y_max = X[:, 1].min() - 1, X[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, 0.02),
                         np.arange(y_min, y_max, 0.02))

    Z = clf.predict(np.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)

    plt.contourf(xx, yy, Z, alpha=0.8)
    plt.scatter(X[:, 0], X[:, 1], c=y, edgecolors='k')
    plt.xlabel('Sepal length')
    plt.ylabel('Sepal width')
    plt.title('SVM Decision Boundary')
    plt.show()


plot_decision_boundary(svm, X_train, y_train)