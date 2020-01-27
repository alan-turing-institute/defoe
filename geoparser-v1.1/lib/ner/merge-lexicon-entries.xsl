<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:key name="word" match="lex" use="@word"/>

<xsl:template match="lex">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select="key('word', @word)/*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
