title: Supplementary Materials


# Supplementary Materials

This is the supplementary material for the APSEC'16 paper

* {{ render_bib_entry(g.site.spar_paper.wu_testing_2016) }}

## Study of Gesture Recognition
To investigate how gestures are recognized in Android, we studied technical documents (API documentations [1], books [2], [3] and tutorials [4]) as well as open-source projects (from F-Droid [5] and GitHub [6], by searching with keywords “gesture” and “Android”). In those open-source projects, we study code that is related to gesture recognition and handling.

We summarize the four most popular categories of gesture recognition as follows, in the order of decreasing popularity:
 
1. Using the GestureDetector library. To use GestureDetector, the developer provides a gesture listener object (of a subclass of GestureListener), which contains overriding methods that indicate its relevant gestures. GestureDetector object takes a MotionEvent object as an argument to invoke GestureDetector.onTouchEvent. This method will finish the work of gesture recognition.
2. Parsing the MotionEvent objects with customized code. Within this category, gesture recognition can be as simple as a threshold checking (e.g., detecting a scrolling gesture by checking discrepancies of x and y coordinates), or as complex as invoking a classifier trained by machine-learning algorithm. We find that in such cases, the recognized gestures are (1) simple gestures, as it is so easy to recognize those gestures that developers needn’t bother GestureDetector; (2) multi-touch gestures, as MotionEvent provides rich APIs for handling multi-touch, and developers can recognize specific or even fancy multi-touch gestures based on the sequence of MotionEvent objects.
3. Using GestureOverlayView and GestureLibrary [11]. Gestures drawn on a GestureOverlayView object can be captured and stored in a GestureLibrary object. Later, if users draw a gesture that needs to be recognized, developers can tend to the GestureLibrary object and invoke GestureLibrary.recognize on this object to infer the user-defined type of this gesture.
4. Built-in gesture recognition of a UI component. Some types of views are bound with specific gestures, and such gestures are automatically recognized by the Android system. For example, the view android.support.v4.ViewPager receives scroll gestures. Another example is registering a drag listener on a view, which makes the view relevant to drag gestures.
 
To the best of our knowledge, all gesture recognition ways in Android can be classified as one of the four categories.

[1] “Android classes,” http://developer.android.com/reference/.<br>
[2] “Android Programming: The Big Nerd Ranch Guide,” https://www.bignerdranch.com/we-write/android-programming/.<br>
[3] “Head First Android Development,” http://www.amazon.com/Head-First-Android-Development-Griffiths/dp/1449362184.<br>
[4] “Android - Gestures totorial,” http://www.tutorialspoint.com/android/android gestures.htm/.<br>
[5] “F-Droid,” https://f-droid.org/.<br>
[6] “Github,” https://github.com/.<br>

## Experiment Demo Subjects

<table border="1">
  <tr>
    <th>App Name</th>
    <th>URL</th>
  </tr>
  <tr>
      <td>Coverflow</td>
    <td>https://github.com/missingfeature/android-coverflow</td>	
	</tr>
	<tr>
    <td>Zoompage</td>
    <td>https://github.com/victoryckl/zoompage</td>
	</tr>
	<tr>
    <td>Sidemenu</td>
    <td>https://github.com/dmitry-zaitsev/AndroidSideMenu</td>
	</tr>
	<tr>
    <td>Flotandroid Chart</td>
    <td>https://github.com/himanshu1706/flot-android-chart</td>
	</tr>
	<tr>
    <td>Androviews</td>
    <td>https://github.com/olibye/AndroViews</td>
	</tr>
	<tr>
    <td>Swipeable-Cards</td>
    <td>https://github.com/kikoso/Swipeable-Cards/</td>
	</tr>	
  </tr>
</table>

