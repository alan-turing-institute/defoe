<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:param name="begindate" select="''"/>
<xsl:param name="enddate" select="''"/>

<xsl:template match="place">
  <xsl:choose>
    <xsl:when test="attestations/attestation/date[(@begin &gt;= $begindate and @begin &lt;= $enddate) or (@end &gt;= $begindate and @end &lt;= $enddate)]">
      <xsl:copy>
        <xsl:apply-templates select="node()|@*"/>
      </xsl:copy>
    </xsl:when>
    <xsl:otherwise>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
