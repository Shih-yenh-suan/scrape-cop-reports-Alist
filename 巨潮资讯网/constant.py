URL = 'http://www.cninfo.com.cn/new/hisAnnouncement/query'
HEADERS = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Content-Length': '181',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Host': 'www.cninfo.com.cn',
    'Origin': 'http://www.cninfo.com.cn',
    'Referer': 'http://www.cninfo.com.cn/new/commonUrl/pageOfSearch?url=disclosure/list/search',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest'}
TRADE = ['农、林、牧、渔业', '电力、热力、燃气及水生产和供应业', '交通运输、仓储和邮政业',
         '金融业', '科学研究和技术服务业', '教育', '综合', '采矿业', '建筑业', '住宿和餐饮业',
         '房地产业', '水利、环境和公共设施管理业', '卫生和社会工作', '制造业', '批发和零售业',
         '信息传输、软件和信息技术服务业', '租赁和商务服务业', '居民服务、修理和其他服务业', '文化、体育和娱乐业']

DATA = {
    'pageNum': '',
    'pageSize': 30,
    'column': '',
    'tabName': 'fulltext',
    'plate': '',
    'stock': '',
    'searchkey': '',
    'secid': '',
    'category': '',
    'trade': '',
    'seDate': '',
    'sortName': '',
    'sortType': '',
    'isHLtitle': 'true'
}
STOP_WORDS_DICT = {
    "normal_sw":  ['摘要',
                   '英文',
                   '回复',
                   '细则',
                   '基金',
                   '已取消',
                   '延迟',
                   '提示',
                   '意见',
                   '季度',
                   'eport',
                   '财务指标',
                   '说明',
                   '管理办法',
                   '半年',
                   '半<em>年',
                   '制度',
                   '变更',
                   '表格',
                   '设立',
                   '规则',
                   '签字页',
                   '决议公告',
                   '纲要',
                   '鉴证',
                   '内部控制',
                   '审计',
                   '审核',
                   '债券',
                   '自查',
                   '声明',
                   '整改',
                   '回函',
                   '更正前',
                   '更正公告',
                   '差错更正',
                   '更新前',
                   '修正公告',
                   '修订公告',
                   '更正披露',
                   '更正事项',
                   '专项活动',
                   '方案',
                   '研究报告',
                   '检查',
                   '核查',
                   '补充资料',
                   '补充披露',
                   '补充公告',
                   '补充说明',
                   '补充报告',
                   '的公告',
                   '社会公众',
                   '有限责任',
                   '担保',
                   '责任主体',
                   '季度',
                   '中期',
                   '章程',
                   '意见',
                   '预案',
                   '异常波动',
                   '进展',
                   '资产评估',
                   '督导培训',
                   '规划',
                   '备忘录',
                   '强制停牌',
                   '无法',
                   '不能',
                   '延期',
                   '规程'],
    "zhaogu_sw": ['提示',
                  '附录',
                  '关于',
                  '虚假',
                  '增发',
                  '摘要',
                  '确认',
                  '澄清',
                  '更正公告',
                  '补充公告',
                  '已取消'],
    "yugao_sw":  ['摘要',
                  '英文',
                  '回复',
                  '细则',
                  '基金',
                  '已取消',
                  '延迟',
                  '意见',
                  'eport',
                  '财务指标',
                  '管理办法',
                  '制度',
                  '表格',
                  '设立',
                  '规则',
                  '签字页',
                  '决议公告',
                  '纲要',
                  '鉴证',
                  '内部控制',
                  '审计',
                  '审核',
                  '债券',
                  '自查',
                  '声明',
                  '整改',
                  '回函',
                  '更正前',
                  '更正公告',
                  '差错更正',
                  '更新前',
                  '修正公告',
                  '修订公告',
                  '更正披露',
                  '更正事项',
                  '专项活动',
                  '方案',
                  '研究报告',
                  '检查',
                  '核查',
                  '补充资料',
                  '补充披露',
                  '补充公告',
                  '补充说明',
                  '补充报告',
                  '社会公众',
                  '有限责任',
                  '担保',
                  '责任主体',
                  '章程',
                  '意见',
                  '预案',
                  '异常波动',
                  '进展',
                  '资产评估',
                  '督导培训',
                  '规划',
                  '备忘录',
                  '强制停牌',
                  '无法',
                  '不能',
                  '延期',
                  '规程'],
    "wenxun_sw": ['延期', '提示'],
    "quarter_sw": ['摘要',
                   '报表',
                   '业绩',
                   'eport',
                   '更正的公告',
                   '预告',
                   '审阅',
                   '简报',
                   '更正公告',
                   '补充公告',
                   '补充说明',
                   '业务',
                   '英文',
                   '营数据',
                   '取消'],
}

SEARCH_KEY_LIST = {
    "A股招股书": ['招股说明书', '招股意向书'],
    "A股年报": ['年度报告', '年报'],
    "A股社会责任": ['社会和', '社会及', 'ESG',
               '社会与', '社会责任', '社会企业责任', '社会暨', '社会治理',
               '环境报告书', '环境责任', '环境及治理', '环境管理', '环境报告书',
               '可持续发展'],
    "三板年报": ['年度报告', '年报'],
    "A股问询函": ['问询', '回复', '回函'],
    "A股一季报": ['一季度']
}

CATEGORY_AND_NAME = {
    "A股年报": ['category_ndbg_szsh', 'szse'],
    "A股半年报": ['category_bndbg_szsh', 'szse'],
    "A股一季报": ['category_yjdbg_szsh', 'szse'],
    "A股三季报": ['category_sjdbg_szsh', 'szse'],
    "A股业绩报告": ['category_yjygjxz_szsh', 'szse'],
    "三板年度报告": ['category_dqgg', 'third']
}
