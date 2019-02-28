# 以MinMax算法为核心AI的井子棋，带Alpha-Beta剪枝 

## 函数说明：
- MinMaxGameTree，AI函数，极小极大博弈树算法
  - 参数：玩家player、当前状态chessboard、层策略strategy(max或min)、最大搜索深度max_depth及alpha、beta值
  - 返回值：以(落子位置，预计最佳得分)tuple为元素的list

- AlphaBetaGameTree，AI函数，MinMaxGameTree带剪枝的版本，可以降低搜索成本，增加搜索深度；
  - 参数：MinMaxGameTree所需参数及alpha、beta值；
  - 返回值：以(落子位置，预计最佳得分)tuple为元素的list，部分落子位置可能被裁剪

- Evaluate，得分评估函数，修改此函数的评分方式便可将算法运用到其他规则的游戏中
  - 参数：玩家player, 当前状态chessboard
  - 返回值：player在当前状态的得分