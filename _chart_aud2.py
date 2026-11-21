
# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
rows = [
 ("11-11 17:45","sell",1.44,"0.68491","11-11 23:30","0.68458",47.52),
 ("11-12 01:45","sell",1.44,"0.68446","11-12 03:06","0.68428",25.92),
 ("11-12 03:45","sell",1.44,"0.68481","11-12 05:10","0.68457",34.56),
 ("11-12 10:15","sell",1.44,"0.68258","11-12 11:00","0.68234",34.56),
 ("11-12 11:45","sell",1.44,"0.68280","11-12 15:22","0.68255",36.00),
 ("11-12 18:30","sell",1.20,"0.68095","11-12 23:30","0.68064",37.20),
 ("11-13 03:15","sell",1.45,"0.68111","11-13 12:15","0.67941",246.53),
 ("11-13 12:30","sell",1.45,"0.67940","11-13 13:31","0.67892",69.60),
 ("11-13 15:15","sell",1.46,"0.67856","11-13 15:30","0.67955",-144.54),
 ("11-13 16:45","sell",1.45,"0.67956","11-13 23:30","0.67737",317.55),
 ("11-16 01:15","sell",1.46,"0.67753","11-16 10:15","0.67559",283.97),
 ("11-16 10:45","sell",1.47,"0.67568","11-16 12:09","0.67547",30.87),
 ("11-16 12:45","sell",1.47,"0.67568","11-16 21:45","0.67371",288.56),
 ("11-16 22:15","sell",1.48,"0.67379","11-16 23:30","0.67362",25.16),
 ("11-17 01:15","sell",1.48,"0.67352","11-17 02:38","0.67335",25.16),
 ("11-17 03:15","sell",1.48,"0.67342","11-17 05:07","0.67440",-145.04),
 ("11-17 10:30","sell",1.48,"0.67371","11-17 11:44","0.67351",29.60),
 ("11-17 12:30","sell",1.48,"0.67378","11-17 16:03","0.67354",35.52),
 ("11-18 07:45","sell",1.48,"0.67226","11-18 10:51","0.67203",34.04),
 ("11-19 01:30","sell",1.48,"0.67137","11-19 07:45","0.66913",330.78),
 ("11-19 20:15","sell",0.92,"0.66644","11-19 23:30","0.66560",77.28),
 ("11-20 01:00","sell",1.25,"0.66549","11-20 06:43","0.66669",-150.00),
 ("11-20 07:45","sell",1.20,"0.66594","11-20 08:10","0.66753",-190.80),
 ("11-20 14:15","sell",1.39,"0.66596","11-20 23:15","0.66237",498.46),
]
def font(size, bold=False):
    paths = [r"C:\Windows\Fonts\msyhbd.ttc", r"C:\Windows\Fonts\msyh.ttc"] if bold else [r"C:\Windows\Fonts\msyh.ttc", r"C:\Windows\Fonts\simhei.ttf"]
    for p in paths:
        try: return ImageFont.truetype(p, size)
        except Exception: pass
    return ImageFont.load_default()
# ---- table image ----
cols = ["开仓时间","类型","手数","开仓价","平仓时间","平仓价","盈亏 USD"]
widths = [120, 70, 70, 90, 120, 90, 100]
rowh = 26; pad = 16
W = sum(widths) + pad*2
H = 78 + rowh*(len(rows)+1) + 40
img = Image.new("RGB",(W,H),"white"); d = ImageDraw.Draw(img)
f_title = font(20); f_head = font(14, True); f_cell = font(13)
d.text((pad,16),"AUDUSD 模拟盘成交记录（2026-11-11 → 11-20，24 笔）",fill="#111827",font=f_title)
d.text((pad,44),"累计 +1,878.46 USD ｜ 胜率 83.3%（20 胜 4 负）｜ 单一品种、单边下跌行情、样本小",fill="#6b7280",font=font(12))
y = 70
x = pad
for i,c in enumerate(cols):
    d.rectangle([x,y,x+widths[i],y+rowh],fill="#f3f4f6",outline="#e5e7eb")
    d.text((x+6,y+6),c,fill="#374151",font=f_head); x += widths[i]
y += rowh
for r in rows:
    x = pad
    vals = [r[0],r[1],f"{r[2]:.2f}",r[3],r[4],r[5],f"{r[6]:+.2f}"]
    for i,v in enumerate(vals):
        d.rectangle([x,y,x+widths[i],y+rowh],outline="#f3f4f6")
        col = "#111827"
        if i==6: col = "#16a34a" if r[6]>=0 else "#dc2626"
        if i==1: col = "#b91c1c"
        d.text((x+6,y+6),v,fill=col,font=f_cell); x += widths[i]
    y += rowh
d.text((pad,H-28),"仅为模拟账户历史记录，不代表未来收益；AUDUSD 未通过策略回测验证（两段回测均为负）。",fill="#b91c1c",font=font(11))
img.save(r"C:\Users\ruaibeite\Desktop\gold\gold-auto-ea-showcase\assets\audusd-trades.png")
# ---- cumulative curve ----
cum=[]; s=0
for r in rows:
    s += r[6]; cum.append(s)
W2,H2 = 900, 420
img2 = Image.new("RGB",(W2,H2),"white"); d2 = ImageDraw.Draw(img2)
d2.text((30,20),"AUDUSD 模拟盘累计盈亏（24 笔）",fill="#1f2937",font=font(24))
d2.text((30,52),f"最终 +{cum[-1]:.2f} USD ｜ 胜率 83.3%",fill="#6b7280",font=font(14))
left,top,right,bottom = 80,95,W2-40,H2-60
vmin,vmax = min(0,min(cum)), max(cum); 
if vmax==vmin: vmax=vmin+1
def y(v): return bottom-(v-vmin)/(vmax-vmin)*(bottom-top)
def x(i): return left + (i)/(len(cum)-1)*(right-left)
for k in range(5):
    v = vmin + (vmax-vmin)*k/4
    yy=y(v); d2.line([(left,yy),(right,yy)],fill="#e5e7eb")
    d2.text((left-58,yy-8),f"{v:.0f}",fill="#6b7280",font=font(13))
if vmin<=0<=vmax: d2.line([(left,y(0)),(right,y(0))],fill="#9ca3af")
pts=[(x(i),y(c)) for i,c in enumerate(cum)]
d2.line(pts,fill="#2563eb",width=3)
for i,(px,py) in enumerate(pts):
    col = "#16a34a" if rows[i][6]>=0 else "#dc2626"
    d2.ellipse([px-4,py-4,px+4,py+4],fill=col)
d2.text((30,H2-30),"仅为模拟账户历史记录，不代表未来收益；未通过策略回测验证。",fill="#b91c1c",font=font(11))
img2.save(r"C:\Users\ruaibeite\Desktop\gold\gold-auto-ea-showcase\assets\audusd-live.png")
print("trades", len(rows), "sum", round(cum[-1],2))
