<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml">

<xsl:param name="key" select="dummy"/>

<xsl:output method="html"
	    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
	    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"/>

<xsl:template match="/">
  <xsl:variable name="firstplace" select="(//place)[1]"/>
<html>
  <head>
    <meta http-equiv="content-type" content="application/xhtml+xml; charset=utf-8"/>
    <title>Geoparser results</title>
    <script src="http://maps.googleapis.com/maps/api/js?key={$key}&amp;sensor=false"
	    type="text/javascript" ></script>
    <script type="text/javascript">

    var map;
    var markers = new Array();

    var icondir = "http://www.google.com/intl/en_us/mapfiles/ms/micons/";
    var red_icon = icondir+"red-dot.png";
    var green_icon = icondir+"green-dot.png";

    function load() {
        var center = new google.maps.LatLng(<xsl:value-of select="$firstplace/@lat"/>,
                                            <xsl:value-of select="$firstplace/@long"/>);
	map = new google.maps.Map(document.getElementById("map"),
                               {center: center,
                                zoom: 6,
                                overviewMapControl: true,
                                overviewMapControlOptions: {opened: true}
                               });
	<xsl:apply-templates mode="markers" select="//placename/place"/>

	adjust_locations(markers);
    }

    function goto(x, y) {
        map.setCenter(new google.maps.LatLng(x, y), 10);
    }

    function show_info(name) {
	var para = document.getElementById("message").firstChild;
	para.nodeValue = name;
    }

    <!-- we create a javascript-commented-out CDATA section because of the special
          characters (lt, gt, amp) in the javascript -->

    <xsl:text disable-output-escaping="yes">
//&lt;![CDATA[

// adjust the locations of identically-positioned candidates so they are
// distinguishable on the map.

function adjust_locations(markers)
{
    markers.sort(compare_locations);

    var dups = new Array();

    var lastlat = 99999, lastlng = 9999;
    for(var i=0; i &lt; markers.length; i++)
    {
        var l = markers[i].getPosition();
        if(l.lat() == lastlat &amp;&amp; l.lng() == lastlng)
        {
//            alert("match: " + l.lat() + "," + l.lng() + " = " + lastlat + ","  + lastlng);
            dups.push(markers[i]);
        }
        else
        {
            if(dups.length > 1)
                spread(dups);
            dups.length = 0;
            dups.push(markers[i]);
        }
        lastlat = l.lat();
        lastlng = l.lng();
    }
    if(dups.length > 1)
        spread(dups);
}

// spread an array of identically-positioned markers into a 0.005 degree circle

function spread(dups)
{
    var latlng = dups[0].getPosition();
    var lat = latlng.lat(), lng = latlng.lng();
//    alert("Spreading " + dups.length + " markers from " + lat + "," + lng);
    for(var i=0; i &lt; dups.length; i++)
    {
        var point = new google.maps.LatLng(55.944696, -3.187004);

        var newlatlng = new google.maps.LatLng(
            lat + Math.sin((2 * 3.14159 * i) / dups.length) * 0.005,
            lng + Math.cos((2 * 3.14159 * i) / dups.length) * 0.005);
        dups[i].setPosition(newlatlng);
//        alert(lat + " -> " + newlatlng.lat() + "   " + lng + " -> " + newlatlng.lng());
    }
}

// comparison function for sorting

function compare_locations(m1, m2)
{
    var l1 = m1.getPosition(), l2 = m2.getPosition();
    if(l1.lat() == l2.lat())
        return l1.lng() - l2.lng();
    else
        return l1.lat() - l2.lat();
}
//]]&gt;
      </xsl:text>
    </script>

    <style>
      .found {color: red;} 
      table  {border-collapse: collapse; empty-cells: show;}
      tr     {border: 1px solid black;}
      td[best="true"] {color: green;}
      td[best="false"] {color: red;}
    </style>

  </head>
  <body onload="load()">
    <div id="map" style="height: 400px"></div>
  </body>
</html>

</xsl:template>

<xsl:template mode="markers" match="place">
        point = new google.maps.LatLng(<xsl:value-of select="@lat"/>, <xsl:value-of select="@long"/>);
        var marker = new google.maps.Marker({
	    title: "<xsl:value-of select="translate(@name, '&quot;', '_')"/>",
	    icon: <xsl:value-of select="@rank"/> == 1 ? green_icon : red_icon,
            position: point,
            map: map,
	    zIndex: google.maps.Marker.MAX_ZINDEX + 1000 - <xsl:value-of select="@rank"/>
      });
      markers.push(marker);
</xsl:template>

</xsl:stylesheet>
