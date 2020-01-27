<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:param name="filename">
  <xsl:value-of select="$filename"/>
</xsl:param>

<xsl:template match="body">
  <document>
    <meta/>
    <xsl:apply-templates select="node()"/>
  </document>
</xsl:template>

<xsl:template match="div[@class='ocr_page']">
  <text>
    <page fileid="{$filename}">
    <xsl:apply-templates select="node()"/>
    </page>
  </text>
</xsl:template>

<xsl:template match="div[@class='ocrx_block']">
  <xsl:apply-templates select="node()|*"/>
</xsl:template>

<xsl:template match="p">
  <p>
    <xsl:attribute name="bbox">
      <xsl:value-of select="substring-after(@title, ' ')"/>
    </xsl:attribute>
    <xsl:attribute name="block">
      <xsl:value-of select="count(../preceding-sibling::div)"/>
    </xsl:attribute>
    <xsl:apply-templates select="node()|*"/>
  </p>
</xsl:template>

<xsl:template match="span[@class='ocr_line']">
  <xsl:apply-templates select="node()|*"/>
  <xsl:text>&#10;</xsl:text>
</xsl:template>

<xsl:template match="br">
</xsl:template>

<xsl:template match="span[@class='ocr_cinfo']">
  <span>
    <xsl:attribute name="bbox">
      <xsl:value-of select="substring-after(@title, ' ')"/>
    </xsl:attribute>
    <xsl:if test="@style~'bold'">
      <xsl:attribute name="font">bold</xsl:attribute>
    </xsl:if>
    <xsl:apply-templates select="node()|*"/>
  </span>
</xsl:template>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
