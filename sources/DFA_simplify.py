# 添加分组标志
def add_tag(dfa_table):
    for i in dfa_table:
        i.extend([i[0]])


# 对节点进行分组
def sectionalization(dfa_table, normal_table, end_table):
    # 测试用数据，用来记录终态和非终态的状态
    normal = normal_table
    end = end_table
    # 标志位，用来标志是否发现同一组节点
    find = False
    for y1 in range(0, len(dfa_table)):
        for y2 in range(0, len(dfa_table)):
            # 两个节点都是非终态
            if y1 != y2 and y1 + 1 in normal and y2 + 1 in normal and dfa_table[y2][-1][0] == y2 + 1:
                for x in range(1, len(dfa_table[y1]) - 1):
                    # 如果两个节点都可以跳向同一个节点，则两个节点可以归为一类，则tag设为相同的并跳出循环
                    if dfa_table[y1][x] == dfa_table[y2][x] and dfa_table[y1][x] != []:
                        dfa_table[y2][-1] = dfa_table[y1][-1]
                        find = True
                        break
            # 找到了相同状态的节点，跳出循环
            if find:
                find = False
                break
            # 两个节点都是终态
            if y1 != y2 and y1 + 1 in end and y2 + 1 in end and dfa_table[y2][-1][0] == y2 + 1:
                for x in range(1, len(dfa_table[y1]) - 1):
                    # 如果两个节点都可以跳向同一个节点，则两个节点可以归为一类，则tag设为相同的并跳出循环
                    if dfa_table[y1][x] == dfa_table[y2][x] and dfa_table[y1][x] != []:
                        dfa_table[y2][-1] = dfa_table[y1][-1]
                        find = True
                        break
            # 找到了相同状态的节点，跳出循环
            if find:
                find = False
                break


# 将分割好的dfa表进行转化
def transform(dfa_table):
    state_number, state = get_state_number(dfa_table)
    # 用来标记要转换成的节点号码
    index = 1
    # 用来存储转换的节点号
    trans_point = [[] for i in range(len(state))]
    # 进行转换，每一轮转换一个状态，先得到拥有这个状态的节点号。再将这个节点号进行重新命名，重复的行数在下一步操作再进行删除
    for i in state:
        # 得到该轮需要转换的节点
        for a in dfa_table:
            if a[-1][0] == i:
                trans_point[index - 1].append(a[0][0])
        trans_point[index - 1].append(index)
        index += 1
    # 根据等到的节点的转换表
    for i in range(0, len(trans_point)):
        # 对dfa中每个节点进行号码替换
        for a in dfa_table:
            for x in range(0, len(a) - 1):
                if a[x] != []:
                    # 查看节点在没在这轮的转换列表中，在则进行转换，不在则跳过
                    if a[x][0] in trans_point[i]:
                        if trans_point[i].index(a[x][0]) != len(trans_point[i]) - 1:
                            a[x][0] = trans_point[i][-1]

    # 删除表中的重复状态和末尾用来分组的tag
    for i in range(0, len(dfa_table))[::-1]:
        for a in range(0, len(dfa_table))[::-2]:
            if dfa_table[i - 1] == dfa_table[i]:
                del dfa_table[i - 1]
                break
        if i == 0:
            break
    for i in dfa_table:
        del i[-1]


# 得到分割后的dfa表拥有的状态数
def get_state_number(dfa_table):
    cache = []
    count = 0
    for i in dfa_table:
        if i[-1][0] not in cache:
            cache.extend(i[-1])
            count += 1
    return count, cache


def simplify(dfa_table, normal, end):
    # 因为每个dfa表的一行最开始为起始节点，所以用该点作为这一行的标记，以便后面进行分割
    add_tag(dfa_table)

    # 进行dfa最小化分割
    sectionalization(dfa_table, normal, end)

    # 进行最后的转化
    transform(dfa_table)

    return dfa_table


if __name__ == '__main__':
    # 测试用数据初始化dfa表
    dfa_table = [[[] for col in range(6)] for row in range(7)]
    dfa_table[0] = [[1], [3], [2], [], []]
    dfa_table[1] = [[2], [4], [2], [], []]
    dfa_table[2] = [[3], [], [6], [3], [5]]
    dfa_table[3] = [[4], [], [7], [3], [5]]
    dfa_table[4] = [[5], [4], [], [], []]
    dfa_table[5] = [[6], [], [6], [], []]
    dfa_table[6] = [[7], [], [6], [], []]

    # 测试用数据，用来记录终态和非终态的状态
    normal = [1, 2, 3, 4, 5]
    end = [6, 7]

    # 因为每个dfa表的一行最开始为起始节点，所以用该点作为这一行的标记，以便后面进行分割
    add_tag(dfa_table)

    # 进行dfa最小化分割
    sectionalization(dfa_table, normal, end)

    # 进行最后的转化
    transform(dfa_table)

    print(dfa_table)
