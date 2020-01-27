<!DOCTYPE xsl:stylesheet [
<!ENTITY nbsp "&#xa0;">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:param name="georesfile" select="''"/>
<xsl:key name="placename" match="placename" use="@name"/>

<xsl:template match="/">
  <html>
    <head>
      <title>Geoparser Output</title>
      <style>span.loc {background:#E0FFE8}</style>
    </head>
    <body bgcolor='#BBCCAA'>
      <div id="text">
      <xsl:apply-templates select="//text"/>
      </div>
    </body>
  </html>
</xsl:template>

<xsl:template match="p">
  <p>
    <xsl:apply-templates/>
  </p>
</xsl:template>

<xsl:template match="enamex[@type='location']">
  <xsl:variable name="ent">
    <xsl:value-of select="normalize-space(.)"/>
  </xsl:variable>
  <xsl:variable name="link">
    <xsl:for-each select="document($georesfile, .)"> 
      <xsl:for-each select="key('placename', $ent)">
        <xsl:value-of select="place[@rank='1']/@uricdda"/>
      </xsl:for-each>
    </xsl:for-each>
  </xsl:variable>
  <xsl:choose>
    <xsl:when test="$link~'.'">
      <a>
        <xsl:attribute name="href">
          <xsl:value-of select="$link"/>
        </xsl:attribute>
        <span class="loc">
          <xsl:apply-templates/>
        </span>
      </a>
    </xsl:when>
    <xsl:otherwise>
      <span class="loc">
        <xsl:apply-templates/>
      </span>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>
