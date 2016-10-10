function decode(h) {
    var textArea = document.createElement('textarea');
    textArea.innerHTML = h;
    val = textArea.value;
    if ('remove' in Element.prototype) textArea.remove();
    return val;
}

$(function() {
  $("span.math").each(function(idx, e) {
    try {
      var d = katex.renderToString(decode(e.innerHTML), { displayMode: true, throwOnError: false });
      e.innerHTML = d;
    } catch (err) {}
  });

  $("span.inline_math").each(function(idx, e) {
    try {
      var d = katex.renderToString(decode(e.innerHTML), { throwOnError: false });
      e.innerHTML = d;
    } catch (err) {}
  });

});
