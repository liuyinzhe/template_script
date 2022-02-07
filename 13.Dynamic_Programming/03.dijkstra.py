# 参考自 https://www.cnblogs.com/goldsunshine/p/12978305.html # 主要代码来源，文字不好理解
# 辅助：b站 https://www.bilibili.com/video/BV1QK411V7V4/  # 推荐看视频理解，慢慢对照代码，我主要看视频理解了，然后慢慢对照视频看代码理解
# 辅助: b站 # abcdef 换成123456
# used_node 为S(T/F);  表示已经选为最短路径的点
# 寻找下一个 访问的点时， F的点可以选， T的点不能选
# dis 为distance  为used_node 为 F 时，更新最短的距离 
# 注释学习
# 参考阅读:https://www.cnblogs.com/leokale-zz/p/12378193.html

# dijkstra 的思路特点就是： 从起点开始找直接可以访问的node 点之间的距离，并记录起点到这个点的最短路径；
# 新的点，继续向外衍生，寻找 起点到这个点的最短距离，记录并比较所有可能分支； 
# 由于distance 记录起点到下一点的最短距离之和；多个局部贪心，重叠找最短，最终可以求得全局最优解



MAX= float('inf')

matrix = [
    [0,10,MAX,4,MAX,MAX],
    [10,0,8,2,6,MAX],
    [MAX,8,0,15,1,5],
    [4,2,15,0,6,MAX],
    [MAX,6,1,6,0,12],
    [MAX,MAX,5,MAX,12,0]
    ]

#矩阵中，查看 C点到其他点的距离，则看3列为 0 的行，或者第三行为0的位置，他的代码矩阵0写成了10；写错了
# matrix = [
#      A  B  C  D  E   F
#   A [0,10,MAX,4,MAX,MAX],
#   B [10,0,8,2,6,MAX],
#   C [MAX,8,0,15,1,5],
#   D [4,2,15,0,6,MAX],
#   E [MAX,6,1,6,0,12],
#   F [MAX,MAX,5,MAX,12,0]
#     ]

 

def dijkstra(matrix, start_node):
    
    #矩阵一维数组的长度，即节点的个数
    matrix_length = len(matrix)

    #访问过的节点数组
    used_node = [False] * matrix_length

    #最短路径距离数组
    distance = [MAX] * matrix_length
    #存储 start_node 起点到任意点的最短距离之和

    #初始化，将起始节点的最短路径修改成0
    distance[start_node] = 0 
    
    #将访问节点中未访问的个数作为循环值，其实也可以用个点长度代替。
    while used_node.count(False):
        min_value = float('inf')
        min_value_index = 999 # 初始值
        
        #在最短路径节点中找到最小值，已经访问过的不在参与循环。
        #得到最小值下标，每循环一次肯定有一个最小值
        # 第一次时，最小值就是起点，第二次时，最小值的未经过的下一个点
        # 获得最短分支，由于其他无法访问的是正无穷 inf 所以 遍历时肯定大于最小值
        for index in range(matrix_length):
            if not used_node[index] and distance[index] < min_value:
                min_value = distance[index]
                min_value_index = index
        
        # 分支 最短的 改为 True
        #将访问节点数组对应的值修改成True，标志其已经访问过了
        used_node[min_value_index] = True

        #更新distance数组。
        #以B点为例：distance[x] 起始点达到B点的距离，
        #distance[min_value_index] + matrix[min_value_index][index] 是起始点经过某点达到B点的距离，比较两个值，取较小的那个。
        for index in range(matrix_length):
            distance[index] = min(distance[index], distance[min_value_index] + matrix[min_value_index][index])

    return distance



# 起始节点，就是ABCDE， index 0-5
start_node = int(input('请输入起始节点:'))
result = dijkstra(matrix,start_node)
print('起始节点到其他点距离：%s' % result)
