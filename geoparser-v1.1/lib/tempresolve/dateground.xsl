<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:import href="dates.xsl"/>

<xsl:variable name="docyear">
  <xsl:value-of select="/document/meta/attr[@name='docdate']/@year"/>
</xsl:variable>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="attr[@month~'.' and @date~'.' and @year~'.']">
  <xsl:variable name="dnum">
    <xsl:call-template name="compute-day-number">
      <xsl:with-param name="day" select="@date"/>
      <xsl:with-param name="month" select="@month"/>
      <xsl:with-param name="year" select="@year"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="wday">
    <xsl:call-template name="compute-weekday">
      <xsl:with-param name="day-number" select="$dnum"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="sdate">
      <xsl:call-template name="compute-date">
        <xsl:with-param name="day-number" select="$dnum"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:attribute name="day-number">
      <xsl:value-of select="$dnum"/>
    </xsl:attribute>
    <xsl:attribute name="day">
      <xsl:value-of select="$wday"/>
    </xsl:attribute>
    <xsl:attribute name="wdaynum">
      <xsl:call-template name="compute-weekdaynum">
        <xsl:with-param name="weekday" select="$wday"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="ent[@month~'.' and @date~'.' and @year~'.']">
  <xsl:variable name="dnum">
    <xsl:call-template name="compute-day-number">
      <xsl:with-param name="day" select="@date"/>
      <xsl:with-param name="month" select="@month"/>
      <xsl:with-param name="year" select="@year"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="sdate">
      <xsl:call-template name="compute-date">
        <xsl:with-param name="day-number" select="$dnum"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:attribute name="day-number">
      <xsl:value-of select="$dnum"/>
    </xsl:attribute>
    <xsl:attribute name="day">
      <xsl:call-template name="compute-weekday">
        <xsl:with-param name="day-number" select="$dnum"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="ent[@day-number~'.' and (not(@date) or not(@day))]">
  <xsl:variable name="ymd">
    <xsl:call-template name="compute-date">
      <xsl:with-param name="day-number" select="@day-number"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:variable name="md">
    <xsl:value-of select="substring-after($ymd, '-')"/>
  </xsl:variable>
  <xsl:variable name="wday">
    <xsl:call-template name="compute-weekday">
      <xsl:with-param name="day-number" select="@day-number"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="sdate">
      <xsl:value-of select="$ymd"/>
    </xsl:attribute>
    <xsl:attribute name="year">
      <xsl:value-of select="substring-before($ymd, '-')"/>
    </xsl:attribute>
    <xsl:attribute name="month">
      <xsl:value-of select="substring-before($md, '-')"/>
    </xsl:attribute>
    <xsl:attribute name="date">
      <xsl:value-of select="substring-after($md, '-')"/>
    </xsl:attribute>
    <xsl:attribute name="day">
      <xsl:value-of select="$wday"/>
    </xsl:attribute>
    <xsl:attribute name="wdaynum">
      <xsl:call-template name="compute-weekdaynum">
        <xsl:with-param name="weekday" select="$wday"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
