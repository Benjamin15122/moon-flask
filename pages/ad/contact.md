title: 联系我们
bundle: qqmap

<div class="row gutter"><!-- row -->
    <div class="col-lg-12 col-md-12">
        <div id="panoCon" style="height: 500px;"></div> 
        <div id="overViewCon" style="height:300px;"></div>
    </div>
</div><!-- row end -->

~~~{.customjs}
var panorama = new qq.maps.Panorama('panoCon', {
    "pano": "10101122121102140333100",
    "pov":{
        heading:82,
        pitch:0
    }
});
var ovc=document.getElementById('overViewCon');
var overview = new qq.maps.PanoOverview(ovc,{
    panorama:panorama
});
var qqmap=overview.getMap();
~~~
