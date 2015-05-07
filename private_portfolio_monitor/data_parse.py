# -*- coding: utf-8 -*- 

import os
from collections import OrderedDict
from datetime import date

import numpy as np

import DataAPI


POSITION_FILE_PATH = "./posdb"
RESOURCE_PATH = "./resources"


def parse_position_string(posstr):
    posstr = posstr.split('\n')
    cash, secpos = float(posstr[0]), [s.split('|') for s in posstr[1:]]
    
    tk2id = lambda x: x+'.XSHG' if x[0]=='6' else x+'.XSHE'
    secpos = {tk2id(tk): float(am) for tk, am in secpos}
    return cash, secpos

def get_minute_bar():
    mb = file(os.path.join(RESOURCE_PATH, 'minute_bar')).readlines()
    return [m.strip() for m in mb]

def get_history_position():
    poslist = os.listdir(POSITION_FILE_PATH)
    poslist = sorted(poslist)[:-1]
    history = OrderedDict()
    for posFile in poslist:
        posDate = posFile.split('.')[0]
        pos = file(os.path.join(POSITION_FILE_PATH, posFile)).read()
        history[posDate] = parse_position_string(pos)
    return history

def get_current_position():
    poslist = os.listdir(POSITION_FILE_PATH)
    newestFile = max(poslist)
    newestDate = newestFile.split('.')[0]

    today = date.today().strftime('%Y%m%d')
    newestPosition = file(os.path.join(POSITION_FILE_PATH, newestFile)).read()
    if newestDate < today:
        fw = open(os.path.join(POSITION_FILE_PATH, today+'.txt'), 'w')
        fw.write(newestPosition)
        fw.close()
    return parse_position_string(newestPosition)

def evaluate(pos, dt):
    cash, secpos = pos
    df = DataAPI.MktEqudGet(secID=secpos.keys(), beginDate=dt, endDate=dt, field=['secID', 'closePrice']) 
    price = dict(zip(df['secID'], df['closePrice']))             
    return cash + sum(am*price[sec] for sec,am in secpos.items()), price

def get_historyline(history):
    tradingdays = history.keys()
    vseries = [evaluate(pos, dt) for dt,pos in history.items()]
    ltcpshot = vseries[-1][-1]
    vseries = [p[0] for p in vseries]
    ini_v = vseries[-1]
    aseries = [v/vseries[0]-1 for v in vseries]
    bseries = DataAPI.MktIdxdGet(indexID='000300.ZICN', beginDate=tradingdays[0], endDate=tradingdays[-1], field=['closeIndex'])['closeIndex'].tolist()
    ini_b = bseries[-1]
    bseries = [b/bseries[0]-1 for b in bseries]
    return (ini_v, ini_b, ltcpshot), (tradingdays, vseries, aseries, bseries)

def get_snapshot(pos, baseinfo):
    # load information
    cash, secpos = pos
    barTime = get_minute_bar()
    
    # get yesterday's info
    ini_v, ini_b, ltcpshot  = baseinfo

    # get today's newest benchmark, portfolio value and securities' prices
    clsp, secname = {}, {}
    for sec in secpos:
        df = DataAPI.MktBarRTIntraDayGet(securityID=sec)
        clsp[sec] = df['closePrice'].tolist()
        secname[sec] = df.at[0, 'shortNM'].decode('utf8')
        if sec not in ltcpshot:
            ltcpshot[sec] = df.at[0, 'openPrice']
    clspshot = {sec:p[-1] for sec,p in clsp.items()}

    vseries = []
    for i in range(len(clsp[sec])):
        v = cash
        for sec, am in secpos.items():
            v += am * clsp[sec][i]
        vseries.append(v)    
    aseries = [v/ini_v-1 for v in vseries]

    cur_t = barTime[len(vseries)-1] 
    cur_v = vseries[-1]
    
    bseries = DataAPI.MktBarRTIntraDayGet(securityID='000300.XSHG')['closePrice'].tolist()
    cur_b = bseries[-1]
    bseries = [b/ini_b-1 for b in bseries]

    # filling with nan    
    for s in [aseries, bseries]:
        s += [np.nan] * (len(barTime) - len(s))
    
    return (cur_t, ini_v, cur_v, ini_b, cur_b), (barTime, aseries, bseries), (secname, secpos, ltcpshot, clspshot)