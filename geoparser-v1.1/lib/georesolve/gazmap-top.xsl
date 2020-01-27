<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns="http://www.w3.org/1999/xhtml">

<!-- Extract top-ranked places from the gaz.xml list of candidate locations and reformat for display on a google map. -->

<xsl:param name="key" select="dummy"/>

<xsl:output method="html"
	    doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"
	    doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"/>

<xsl:template match="/">
  <xsl:variable name="firstplace" select="(//place)[1]"/>
<html>
  <head>
    <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
    <title>Geoparser results</title>
    <script src="http://maps.google.com/maps?file=api&amp;v=2&amp;key={$key}"
      type="text/javascript"></script>
    <script type="text/javascript">

    var map;

     <!-- icon code from http://groups.google.com/group/Google-Maps-API/browse_thread/thread/d2374aa1490685e2 -->

    var red_icon = new GIcon(G_DEFAULT_ICON, "http://www.google.com/intl/en_us/mapfiles/ms/micons/red-dot.png");
    var green_icon = new GIcon(G_DEFAULT_ICON, "http://www.google.com/intl/en_us/mapfiles/ms/micons/green-dot.png");

    red_icon.size = green_icon.size = new GSize(32, 32);
    red_icon.iconAnchor = green_icon.iconAnchor = new GPoint(16,32); 
    red_icon.shadowSize = green_icon.shadowSize = new GSize(59,32);
    red_icon.shadow = green_icon.shadow = "http://maps.google.com/mapfiles/ms/micons/msmarker.shadow.png" 

    function load() {
      if (GBrowserIsCompatible()) {
        var point;
        map = new GMap2(document.getElementById("map"));
	map.addControl(new GLargeMapControl());
        map.setCenter(new GLatLng(<xsl:value-of select="$firstplace/@lat"/>,
	                          <xsl:value-of select="$firstplace/@long"/>), 4);
	<xsl:apply-templates mode="markers" select="//placename/place"/>
      }
    }

    function goto(x, y) {
        map.setCenter(new GLatLng(x, y), 6);
    }

    function show_info(name) {
	var para = document.getElementById("message").firstChild;
	para.nodeValue = name;
    }
    </script>

    <style>
      .found {color: green;} 
      table  {border-collapse: collapse; empty-cells: show;}
      tr     {border: 1px solid black;}
      td {color: green;}
     </style>

  </head>
  <body onload="load()" onunload="GUnload()">
    <div id="map" style="height: 400px"></div>
  </body>
</html>

</xsl:template>

<xsl:template mode="markers" match="place[@rank='1']">
        point = new GLatLng(<xsl:value-of select="@lat"/>, <xsl:value-of select="@long"/>);
	marker = new GMarker(point, {title: "<xsl:value-of select="translate(@name, '&quot;', '_')"/>",
	                             icon: green_icon});
	map.addOverlay(marker);
</xsl:template>

</xsl:stylesheet>
