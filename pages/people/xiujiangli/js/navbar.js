var prefix = "";

if (window.location.pathname.indexOf("posts") == -1) {
	prefix = "";
}
else {
	prefix = "../";
}

document.write(""+
    "<nav class=\"navbar navbar-default\" role=\"navigation\">"+
        "<div class=\"container\">"+
            "<div class=\"collapse navbar-collapse\" id=\"bs-example-navbar-collapse-1\">"+
                "<ul class=\"nav navbar-nav\">"+
                    "<li>"+
                        "<a href=\"" + prefix + "index.html\">Home</a>"+
                    "</li>"+
                    "<li>"+
                        "<a href=\"" + prefix + "blog.html\">Blog</a>"+
                    "</li>"+
                    "<li>"+
                        "<a href=\"" + prefix + "contact.html\">Contact</a>"+
                    "</li>"+
                "</ul>"+
            "</div>"+
        "</div>"+
    "</nav>");
