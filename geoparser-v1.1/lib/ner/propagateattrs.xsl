<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="timex[@type='date' and @unit='quarter']">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select='w/@month'/>
    <xsl:apply-templates select='w/@date'/>
    <xsl:apply-templates select='*/@year'/>
    <xsl:apply-templates select='w/@season'/>
    <xsl:apply-templates select='w/@day'/>
    <xsl:apply-templates select='w/@wdaynum'/>
    <xsl:apply-templates select='w/@trel'/>
    <xsl:apply-templates select='w/@unit'/>
    <xsl:apply-templates select='*[not(@year)]/@quty'/>
    <xsl:apply-templates select='w/@sdate'/>
    <xsl:apply-templates select='w/@tref'/>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="timex[@type='date']">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select='w/@month'/>
    <xsl:apply-templates select='w/@date'/>
    <xsl:apply-templates select='*/@year'/>
    <xsl:apply-templates select='w/@season'/>
    <xsl:apply-templates select='w/@day'/>
    <xsl:apply-templates select='w/@wdaynum'/>
    <xsl:apply-templates select='w/@trel'/>
    <xsl:apply-templates select='w/@unit'/>
    <xsl:apply-templates select='*/@quty'/>
    <xsl:apply-templates select='w/@sdate'/>
    <xsl:apply-templates select='w/@tref'/>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="timex[@type='time']">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select='w/@trel'/>
    <xsl:apply-templates select='w/@unit'/>
    <xsl:apply-templates select='*/@quty'/>
    <xsl:apply-templates select='w/@tval'/>
    <xsl:if test="not(w[@tval]) and w[.~'[0-9]']">
      <xsl:attribute name="tval">
        <xsl:value-of select="translate(w[.~'[0-9]'], '.', ':')"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="not(w[@tval]) and not(w[.~'[0-9]']) and w[@quty]">
      <xsl:attribute name="tval">
        <xsl:value-of select="w[@quty]/@quty"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:if test="not(w[@tval]) and w[.~'^[0-9][0-9][0-9][0-9]$']">
      <xsl:attribute name="tval">
        <xsl:value-of select="substring(w[.~'^[0-9][0-9][0-9][0-9]$'], 1, 2)"/>
        <xsl:text>:</xsl:text>
        <xsl:value-of select="substring(w[.~'^[0-9][0-9][0-9][0-9]$'], 3, 2)"/>
      </xsl:attribute>
    </xsl:if>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="timex[@type='set']">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select='w/@month'/>
    <xsl:apply-templates select='w/@date'/>
    <xsl:apply-templates select='*/@year'/>
    <xsl:apply-templates select='w/@season'/>
    <xsl:apply-templates select='w/@day'/>
    <xsl:apply-templates select='w/@wdaynum'/>
    <xsl:apply-templates select='w/@trel'/>
    <xsl:apply-templates select='w/@unit'/>
    <xsl:apply-templates select='*/@quty'/>
    <xsl:apply-templates select='w/@sdate'/>
    <xsl:apply-templates select='w/@tref'/>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>

