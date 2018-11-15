# 表示NFA节点的全局序号
NFA_ID = 1
# 存储作为最后结果的NFA
OUTPUT_NFA = []


class NFA:
    def __init__(self, id, chr, head=False, trail=False):
        # NFA节点的序号
        self.id = id
        # NFA节点的下一个节点
        self.next = []
        # NFA节点的上一个节点
        self.pre = []
        # NFA节点拥有的符号
        self.chr = chr
        # NFA是否拥有两个下一个节点
        self.twoflag = False
        # 判断是否为头或尾
        self.head = head
        self.trail = trail
        # 判断下一节点是否是在自己之前的节点
        self.elder = False

    def link_next(self, next_chr, next_nfa):
        self.next.append([next_chr, next_nfa])


# 将后缀表达式转化为NFA
def Transform_NFA(a_str):
    global NFA_ID
    # 用作存储操作数的栈
    operand = []
    for s in a_str:
        if s not in ['.', '*', '|']:
            operand.append(NFA(NFA_ID, s))
            NFA_ID += 1
            continue
        else:
            # 连接操作
            if s == '.':
                operand2 = operand.pop()
                operand1 = operand.pop()
                # 当操作数都为单节点的时候
                if operand2.next == [] and operand1.next == []:
                    operand2.link_next(operand2.chr, NFA(NFA_ID, 'null', False, True))
                    NFA_ID += 1

                if operand1.next != [] and operand2.next == []:
                    x = operand1
                    while (True):
                        if x.trail == True:
                            operand2.trail = True
                            x.trail = False
                            x.link_next(operand2.chr, operand2)
                            break
                        else:
                            x = x.next[0][1]

                if (operand1.trail != True):
                    operand1.head = True
                    operand1.trail = False

                operand1.link_next(operand1.chr, operand2)
                operand.append(operand1)

            # 或运算
            if s == '|':

                temp1 = operand2 = operand.pop()
                temp2 = operand1 = operand.pop()
                if temp1.next == [] and temp2.next == []:
                    temp1.link_next(temp1.chr, NFA(NFA_ID, 'null', False, True))
                    NFA_ID += 1
                    temp2.link_next(temp2.chr, NFA(NFA_ID, 'null', False, True))
                    NFA_ID += 1
                # 添加尾节点
                while (True):
                    if temp1.trail == True:
                        temp1.trail = False
                        new_end = NFA(NFA_ID + 1, 'null', False, True)
                        temp1.link_next('null', new_end)
                        break
                    if temp1.next != []:
                        temp1 = temp1.next[0][1]
                    else:
                        break

                # 添加尾节点
                while (True):
                    if temp2.trail == True:
                        temp2.trail = False
                        temp2.link_next('null', new_end)
                        break
                    if temp2.next != []:
                        temp2 = temp2.next[0][1]
                    else:
                        break

                # 添加新的起始节点
                # 本来是应该新的头节点比新的尾节点大1，但由于我这里为了方便操作先添加了尾节点，但添加尾节点后NFA_ID没有加1，
                # 所以这里添加了头结点后直接加2，补上了尾节点没加的1
                new_start = NFA(NFA_ID, 'null', True, False)
                NFA_ID += 2
                new_start.twoflag = True
                operand1.head = False
                operand2.head = False
                new_start.link_next('null', operand1)
                new_start.link_next('null', operand2)
                operand.append(new_start)

            # 闭包运算
            if s == '*':
                x = operand.pop()
                if x.next == []:
                    x.link_next(x.chr, NFA(NFA_ID, 'null', False, True))
                    x.head = True
                    NFA_ID += 1
                # 添加新的起始起点和末尾节点
                while (True):
                    if x.head == True:
                        # print("head %s"%(x.id))
                        x.head = False
                        new_head_NFA = NFA(NFA_ID, 'null', True)
                        NFA_ID += 1
                        new_head_NFA.link_next('null', x)
                        x = new_head_NFA.next[0][1]
                    if x.trail == True:
                        # print("trail %s" % (x.id))
                        x.trail = False
                        new_end_NFA = NFA(NFA_ID, 'null', False, True)
                        x.link_next('null', new_end_NFA)
                        NFA_ID += 1
                        new_head_NFA.link_next('null', new_end_NFA)
                        new_head_NFA.twoflag = True
                        operand.append(new_head_NFA)
                        break
                    # 判断是否到达末尾节点
                    if x.next != []:
                        x = x.next[0][1]
                    else:
                        operand.append(new_head_NFA)
                        break
                x = operand.pop()

                # 闭包运算添加回环箭头
                while (True):

                    if x.head == True:
                        start_NFA = x
                        loop_start = x.next[0][1]
                        # print("%s %s"%(x.id,x.next[0][1].id))

                    if x.next[0][1].trail == True:
                        x.twoflag = True
                        x.link_next('null', loop_start)
                        x.elder = True
                        operand.append(start_NFA)
                        break

                    if x.next != []:
                        x = x.next[0][1]
                    else:
                        operand.append(start_NFA)
                        break

    # show_NFA(operand)
    # 以list存储NFA结构
    outputNFA(operand)
    return operand


# 将最后得到的结果以List方式保存下来，以便查看
def outputNFA(operand):
    # 初始化暂存变量temp
    temp = 0
    NFA_out = []
    for e in range(0, len(operand)):
        for i in range(0, 100):
            if i == 0:
                temp = operand[e]
            elif temp.next != []:
                temp = temp.next[0][1]
            else:
                break
            if temp.next != []:
                NFA_out.append(temp.id)
                NFA_out.append(temp.next[0][0])
                NFA_out.append(temp.next[0][1].id)
                # 查看是否已经存在该记录,存在则不进行保存操作
                if isAlreadyExist(NFA_out) == False:
                    OUTPUT_NFA.append(NFA_out)
                    NFA_out = []
            if (temp.twoflag):
                NFA_out.append(temp.id)
                NFA_out.append(temp.next[1][0])
                NFA_out.append(temp.next[1][1].id)
                # 查看是否已经存在该记录,存在则不进行保存操作
                if isAlreadyExist(NFA_out) == False:
                    OUTPUT_NFA.append(NFA_out)
                    NFA_out = []
                if (temp.elder == False):
                    next = []
                    next.append(temp.next[1][1])
                    outputNFA(next)
            NFA_out = []


# 查看该元组是否已经存在
def isAlreadyExist(new):
    for i in OUTPUT_NFA:
        if i[0] == new[0] and i[1] == new[1] and i[2] == new[2]:
            return True

    return False


def show_NFA(operand):
    # 初始化暂存变量temp
    temp = 0

    for e in range(0, len(operand)):
        for i in range(0, 100):
            if i == 0:
                temp = operand[e]
            elif temp.next != []:
                temp = temp.next[0][1]
            else:
                break
            if temp.next != []:
                print("%s " % (temp.id), end="")
                print("%s %s" % (temp.next[0][0], temp.next[0][1].id))
            if (temp.twoflag):
                print("%s " % (temp.id), end="")
                print("%s %s" % (temp.next[1][0], temp.next[1][1].id))
                if (temp.elder == False):
                    next = []
                    next.append(temp.next[1][1])
                    show_NFA(next)


# 正则表达式优先级
ops_rule = {
    '|': 1,
    '*': 3,
    '.': 2
}


# 中缀转后缀表达式
def middle_to_after(s):
    expression = []
    ops = []
    for item in range(0, len(s)):
        if s[item] in ['|', '*', '.']:
            while len(ops) >= 0:
                if len(ops) == 0:
                    ops.append(s[item])
                    break
                op = ops.pop()
                if op == '(' or ops_rule[s[item]] > ops_rule[op]:
                    ops.append(op)
                    ops.append(s[item])
                    break
                else:
                    expression.append(op)
        elif s[item] == '(':
            ops.append(s[item])
        elif s[item] == ')':
            while len(ops) > 0:
                op = ops.pop()
                if op == '(':
                    break
                else:
                    expression.append(op)
        else:
            expression.append(s[item])

    while len(ops) > 0:
        expression.append(ops.pop())

    return expression


# 补齐连接符号，用.来表示连接符号，方便后面的中缀表达式转后缀表达式
def Re_to_NeRe(string):
    alpha = "abcdefghijklmnopgrstuvwxyz"
    output = ""
    for i in range(0, len(string) - 1):
        if string[i] in alpha and string[i + 1] in alpha:
            output += string[i]
            output += "."
        elif string[i] in alpha and string[i + 1] == "(":
            output += string[i]
            output += "."
        elif string[i] == '*' and string[i + 1] in alpha:
            output += string[i]
            output += "."
        else:
            output += string[i]
    output += string[-1]
    return output


def build_NFA(re):
    # 将输入的正则表达式转为补齐连接操作的正则表达式
    # "b((ab)*|bb)*ab"
    str_Ne = Re_to_NeRe(re)
    # 中缀转为后缀表达式
    after_exp = middle_to_after(str_Ne)
    # print(after_exp)
    NFA = Transform_NFA(after_exp)
    return OUTPUT_NFA


if __name__ == '__main__':
    # 将输入的正则表达式转为补齐连接操作的正则表达式
    str_Ne = Re_to_NeRe("((ab)*|bb)*")
    # 中缀转为后缀表达式
    after_exp = middle_to_after(str_Ne)
    print(after_exp)
    # print(after_exp)
    NFA = Transform_NFA(after_exp)
    show_NFA(NFA)
