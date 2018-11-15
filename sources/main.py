import Re_to_NFA
import NFA_to_DFA
import DFA_simplify

if __name__ == '__main__':
    # 测试的(ab)*|bb和((ab)*|bb)*都可以
    re = "(ab)*|bb"
    print("输入的正则的表达式:")
    print(re)
    # 正则表达式构建NFA，这里所使用的正则表达式是最简单的那种，只有连接、闭包和或运算
    nfa = Re_to_NFA.build_NFA(re)
    print("得到的NFA:")
    print(nfa)
    # NFA转DFA，结果以list保存
    # 最后输出的格式是 (起始节点 通过a跳转到的节点 通过b跳转到的节点)
    dfa, normal, end = NFA_to_DFA.translate(nfa)
    print("得到的DFA:")
    print(dfa)
    # dfa化简
    dfa = DFA_simplify.simplify(dfa, normal, end)
    print("经过DFA最简化后:")
    print(dfa)
