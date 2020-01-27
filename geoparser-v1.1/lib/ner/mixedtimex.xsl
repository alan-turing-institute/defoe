<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="timex[@type='mix' and timex[@type='time'][2]]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select="timex[@type='date']/@*"/>
    <xsl:attribute name="time">
      <xsl:if test="timex[@type='time' and @tval]">
        <xsl:value-of select="timex[@type='time' and @tval]/@tval"/>
      </xsl:if>
    </xsl:attribute>
    <xsl:attribute name="time2">
      <xsl:if test="timex[@type='time' and not(@tval)]">
        <xsl:value-of select="timex[@type='time' and not(@tval)]"/>
      </xsl:if>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="timex[@type='mix' and not(timex[@type='time'][2])]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select="timex[@type='date']/@*"/>
    <xsl:attribute name="time">
      <xsl:if test="timex[@type='time' and @tval]">
        <xsl:value-of select="timex[@type='time']/@tval"/>
      </xsl:if>
      <xsl:if test="timex[@type='time' and not(@tval)]">
        <xsl:value-of select="timex[@type='time']"/>
      </xsl:if>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="timex[@type='mix']/timex">
  <xsl:apply-templates select="node()"/>
</xsl:template>

</xsl:stylesheet>

