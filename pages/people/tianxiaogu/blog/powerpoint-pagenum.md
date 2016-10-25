title: 为PPT生成页码
category: programming
tags: ppt
date: 2016-10-13
template: post.html


最近弃用`beamer`改用`powerpoint`，
但是PowerPoint的插入页脚功能简直不能用，
为此先是找了一段VBA代码，再改为了python代码。

## pywin32

`pywin32com`参考了如下链接：

* <http://www.s-anand.net/blog/automating-powerpoint-with-python/>
* <http://docs.activestate.com/activepython/3.3/pywin32/html/com/win32com/HTML/QuickStartClientCom.html#UsingComConstants>



~~~{.py}
#!/use/bin/python3

import os, sys, traceback, itertools

import win32com.client

# Run `makepy.py -o ..\gen_py\office.py "Microsoft Office 15.0 Object Library"` in the fold
# `Python35\Lib\site-packages\win32com\client` first
import win32com.gen_py.office

PowerPoint = win32com.client.gencache.EnsureDispatch('PowerPoint.Application')

def RGB(r,g,b):
    return r + g * 256 + b * 256 ** 2

def get_opened_presentation(ppt_file):
    for p in PowerPoint.Presentations:
        if os.path.samefile(p.FullName, ppt_file):
            return p

    return PowerPoint.Presentations.Open(ppt_file)

def add_page_number(ppt_file):
    ppt = get_opened_presentation(ppt_file)

    SlideHeight= ppt.PageSetup.SlideHeight
    SlideWidth = ppt.PageSetup.SlideWidth
    msoShapeRectangle = win32com.client.constants.msoShapeRectangle

    slides_count = int(ppt.Slides.Count)

    # ignore the first and the last slides
    slides = list([ppt.Slides(i) for i in range(2, slides_count)])

    invisible_slides = list([slide for slide in slides if slide.SlideShowTransition.Hidden])
    for slide in invisible_slides:
        for shape in slide.Shapes:
            if shape.Name.startswith('Slide Number'):
                shape.TextFrame.TextRange.Text = ''

    visible_slides = list([slide for slide in slides if not slide.SlideShowTransition.Hidden])
    total_visible_count = len(visible_slides)
    for page_number,slide in enumerate(visible_slides, 1):
        for shape in slide.Shapes:
            if shape.Name.startswith('Slide Number'):
                shape.TextFrame.TextRange.Text = '{0}/{1}'.format(page_number, total_visible_count)

        try:
            slide.Shapes("PB").Delete
        except:
            pass

        s = slide.Shapes.AddShape(msoShapeRectangle, 0, SlideHeight - 3, page_number * SlideWidth / total_visible_count, 3)
        s.Fill.ForeColor.RGB = RGB(255, 0, 0)
        s.Line.ForeColor.RGB = RGB(0, 0, 255)
        s.Name = "PB"

if __name__ == '__main__':
    try:
        add_page_number(os.path.abspath(sys.argv[1]))
    except:
        traceback.print_exc()
~~~

## PowerPoint VBA

网上不记得从哪里找到的一段插入进度条的VBA代码，
加以改造，留待以后复制使用。

代码具体是统计全部的slides数目，剔除隐藏的slides，算总的页码，然后以插入类似`4/100`这样的形式插入。

* 判断slide是否是隐藏的用`Slide.SlideShowTransition.Hidden`
* 需要先插入页眉页脚
    * 页码对应的文本框（占位符？？）是一个`Shape`，其`Name`为`Slide Number`后跟一个数字。
* VBA太难用了，都不知道语法在哪里找，有空用`pywin32+COM`写成一个命令行工具


~~~{.vbnet}
Sub InsertSlideNumber()
    On Error Resume Next
        With ActivePresentation
        VC = 0
        For x = 2 To .Slides.Count - 1 '第一页和最后一页不加

              If .Slides(x).SlideShowTransition.Hidden Then
                GoTo ContinueLoop
              End If
              VC = VC + 1
ContinueLoop:
              Next x:

              VN = 1
              For x = 2 To .Slides.Count - 1 '第一页和最后一页不加

              If .Slides(x).SlideShowTransition.Hidden Then
              With .Slides(x)
                For s = 1 To .Shapes.Count
                    If .Shapes(s).Name Like "Slide Number*" Then
                       .Shapes(s).TextFrame.TextRange.Text = ""
                    End If
                Next s:
              End With
                GoTo ContinueLoop2
              End If

              With .Slides(x)
                For s = 1 To .Shapes.Count
                    If .Shapes(s).Name Like "Slide Number*" Then
                       .Shapes(s).TextFrame.TextRange.Text = VN & "/" & VC

                    End If
                Next s:
              End With
              .Slides(x).Shapes("PB").Delete
              Set s = .Slides(x).Shapes.AddShape(msoShapeRectangle, _
              0, .PageSetup.SlideHeight - 3, _
              VN * .PageSetup.SlideWidth / VC, 3) '条高度
              s.Fill.ForeColor.RGB = RGB(246, 202, 5) '设置颜色
              s.Name = "PB"

              VN = VN + 1
ContinueLoop2:
              Next x:
        End With
End Sub
~~~
