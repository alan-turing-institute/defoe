<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  xmlns="http://www.w3.org/1999/xhtml">

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

    <style>
      .found {color: red;} 
      table  {border-collapse: collapse; empty-cells: show;}
      tr     {border: 1px solid black;}
      td[best="true"] {color: green;}
      td[best="false"] {color: red; visibility: hidden;}
    </style>
  </head>

  <body>
    <div id="instr">
      <p>
        Click on a lat/long to centre the map there.
      </p>
    </div>
    <div id="table">
      <table cellpadding="3">
        <xsl:apply-templates select="//placename"/>
      </table>
    </div>
  </body>
</html>

</xsl:template>

<xsl:template match="placename">
  <tr>
    <td><xsl:value-of select="translate(@name, ' ', '&#xa0;')"/></td>
    <xsl:apply-templates select="place"/>
  </tr>
</xsl:template>

<!-- remove mode="decimal" if you want the old style of display -->
<xsl:template match="place">
 <td best="{@rank = 1}">
  <a onClick="parent.map.goto({@lat},{@long})">
    <span style="white-space:nowrap">
      <xsl:apply-templates select="@lat" mode="decimal"/>
      <xsl:text>,</xsl:text>
      <xsl:apply-templates select="@long" mode="decimal"/>
    </span>
  </a>
 </td>
</xsl:template>

<xsl:template match="@lat|@long" mode="decimal">
    <xsl:value-of select="format-number(., '0.000')"/>
</xsl:template>

<xsl:template match="@lat[. &lt; 0]">
  <xsl:call-template name="latlong"/>
  <xsl:text>S</xsl:text>
</xsl:template>

<xsl:template match="@lat">
  <xsl:call-template name="latlong"/>
  <xsl:text>N</xsl:text>
</xsl:template>

<xsl:template match="@long[. &lt; 0]">
  <xsl:call-template name="latlong"/>
  <xsl:text>W</xsl:text>
</xsl:template>

<xsl:template match="@long">
  <xsl:call-template name="latlong"/>
  <xsl:text>E</xsl:text>
</xsl:template>

<xsl:template name="latlong">
  <xsl:variable name="abs">
    <xsl:choose>
      <xsl:when test=". &lt; 0"><xsl:value-of select="-."/></xsl:when>
      <xsl:otherwise><xsl:value-of select="."/></xsl:otherwise>
    </xsl:choose>
  </xsl:variable>
  <xsl:value-of select="floor($abs)"/>
  <xsl:text>&#xb0;</xsl:text>
  <xsl:value-of select="round(($abs - floor($abs)) * 60)"/>
  <xsl:text>'</xsl:text>
</xsl:template>

</xsl:stylesheet>
