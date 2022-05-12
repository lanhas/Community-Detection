import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QMainWindow, QWidget, QGridLayout, QHeaderView, QTableWidgetItem
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# 通过matplotlib.backends.backend_qt5agg类连接PyQt5
# 使用FigureCanvas和Figure类创建plot绘制窗口
# 使用 matplotlib中的FigureCanvas (在使用 Qt5 Backends中 FigureCanvas继承自QtWidgets.QWidget)
from networkx import spectral_layout, random_layout

import dataset
import model
from interface.detection import Ui_CommunityDetection as detecForm

matplotlib.use("Qt5Agg")  # 声明使用QT5


class BaseMainWindow(QMainWindow):
    """
    对QDialog类重写，实现一些功能
    """
    def closeEvent(self, event):
        """
        重写closeEvent方法，实现dialog窗体关闭时执行一些代码
        :param event: close()触发的事件
        :return: None
        """
        reply = QMessageBox.question(self, '本程序',
                                        "是否要退出界面？",
                                        QMessageBox.Yes | QMessageBox.No,
                                        QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class PlotFigure(FigureCanvas):
    """
    通过继承FigureCanvas类，使得该类既是一个PyQt5的Qwidget，
    又是一个matplotlib的FigureCanvas，这是连接pyqt5与matplotlib的关键。

    该类用于绘制不同的社交网络
    """
    def __init__(self, width=5, height=4, dpi=100):
        # 创建一个Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super(PlotFigure, self).__init__(self.fig)
        # 生成画布，作为控件添加到GUI
        self.canvas = FigureCanvas(self.fig)
        self.axes = self.fig.add_subplot(111)

    def plot_karate(self):
        """
        绘制空手道网络
        """
        g_karate = nx.karate_club_graph()
        pos = nx.spring_layout(g_karate, seed=100)  # 设置布局
        options = {
            "node_color": "black",
            "node_size": 50,
            "linewidths": 0,
            "width": 0.1,
        }
        # ax指定网络绘制在哪一个子图上
        nx.draw(g_karate, **options, pos=pos, ax=self.axes)

    def plot_(self, name):
        """
        绘制其余网络
        """
        if name == 'karata':
            self.plot_karate()
        else:
            data = dataset.make(name)
            data_txt = data.get_txt()
            data_gml = data.get_gml().split("\n")[1:]
            data.close()
            # 删除mejn文件中带有#的第一行伪代码
            G = nx.parse_gml(data_gml)  # 解析gml数据
            print(data_txt)
            # print degree for each team - number of games
            for n, d in G.degree():
                print(f"{n:20} {d:2}")
            options = {
                "node_color": "black",
                "node_size": 50,
                "linewidths": 0,
                "width": 0.1,
            }
            print(G.edges)
            # nx.draw(G, **options, pos=nx.spring_layout(G, seed=100), ax=self.axes)
            nx.draw(G, **options, pos=random_layout(G), ax=self.axes)

    def plot_result(self, graph, com):
        """
        绘制结果图，将社区划分结果以不同的颜色进行标记区分
        """
        # pos = nx.spring_layout(graph, seed=100)
        pos = nx.random_layout(graph, seed=100)
        size = len(com)
        count = 0
        color_list = ['pink', 'orange', 'r', 'g', 'b', 'y', 'm', 'gray', 'black', 'c', 'brown']
        for i in range(len(com)):
            # nx.draw(graph, pos, node_size=50, linewidths=0, width=0.1, nodelist=com[i],
            #         node_color=color_list[i], ax=self.axes)
            count = count+1
            nx.draw(graph, pos, node_size=50, linewidths=0, width=0.1, nodelist=com[i],
                    node_color=str(count / size), ax=self.axes)

    def plot_metric(self, x, y, s_label):
        """
        绘制度量指标模块图
        """
        self.axes.plot(x, y, label=s_label)


class DetecNetwork(QWidget, detecForm):
    """
    复杂社交网络社区检测
    """
    def __init__(self, parent=None):
        super(DetecNetwork, self).__init__(parent)
        self.setupUi(self)
        # lineEditParameters默认不可输入
        self.lineEditParameters.setEnabled(False)
        # 下拉框中对不同的值所做出的反应
        self.comboBoxInputAlgorithm.currentTextChanged.connect(self.combox_input_algorithm_changed)
        # 设置表单控件水平、垂直方向等宽且自适应窗口
        self.tableWidgetCompareResult.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidgetCompareResult.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 定义一个PlotFigure类的实例
        self.F = PlotFigure(width=3, height=2, dpi=100)
        self.F1 = PlotFigure(width=3, height=2, dpi=100)
        self.F2 = PlotFigure(width=3, height=2, dpi=100)
        self.dataset_dict = {"Karata_Network": "karata",
                             "Dolphin_Network": "dolphins",
                             "football_Network": "football",
                             "cond-mat_Network": "cond_mat"}
        self.model_dict = {"LPA": "lpa",
                           "GN": 'gn',
                           "Louvain": 'louvain'}
        self.metrics_dict = {"Modularity": "modularity",
                             "NMI": "nmi"}

    def combox_input_algorithm_changed(self):
        """
        QComboBox(comboBoxInputAlgorithm)切换选项触发事件
        """
        if self.comboBoxInputAlgorithm.currentIndex() == 2:
            self.lineEditParameters.setEnabled(True)
        else:
            self.lineEditParameters.setEnabled(False)

    def submit_alog(self):
        """
        提交按钮的槽函数，用户输入网络和算法，并展示真实网络图和社区划分图
        """
        self.plot_data_graph()
        self.plot_alg_graph()

    def plot_data_graph(self):
        """
        绘制真实网络并显示
        """
        self.F.axes.cla()
        current_network = self.comboBoxInputNetwork.currentText()
        self.F.plot_(self.dataset_dict[current_network])
        self.gridlayout = QGridLayout(self.groupBox_4)  # 继承容器groupBox
        self.gridlayout.addWidget(self.F, 0, 1)  # 将F这个控件加入到布局中
        self.F.draw()

    def plot_alg_graph(self):
        """
        获取界面用户所选择的信息，进行相应的社区划分，在figure上绘制网络,将绘制好的F1添加到布局中进行显示
        """
        # 获取选择框中的算法信息并创建相应的算法对象
        model_ = model.make(self.model_dict[self.comboBoxInputAlgorithm.currentText()])
        # 获取选择框中的数据集信息并创建相应的数据集对象
        data_ = dataset.make(self.dataset_dict[self.comboBoxInputNetwork.currentText()])
        # 解析gml数据生成图G
        G = nx.parse_gml(data_.get_gml().split("\n")[1:], label='id')
        # 对图G进行社区划分并得到其划分结果com（com为List形式）
        if self.comboBoxInputAlgorithm.currentText() == "GN":
            k = int(self.lineEditParameters.text()) - 1
            com = model_.run(G, k)
        else:
            com = model_.run(G)
        self.F1.axes.cla()
        self.F1.plot_result(G, com)
        self.gridlayout1 = QGridLayout(self.groupBox_3)  # 继承容器groupBox
        self.gridlayout1.addWidget(self.F1, 0, 1)  # 将F这个控件加入到布局中
        self.F1.draw()

    def plot_metrics_graph(self):
        """
        绘制度量指标在不同数据集上的折线图，并且是确定按钮的槽函数
        """
        # 获取度量指标
        metric_ = model.make(self.metrics_dict[self.comboBoxMeasure.currentText()])
        # 数据集
        data = ["karata", "football", "dolphins"]
        res1 = []
        res2 = []
        res3 = []
        for item_data in data:
            data_ = dataset.make(item_data)
            G = nx.parse_gml(data_.get_gml().split("\n")[1:], label='id')
            # LPA
            alg1 = model.make('lpa')
            com1 = alg1.run(G)
            res1.append(metric_.calculate(G, com1))
            # GN
            k = int(self.lineEditParameters2.text()) - 1
            alg2 = model.make('gn')
            com2 = alg2.run(G, k)
            res2.append(metric_.calculate(G, com2))
            # louvain
            alg3 = model.make('louvain')
            com3 = alg3.run(G)
            res3.append(metric_.calculate(G, com3))

        self.F2.axes.cla()
        self.F2.plot_metric(data, res1, 'lpa')
        self.F2.plot_metric(data, res2, 'gn')
        self.F2.plot_metric(data, res3, 'louvain')
        # 绘制图例的位置(右下)
        self.F2.axes.legend(loc='lower right')
        self.gridlayout1 = QGridLayout(self.groupBox_5)  # 继承容器groupBox
        self.gridlayout1.addWidget(self.F2, 0, 1)  # 将F这个控件加入到布局中
        self.F2.draw()
        self.plot_metrics_table(res1, res2, res3)

    def plot_metrics_table(self, result1, result2, result3):
        """
        在表格中显示度量指标计算完成后的值
        """
        result = [result1, result2, result3]
        # 逐个将度量指标的值填入表格
        for column_num in range(self.tableWidgetCompareResult.columnCount()):
            for row_num in range(self.tableWidgetCompareResult.rowCount()):
                item = QTableWidgetItem()
                item.setText(str(result[row_num][column_num]))
                # 水平居中
                item.setTextAlignment(Qt.AlignCenter)
                # 设置单元格内容不可修改
                item.setFlags(Qt.ItemIsEnabled)
                self.tableWidgetCompareResult.setItem(column_num, row_num, item)

    def exit_alog(self):
        """
        退出算法计算页面
        """
        pass



