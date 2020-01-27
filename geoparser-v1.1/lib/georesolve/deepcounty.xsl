<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:param name="countiesin" select="''"/>

<xsl:template match="place">
  <xsl:variable name="countylist">
    <xsl:value-of select="normalize-space(translate($countiesin, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'))"/>
  </xsl:variable>
  <xsl:variable name="county">
    <xsl:value-of select="translate(@deepcounty, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>
  </xsl:variable>
  <xsl:choose>
    <xsl:when test="not(contains($countylist, $county))">
    </xsl:when>
    <xsl:otherwise>
      <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
