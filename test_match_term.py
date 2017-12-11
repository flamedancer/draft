# -*- coding: utf-8 -*-
import re
from pypinyin import lazy_pinyin

terms_str = u'''
286 400电话
292 400电话办理
327 DIY手工坊
120 IT培训
188 MV拍摄
284 POS机办理
302 VR设备租赁
106 个人搬家
321 个性台历
190 中式婚礼
226 乐器租赁
234 二手回收
173 交通事故律师
248 代办签证
250 代理记账
164 会计/审计
179 会计培训
304 住宅房屋购买
314 住家保姆
251 便民服务
125 保姆
5   保洁开荒
170 债务纠纷
201 假期补习
308 健身器材租赁
219 健身教练
127 催乳师
154 儿童摄影
132 公司保洁
107 公司搬家
249 公司法务
158 公司注册
269 其他国家签证
274 写字楼租赁
153 写真摄影
299 农家乐
316 冰箱回收
263 冰箱维修
156 冲印彩扩
174 刑事律师
191 别墅装修
192 办公室装修
239 办公设备回收
171 劳动纠纷
148 化妆造型
245 医疗纠纷
312 单反相机回收
194 卧室装修
161 印刷
246 合同纠纷
257 咖啡技能培训
155 商业摄影
9   商业服务
195 商业装修
159 商标注册
305 商用房屋购买
253 商铺租赁
162 喷绘招牌
252 国际速运
181 地毯清洗
311 墙面翻新
200 大扫除
240 奢侈品回收
325 娱乐休闲
172 婚姻律师
146 婚宴酒店
7   婚庆典礼
149 婚庆表演
147 婚礼司仪
145 婚礼用品
144 婚礼策划
152 婚纱摄影
150 婚纱礼服
151 婚车租赁
118 学前教育
119 学历教育
275 宠物狗服务
197 客厅装修
193 室内设计
178 室内设计培训
237 家具回收
114 家具拆装
143 家具维修
101 家居装饰
131 家庭保洁
100 家庭装修
4   家政月嫂
301 家政服务
115 家教
345 家电清洗
141 家电维修
166 展会服务
102 工程装修
177 平面设计培训
187 年会策划
196 店面装修
198 庭院设计
133 开荒保洁
142 开锁换锁
262 影音家电维修
282 心理培训
342 快递速运
169 房产纠纷
104 房屋改造
224 房屋租赁
139 房屋维修
244 房屋购买
236 手机回收
220 手机维修
306 投影租赁
2   搬家服务
157 摄影录像
8   摄影摄像
3   教育培训
183 数据恢复
241 数码电子回收
199 新房装修
255 旅游 | 签证
270 日韩旅游
256 日韩签证
105 旧房翻新
343 星巴克
283 暑期夏令营
124 月嫂
338 服装定制
242 服装衣帽回收
331 桌游
268 欧洲签证
184 水务维修
310 水管维修
272 江浙沪周边游
322 汽车改装
287 汽车租赁
227 汽车维修保养
228 汽车美容装饰
223 汽车陪练
303 沙发翻新
298 沪牌代拍
180 油烟机清洗
260 油烟机维修
175 法律援助
10  法律服务
295 洗衣服务
315 洗衣机回收
265 洗衣机维修
271 海岛旅游
320 海报制作
128 涉外家政
329 温泉洗浴
218 游学夏令营
258 游泳培训
267 澳大利亚签证
137 灯具清洗
266 热水器维修
323 烹饪培训
261 燃气灶维修
326 瑜伽培训
341 瓷砖美缝
296 甲醛检测
334 电工服务
235 电脑回收
138 电脑维修
264 电视维修
116 留学
317 病人陪护
339 监控安装
290 短信通道平台
285 短信通道服务
135 石材养护
300 礼仪模特
168 礼品定制
297 礼品鲜花
293 移民服务
247 空调回收
140 空调拆装
182 空调清洗
112 空调移机
294 空调维修
117 管理培训
186 管道疏通
6   维修安装
319 绿植租摆
221 网站建设
160 网络布线
259 美国签证
167 翻译服务
318 老人陪护
123 职业技能培训
130 育婴师
307 自动售货机租赁
324 舞蹈培训
122 艺术培训
176 行李托运
1   装修改造
103 装修设计
109 设备搬迁
163 设备租赁
121 设计培训
165 设计策划
281 语言培训
335 货运服务
110 起重吊装
332 足疗按摩
330 跆拳道培训
344 跑腿代办
328 轰趴馆
333 配镜
243 金银回收
126 钟点工
111 钢琴搬运
222 钢琴教练
313 镜头回收
108 长途搬家搬运
309 门窗维修
185 防水补漏
134 除虫除蚁
129 陪护
136 高空清洗
340 麻将机维修
'''
words = {}
pinyins = {}
terms = {}
re_term = re.compile('\s+')
for item in terms_str.split('\n'):
    item = item.strip()
    if not item:
        continue
    id, word = re.split(re_term, item, 1)
    pin = lazy_pinyin(word)
    terms[int(id)] = {
        'repr': word,
        'pin': ''.join([word_pin.capitalize() for word_pin in pin]),
    }
print terms
    
for key, value in terms.items():
    for w in value['repr']:
        words.setdefault(w, set())
        words[w].add(key)

for key in words:
    pin = lazy_pinyin(key)[0]
    for p in pin:
        pinyins.setdefault(p, set())
        print key
        pinyins[p].add(key)
    first_p = pin[0].upper()
    pinyins.setdefault(first_p, set())
    pinyins[first_p].add(key)

def match(inputs): 
    inputs = inputs.capitalize().decode('utf-8')
    match_terms_set = set()
    for p in inputs:
        word_set = set()
        terms_set = set()
        word_set = word_set | pinyins[p]
        for t in word_set:
            terms_set = terms_set | words[t]
        print "*" * 10, terms_set
        if match_terms_set:
            match_terms_set &= terms_set
        else:
            match_terms_set = terms_set
    print "-" * 10, match_terms_set
    for t in match_terms_set:
        print terms[t]['repr']

def sord_weight(inputs, result_term):
    pass
    

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        match(sys.argv[1])
    else:
        match('bj')

