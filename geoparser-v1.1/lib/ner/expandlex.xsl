<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="name[@type='person' and w[2]]">
  <name type='person'><xsl:apply-templates select="w"/></name>
  <xsl:text>&#10;</xsl:text>
  <name type='person'><xsl:apply-templates select="w[last()][not(@init) and not(@title)]"/></name>
  <xsl:text>&#10;</xsl:text>
  <name type='person'><xsl:apply-templates select="w[position()!=last()][not(@init) and not(@title) and not(.=',') and .~'^[A-Z]']"/></name>
  <xsl:text>&#10;</xsl:text>
  <name type='person'><xsl:apply-templates select="w[1][not(@init) and not(@title) and not(.=',') and .~'^[A-Z]']"/></name>
  <xsl:text>&#10;</xsl:text>
  <name type='person'><xsl:apply-templates select="w[position()>1][not(@init) and not(@title) and not(.=',')]"/></name>
  <xsl:text>&#10;</xsl:text>
  <name type='person'><xsl:apply-templates select="w[position()>2][not(@init) and not(@title)]"/></name>
  <xsl:text>&#10;</xsl:text>
  <name type='person'><xsl:apply-templates select="w[.~'^[A-Z]' and not(@init) and not(@title)]"/></name>
</xsl:template>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
