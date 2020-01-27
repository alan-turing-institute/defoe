<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<!-- stylesheet to extract text from pipeline output file, formatted as html page with timeline -->

<xsl:param name="jsfile" select="''"/>
<xsl:param name="outfname" select="''"/>
<xsl:param name="nerfname" select="''"/>

<!--create html page with docdate as heading; use docdate for centering timeline-->
<xsl:template match="/">
  <html>
    <head>
      <meta http-equiv="Content-Type" content="text/html;charset=UTF-8"> <xsl:text>&#10;  </xsl:text> <!-- &#10; is the newline char -->
        <title>timeline</title>
        <xsl:text>&#10;  </xsl:text>
        <!--<script src="http://static.simile.mit.edu/timeline/api-2.3.0/timeline-api.js?bundle=true" type="text/javascript"></script>-->
	<script src="http://api.simile-widgets.org/timeline/2.3.1/timeline-api.js?bundle=true" type="text/javascript"></script>
        <xsl:text>&#10;  </xsl:text>
        <script type="text/javascript">
          <xsl:attribute name="src">timeline.js</xsl:attribute>
        </script>
        <xsl:text>&#10;  </xsl:text>
        <script>var datetime=&quot;<xsl:value-of select="//attr/@sdate"/><xsl:text>T00:00:00Z</xsl:text>&quot;</script>
        <xsl:text>&#10;  </xsl:text>
        <!-- filename for events '.events.xml' appended -->
        <script>var eventsList=&quot;<xsl:value-of select="$outfname"/><xsl:text>.events.xml</xsl:text>&quot;</script> 
        <xsl:text>&#10;  </xsl:text>
      </meta>
      <style>span.loc {background:#66CC66}</style>
      <style>span.per {background:#FF3333}</style>
      <style>span.org {background:#0099FF}</style>
      <style>span.date {background:#FFCC00}</style>
    </head>
    <body onload="onLoad(datetime, eventsList, 'timelineBox', '70%', '30%');" onresize="onResize();">
      <div id="text">
        <h2>Docdate: <xsl:value-of select="//attr/@sdate" /></h2>
        <xsl:apply-templates select="//text" />
        <br /><br />
      </div>
      <div id="timelineBox" style="border: 1px solid rgb(170, 170, 170); height: 200px;"></div>
     <noscript>
      This page uses Javascript to show you a Timeline. Please enable
      Javascript in your browser to see the full page. Thank you.
      </noscript>
    </body>
  </html>
</xsl:template>

<xsl:template match="text">
  <xsl:apply-templates select="document($nerfname)//p"/>
</xsl:template>

<xsl:template match="p">
  <p>
    <xsl:apply-templates/>
  </p>
</xsl:template>

<xsl:template match="enamex[@type='location']">
  <span class="loc">
    <xsl:apply-templates/>
  </span>
</xsl:template>

<xsl:template match="enamex[@type='person']">
  <span class="per">
    <xsl:apply-templates/>
  </span>
</xsl:template>

<xsl:template match="enamex[@type='organization']">
  <span class="org">
    <xsl:apply-templates/>
  </span>
</xsl:template>

<xsl:template match="timex[@type='date']">
  <span class="date">
    <xsl:apply-templates/>
  </span>
</xsl:template>

</xsl:stylesheet>