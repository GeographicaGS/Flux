# coding=UTF8

a = [[1,2,3],[1,2],[1,2],[2,4],[1,2,3]]
c = []

[c.append(x) for x in a if x not in c]
