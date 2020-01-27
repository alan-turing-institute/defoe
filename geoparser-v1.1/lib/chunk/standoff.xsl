<!-- Convert inline markup to standoff. -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="standoff">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
    <xsl:text>&#10;</xsl:text>
    <chunks>
      <xsl:apply-templates select="//s//*[not(self::w)]" mode="standoff"/>
      <xsl:text>&#10;</xsl:text>
    </chunks>
  </xsl:copy>
</xsl:template>

<xsl:template match="w">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="s//*[not(self::w)]">
  <xsl:apply-templates select="node()"/>
</xsl:template>

<xsl:template mode="standoff" match="*">
  <xsl:text>&#10;  </xsl:text>
  <xsl:copy>
    <xsl:attribute name="sw">
       <xsl:value-of select="(.//w)[1]/@id"/>
    </xsl:attribute>
    <xsl:attribute name="ew">
       <xsl:value-of select="(.//w)[last()]/@id"/>
    </xsl:attribute>
    <xsl:apply-templates select="@*"/>
    <xsl:value-of select="."/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
