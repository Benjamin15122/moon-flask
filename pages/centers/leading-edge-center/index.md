title: 交叉与前沿中心 

# 交叉与前沿中心
<hr>

## 成员
{{ render_people(center = "leading-edge", category = ["faculty"], large=True) | safe }}
<hr>

## 博士研究生
{{ render_people(category="phd", center='leading-edge', large=True) | safe }}
<hr>

## 硕士研究生
{{ render_people(category="graduates", center='leading-edge', large=True) | safe }}

