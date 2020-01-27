<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:import href="dates.xsl"/>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="ent[@month~'.' and @year~'.' and not(@date)]">
  <xsl:variable name="firstnextmonth">
    <xsl:call-template name="compute-day-number">
      <xsl:with-param name="day" select="1"/>
      <xsl:with-param name="month" select="@month+1"/>
      <xsl:with-param name="year" select="@year"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="edate">
    <xsl:call-template name="compute-date">
      <xsl:with-param name="day-number" select="$firstnextmonth - 1"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="firstthismonth">
    <xsl:call-template name="compute-day-number">
      <xsl:with-param name="day" select="1"/>
      <xsl:with-param name="month" select="@month"/>
      <xsl:with-param name="year" select="@year"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="sdate">
    <xsl:call-template name="compute-date">
      <xsl:with-param name="day-number" select="$firstthismonth"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="edate">
      <xsl:value-of select="$edate"/>
    </xsl:attribute>
    <xsl:attribute name="sdate">
      <xsl:value-of select="$sdate"/>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
