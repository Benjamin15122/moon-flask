
<script language="JavaScript" src="../js/navbar.js"></script>


<hr>
<h2 class="intro-text text-center">Personal
<strong>Blog</strong>
</h2>
<hr>
<center>
<h2>RR for Android
<br>
<small>August 28, 2014</small>
</h2>
</center>
<p style="font-family: 'Josefin Slab','Helvetica Neue',Helvetica,Arial,sans-serif;"><strong><font size=5>1. What is RR for Android</font></strong></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;”RR for Android” is the short for Record and Replay for Android platform. The original idea is coming from <strong>[Gomez@ICSE'13]</strong> :</p>

<p>&nbsp;&nbsp;&nbsp;&nbsp;<em>Lorenzo Gomez, Iulian Neamtiu, Tanzirul Azim, and Todd Millstein. 2013. RERAN: timing- and touch-sensitive      record and replay for Android. In Proceedings of the 2013 International Conference on Software Engineering  (ICSE ’13). IEEE Press, Piscataway, NJ, USA, 72-81.</em></p>

<p>&nbsp;&nbsp;&nbsp;&nbsp;<i>RERAN</i> is the cooperation of PC and mobile, while ONLY mobile device is needed in our RR!</p>


<p style="font-family: 'Josefin Slab','Helvetica Neue',Helvetica,Arial,sans-serif;"><strong><font size=5>2. How to use RR</font></strong></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;Below is a video showing how to use RR: <font color="red">(password: ics)</font></p>

&nbsp;&nbsp;&nbsp;&nbsp;<embed src="http://player.youku.com/player.php/sid/XNzM1OTM1MTQ4/v.swf" allowfullscreen="true" quality="high" width="520" height="430" align="middle" allowscriptaccess="always" type="application/x-shockwave-flash"/>


<p style="font-family: 'Josefin Slab','Helvetica Neue',Helvetica,Arial,sans-serif;"><strong><font size=5>3. How to install RR</font></strong></p>
<p style="font-family: 'Josefin Slab','Helvetica Neue',Helvetica,Arial,sans-serif;"><strong><font size=4>&nbsp;&nbsp;&nbsp;&nbsp;3.1 ROOT</font></strong></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Make sure that your mobile device has been ROOTed!</p>

<p style="font-family: 'Josefin Slab','Helvetica Neue',Helvetica,Arial,sans-serif;"><strong><font size=4>&nbsp;&nbsp;&nbsp;&nbsp;3.2 COPY</font></strong></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Copy <a href="http://xiujiang.sourceforge.jp/wp-content/uploads/pages/RR/replay" target="_blank">replay</a> file to /data/local.</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>$ adb shell push replay /data/local</code></p>

<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Copy <a href="http://xiujiang.sourceforge.jp/wp-content/uploads/pages/RR/toolbox" target="_blank">toolbox</a> file to /data/local.</p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<code>$ adb shell push toolbox /system/bin</code></p>

<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color: #ff0000;">ATTENTION:</span> “toolbox” file is for Android 4.4.2. If you want to acquire “toolbox” file in your own Android version, you should add “fflush(STDOUT)” after each “printf” in “system/core/toolbox/getevent.c” in Android source code and build it (you can read <a href="http://blog.163.com/zhou_411424/blog/static/19736215620139101154776" target="_blank">this</a> to build Android).</p>

<p style="font-family: 'Josefin Slab','Helvetica Neue',Helvetica,Arial,sans-serif;"><strong><font size=4>&nbsp;&nbsp;&nbsp;&nbsp;3.3 INSTALL</font></strong></p>
<p>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Install <a href="http://xiujiang.sourceforge.jp/wp-content/uploads/pages/RR/RR.apk" target="_blank">RR.apk</a> in your device. The apk file is for Android 4.4.2 and the support to other versions is coming soon!</p>

</br>

<center>---OVER---</center>
<hr>

