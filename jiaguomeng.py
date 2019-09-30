# -*- coding: utf-8 -*-
import json
import itertools
import unicodedata
from queue import PriorityQueue as PQ

#可选:将数据直接填在文件中
JsonData={

}
#从文件读取数据
if len(JsonData)==0:
    with open('data.txt','r',encoding='utf8') as JsonFile:
        JsonData=json.load(JsonFile)

commercial = '便利店 五金店 服装店 菜市场 学校 图书城 商贸中心 加油站 民食斋 媒体之声'
residence = '木屋 居民楼 钢结构房 平房 小型公寓 人才公寓 花园洋房 中式小楼 空中别墅 复兴公馆'
industry  = '木材厂 食品厂 造纸厂 水厂 电厂 钢铁厂 纺织厂 零件厂 企鹅机械 人民石油'

#一对多buff
bufflist_246 = [.2, .4, .6, .8, 1.0]
bufflist_005 = [0.25*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_010 = [0.5*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_015 = [0.75*x for x in [.2, .4, .6, .8, 1.0]]
bufflist_035 = [1.75*x for x in [.2, .4, .6, .8, 1.0]]
buffs_global = {
    '人才公寓': bufflist_246,
    '媒体之声': bufflist_005,
    '企鹅机械': bufflist_010,
}
buffs_online ={
    '中式小楼': bufflist_246,
    '空中别墅':bufflist_010,
    '民食斋': bufflist_246,
    '电厂': [.2, .5, .8, 1.1, 1.4],
}
buffs_offline ={
    '复兴公馆':bufflist_010,
    '加油站':bufflist_010,
    '媒体之声': bufflist_015,
    '水厂': [.1,.15,.2,.25,.3],
    '人民石油': bufflist_010,
}
buffs_commercial = {
    '纺织厂': bufflist_015,
}
buffs_residence = {
    '平房': bufflist_246,
    '中式小楼': bufflist_035,
}
buffs_industry = {
    '人才公寓': bufflist_015,
    '钢铁厂': bufflist_015,
}

LastResult=JsonData['LastResult']

Mode=JsonData['Mode']
Policy = JsonData['Policy']
Photos = JsonData['Photos']

BlackList=set()
if Mode == 'Online':
    BlackList=set(' 小型公寓 复兴公馆 水厂'.split())
    Policy['Global']=Policy['Online']
    Photos['Global']=Photos['Online']
    buffs_commercial={**buffs_global,**buffs_online,**buffs_commercial}
    buffs_residence={**buffs_global,**buffs_online,**buffs_residence}
    buffs_industry={**buffs_global,**buffs_online,**buffs_industry}
elif Mode == 'Offline':
    BlackList=set(' 小型公寓 电厂'.split())
    Policy['Global']=Policy['Offline']
    Photos['Global']=Photos['Offline']
    buffs_commercial={**buffs_global,**buffs_offline,**buffs_commercial}
    buffs_residence={**buffs_global,**buffs_offline,**buffs_residence}
    buffs_industry={**buffs_global,**buffs_offline,**buffs_industry}

star = {}
Builds=JsonData['Builds']
ListDifference=lambda a,b: [item for item in a if not item in b]
for key in Builds:
    Builds[key]=ListDifference(Builds[key].split(),BlackList)
    for item in Builds[key]:
        star[item]=int(key)
AllBuild=Builds['1']+Builds['2']+Builds['3']+Builds['4']+Builds['5']
commercial=ListDifference(commercial.split(),BlackList)
residence=ListDifference(residence.split(),BlackList)
industry=ListDifference(industry.split(),BlackList)
#只取需要的建筑
ListIntersection=lambda a,b: [item for item in a if item in b]
commercial=ListIntersection(commercial,AllBuild)
residence=ListIntersection(residence,AllBuild)
industry=ListIntersection(industry,AllBuild)

startDict = {1:1, 2:2, 3:6, 4:24, 5:120}
start = {}
for item in commercial:#商业
    start[item] = startDict[star[item]]*\
        (1+Policy['Global']+Policy['Commercial'])*\
        (1+Photos['Global']+Photos['Commercial'])
for item in residence:#住宅
    start[item] = startDict[star[item]]*\
        (1+Policy['Global']+Policy['Residence'])*\
        (1+Photos['Global']+Photos['Residence'])
for item in industry:#工业
    start[item] = startDict[star[item]]*\
        (1+Policy['Global']+Policy['Industry'])*\
        (1+Photos['Global']+Photos['Industry'])

#收益调整
native_buff={
    '花园洋房':1.022,
    '商贸中心':1.022,
    '平房':1.097,
    '电厂':1.18,
    '水厂':1.26,
    '加油站':1.2,
    '企鹅机械':1.33,
    '人才公寓':1.4,
    '中式小楼':1.4,
    '民食斋':1.52,
    '空中别墅':1.52,
    '媒体之声':1.615,
}

for item in start:
    if item in native_buff:
        start[item]*=native_buff[item]

Mission=JsonData['Mission']
for TryMode in ['Online','Offine']:
    if TryMode in Mission:
        if TryMode==Mode:
            for item in AllBuild:
                Mission[item]=Mission.get(item,0)+Mission[Mode]
        Mission.pop(TryMode)
for key,value in {'住宅':residence,'商业':commercial,'工业':industry}.items():
    if key in Mission:
        for item in value:
            Mission[item]=Mission.get(item,0)+Mission[key]
        Mission.pop(key)
for key,value in Mission.items():
    if key in AllBuild:
        start[key]*=1+value

buffs_100 = {
    '木屋': ['木材厂'],
    '居民楼': ['便利店'],
    '钢结构房': ['钢铁厂'],
    '花园洋房': ['商贸中心'],
    '空中别墅': ['民食斋'],
    '便利店': ['居民楼'],
    '五金店': ['零件厂'],
    '服装店': ['纺织厂'],
    '菜市场': ['食品厂'],
    '学校':  ['图书城'],
    '图书城': ['学校', '造纸厂'],
    '商贸中心': ['花园洋房'],
    '木材厂': ['木屋'],
    '食品厂': ['菜市场'],
    '造纸厂': ['图书城'],
    '钢铁厂': ['钢结构房'],
    '纺织厂': ['服装店'],
    '零件厂': ['五金店'],
    '企鹅机械':['零件厂'],
    '人民石油':['加油站'],
}

buffs_50 = {
    '零件厂': ['企鹅机械'],
    '加油站': ['人民石油'],
}

def calculateComb(buildings):
    buildtuple = buildings[0] + buildings[1] + buildings[2]
    starts = [start[x] for x in buildtuple]
    results = [1] * 9
    for item in buildtuple:
        if item in buffs_100:
            for buffed in buffs_100[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item]
        if item in buffs_50:
            for buffed in buffs_50[item]:
                if buffed in buildtuple:
                    results[buildtuple.index(buffed)] += star[item]*0.5
        if item in buffs_commercial:
            toAdd = buffs_commercial[item][star[item]-1]
            results[0] += toAdd
            results[1] += toAdd
            results[2] += toAdd
        if item in buffs_industry:
            toAdd = buffs_industry[item][star[item]-1]
            results[3] += toAdd
            results[4] += toAdd
            results[5] += toAdd
        if item in buffs_residence:
            toAdd = buffs_residence[item][star[item]-1]
            results[6] += toAdd
            results[7] += toAdd
            results[8] += toAdd
    return (sum([v*results[i] for i, v in enumerate(starts)]),
            [v*results[i]/startDict[star[buildtuple[i]]] for i, v in enumerate(starts)])

results = PQ()
class Result(object):
    def __init__(self, priority, builds):
        self.priority = priority
        self.builds = builds
        return
    def __lt__(self, other):
        return self.priority < other.priority
    def __eq__(self, other):
        return self.priority == other.priority

if Mode=='Online' or Mode=='Offline':
    search_space=list(itertools.product(itertools.combinations(residence, 3), itertools.combinations(commercial, 3), itertools.combinations(industry, 3)))
    search_space_size=len(search_space)
    print('Total iterations:', search_space_size)
    try:
        from tqdm import tqdm
        for item in tqdm(search_space,total=search_space_size,ncols=80):
            prod = calculateComb(item)
            results.put(Result(-prod[0], (item, prod[1])))
    except Exception:
        # raise Exception
        import time,sys
        LastTime=time.time()
        for index in range(search_space_size):
            if(time.time()-LastTime>0.1):
                sys.stdout.write('\r'+str(round(index/search_space_size*100))+'%|'+'█'*round(index/search_space_size*60)+' '*round((1-index/search_space_size)*60)+'|'+str(index)+'/'+str(search_space_size))
                LastTime=time.time()
            prod = calculateComb(search_space[index])
            results.put(Result(-prod[0], (search_space[index], prod[1])))

def printTable(content):
    def strwid(string):
        return sum(
            2 if unicodedata.east_asian_width(char) in {'W', 'F' and 'A'}
            else 1
            for char in string
        )
    widths = [max(strwid(cell) for cell in col) for col in zip(*content)]
    for row in content:
        printed_cells = (
            ' ' * (width - strwid(cell)) + cell
            for cell, width in zip(row, widths)
        )
        print(' | '.join(printed_cells))

layout, scores = results.get().builds
layout_list = [cell for row in layout for cell in row]
priorities = [x*startDict[star[layout_list[i]]] for i, x in enumerate(scores)]
printTable([
    ['#'] + ['{}'.format(d) for d in range(9)],
    ['最优策略'] + layout_list,
    ['各建筑加成倍率'] + ['{:.2f}'.format(score) for score in scores],
    ['升级优先级'] + ['{:.2f}'.format(priority) for priority in priorities],
])
print('总加成倍率：{:.2f}'.format(sum(priorities)))

def getNext():
    print('==============')
    layout, scores = results.get().builds
    layout_list = [cell for row in layout for cell in row]
    priorities = [x*startDict[star[layout_list[i]]] for i, x in enumerate(scores)]
    printTable([
        ['#'] + ['{}'.format(d) for d in range(9)],
        ['次优策略'] + layout_list,
        ['各建筑加成倍率'] + ['{:.2f}'.format(score) for score in scores],
        ['升级优先级'] + ['{:.2f}'.format(priority) for priority in priorities],
    ])

if len(LastResult)==3:
    now_result=[list(item) for item in layout]
    for class_num in range(3):
        for item in LastResult[class_num][:]:
            if item in now_result[class_num]:
                LastResult[class_num].remove(item)
                now_result[class_num].remove(item)
    print(LastResult,'被')
    print(now_result,'替换')

def argsort(x):
    x=[(index,x[index]) for index in range(len(x))]
    x=sorted(x,key=lambda x:x[1])
    x=[item[0] for item in x]
    return x
upgrade_order=argsort(priorities)[::-1]
print('升级顺序:\n({})'.format(', '.join(
    layout_list[i] for i in upgrade_order
)))
# print('(',end='')
# for item in upgrade_order[:-1]:
#     print(item,',',sep='',end='')
# print(upgrade_order[-1],')',sep='')
