title: 为PPT生成页码
category: programming
tags: ppt
date: 2016-10-13
template: post.html


弃用`beamer`改用`powerpoint`，
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
