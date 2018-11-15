import copy

# 用来防止进入死循环状态
break_loop = []


# 返回NFA中有几种转移条件
def get_x(nfa):
    count = 0
    temp = []
    for i in nfa:
        if i[1] not in temp:
            count += 1
            temp.append(i[1])
    return count


# 返回nfa中有几个节点
def get_y(nfa):
    max = 0
    for i in nfa:
        if int(i[0]) > max:
            max = int(i[0])
        elif int(i[2]) > max:
            max = int(i[2])
    return max - 1


# 初始化状态转换表
def ini_state_table(nfa):
    # 初始化二维数组
    state_table_x = get_x(nfa)
    state_table_y = get_y(nfa)
    state_table = [[[] for col in range(state_table_x)] for row in range(state_table_y + 1)]

    # 填充转换表中的下一个跳转元素
    for x in range(0, state_table_y + 1):
        for i in nfa:
            if int(i[0]) == x + 1:
                if i[1] == 'a':
                    state_table[x][0].append(i[2])
                elif i[1] == 'b':
                    state_table[x][1].append(i[2])
                elif i[1] == 'null':

                    if state_table[x][2] == []:
                        state_table[x][2].append(i[2])
                    elif state_table[x][2] == 'null' and i[2] != 'null':
                        state_table[x][2].append(i[2])
                    else:
                        state_table[x][2].append(i[2])
    # 没有元素的list说明没有跳转的地方，用null填充
    for y in range(0, len(state_table)):
        for x in range(0, len(state_table[y])):
            if state_table[y][x] == []:
                state_table[y][x] = 'null'
    return state_table


# 构建E-closure表
def build_E_closure(state_table, nfa):
    state_table_y = get_y(nfa)
    ctable = [[] for i in range(state_table_y + 1)]

    for i in range(0, state_table_y + 1):
        x = get_all_state(state_table, i, i)
        x = list(set(x))
        x.sort()
        ctable[i] = x
        break_loop = []

    # 测试用数据,该数据为网上找到的数据，经过验证代码输出是正确的代码输出
    # ctable[0] = [1, 2, 4, 5, 8]
    # ctable[1] = [2, 3, 5]
    # ctable[2] = [3]
    # ctable[3] = [2, 3, 4, 5, 7, 8]
    # ctable[4] = [5]
    # ctable[5] = [2, 3, 5, 6, 7, 8]
    # ctable[6] = [2, 3, 5, 7, 8]
    # ctable[7] = [8]
    # ctable[8] = [9]
    # ctable[9] = [10]
    #
    # state_table[0] = ['null', 'null']
    # state_table[1] = ['null', 'null']
    # state_table[2] = [[4], 'null']
    # state_table[3] = ['null', 'null']
    # state_table[4] = ['null', [6]]
    # state_table[5] = ['null', 'null']
    # state_table[6] = ['null', 'null']
    # state_table[7] = [[9], 'null']
    # state_table[8] = ['null', [10]]
    # state_table[9] = ['null', 'null']

    end_point = len(state_table)
    # Dfa表
    Dfa_table = []
    # 用于记录产生的新状态，但还没进行ab查询，作栈使用
    wait = []
    # 用于记录每一次跳转到的状态
    cache = []
    # 标记当前是以哪个list作为标识
    index = 0
    Dfa_table.append([ctable[0], [], []])

    while (True):
        # a的时候跳向哪些节点

        for a in range(0, len(ctable)):
            if state_table[a][0] != 'null' and a + 1 in Dfa_table[index][0]:
                cache.extend(state_table[a][0])
        # cache不为空，说明有可以从a到达的节点

        if cache != []:
            for a in cache:
                Dfa_table[index][1].extend(ctable[a - 1])
                Dfa_table[index][1] = list(set(Dfa_table[index][1]))
                Dfa_table[index][1].sort()
        if Dfa_table[index][1] != [] and isExist(Dfa_table, Dfa_table[index][1]) == False and wait.count(
                Dfa_table[index][1]) == 0:
            wait.append(Dfa_table[index][1])

        # b的时候跳向哪些节点
        cache = []
        for a in range(0, len(ctable)):
            if state_table[a][1] != 'null' and a + 1 in Dfa_table[index][0]:
                cache.extend(state_table[a][1])
        # cache不为空，说明有可以从b到达的节点
        if cache != []:
            for a in cache:
                Dfa_table[index][2].extend(ctable[a - 1])
                Dfa_table[index][2] = list(set(Dfa_table[index][2]))
                Dfa_table[index][2].sort()
        # 如果这个状态是第一次出现，进行入栈等待操作
        if Dfa_table[index][2] != [] and isExist(Dfa_table, Dfa_table[index][2]) == False and wait.count(
                Dfa_table[index][2]) == 0:
            wait.append(Dfa_table[index][2])

        # 如果此时栈为空，则跳出
        cache = []
        if len(wait) == 0:
            break
        else:
            index += 1
            Dfa_table.append([wait.pop(0), [], []])
    return Dfa_table, end_point


def isExist(table, new):
    for i in table:
        if i[0] == new:
            return True
    return False


# 使用递归求出所有状态
def get_all_state(state_table, ini_start, start):
    output = []
    temp = []
    temp.append(start + 1)
    # 若该节点无后继节点，则直接返回
    if state_table[start][2] == 'null':
        return temp
    # 查看该节点是否已经经过了，防止进入死循环
    if start + 1 in break_loop:
        return temp
    break_loop.append(start + 1)
    if len(state_table[start][2]) >= 1:
        for a in range(0, len(state_table[start][2])):
            x = get_all_state(state_table, ini_start, state_table[start][2][a] - 1)
            if type(x) == int:
                temp.append(x)
            else:
                temp.extend(x)
            output.extend(temp)

    return output


# 将于集合表示的DFA各个节点改用字母表示
def simplify_dfa(dfa):
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
             'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    cache = []
    for i in range(len(dfa)):
        for a in range(len(dfa[i])):
            if dfa[i][a] not in cache and dfa[i][a] != []:
                cache.append(dfa[i][a])

    # 深拷贝cache
    cache = copy.deepcopy(cache)
    # 得到字母到集合的映射
    for i in range(0, len(cache)):
        for a in dfa:
            for b in a:
                if b != []:
                    if b == cache[i] and alpha[i] not in b:
                        b.append(alpha[i])

    # 删除多余元素
    for i in range(0, len(dfa))[::-1]:
        for a in range(0, len(dfa[i]))[::-1]:
            for b in range(0, len(dfa[i][a]))[::-1]:
                if dfa[i][a][b] not in alpha and dfa[i][a][b] != []:
                    del dfa[i][a][b]


# 将于集合表示的DFA各个节点改用单个数字表示
def simplify_dfa_two(dfa, end_point):
    temp = []
    index = 1
    # 用来标记非终端节点和中断节点
    normal = []
    end = []
    for a in range(0, len(dfa)):
        temp = dfa[a][0]
        for b in range(0, len(dfa)):
            for c in range(0, len(dfa[b])):

                # 用来标记终端和非终端节点
                if dfa[b][c] == temp and end_point in dfa[b][c] and index not in end:
                    end.append(index)
                elif dfa[b][c] == temp and end_point in dfa[b][c] and index in end:
                    dfa[b][c] = [index]
                    break
                elif a != len(dfa) - 1 and end_point not in dfa[b][c] and index not in end and index not in normal:
                    normal.append(index)
                if dfa[b][c] == temp:
                    dfa[b][c] = [index]
        index += 1
    return normal, end


def translate(nfa):
    # 初始化状态转移表
    state_table = ini_state_table(nfa)
    # 构建E_closure转移表
    dfa, end_point = build_E_closure(state_table, nfa)
    # 简化dfa表，用单个数字代替list
    normal, end = simplify_dfa_two(dfa, end_point)
    return dfa, normal, end
