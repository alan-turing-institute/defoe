<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="phr[@c='cd'][tw or w/@quty]">
  <xsl:copy>
    <xsl:attribute name="quty">
      <xsl:apply-templates mode="eval" select="tw | w[@quty]"/>
    </xsl:attribute>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="w[@quty]" mode="eval">
  <xsl:value-of select="@quty"/>
</xsl:template>

<xsl:template mode="eval" match="tw">
  <xsl:choose>
    <xsl:when test="count(tw | w[@quty]) = 2">
      <xsl:variable name="op1">
	<xsl:apply-templates mode="eval" select="(tw|w[@quty])[1]"/>
      </xsl:variable>
      <xsl:variable name="op2">
	<xsl:apply-templates mode="eval" select="(tw|w[@quty])[2]"/>
      </xsl:variable>
      <xsl:choose>
	<xsl:when test="@op = '+'">
	  <xsl:value-of select="$op1 + $op2"/>
	</xsl:when>
	<xsl:when test="@op = '*'">
	  <xsl:value-of select="$op1 * $op2"/>
	</xsl:when>
	<xsl:otherwise>
	  <xsl:message>bad op in
	    <xsl:copy-of select="."/></xsl:message>
	  <xsl:text>NaN</xsl:text>
	</xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:message>wrong number of operands in
	<xsl:copy-of select="."/></xsl:message>
      <xsl:text>NaN</xsl:text>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

</xsl:stylesheet>

