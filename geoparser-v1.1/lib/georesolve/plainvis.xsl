<!DOCTYPE xsl:stylesheet [
<!ENTITY nbsp "&#xa0;">
]>

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

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
  <span class="loc">
    <xsl:apply-templates/>
  </span>
</xsl:template>

</xsl:stylesheet>
