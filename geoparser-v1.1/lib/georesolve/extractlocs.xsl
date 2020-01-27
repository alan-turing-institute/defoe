<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" indent="yes"/>

<xsl:key name="loc-by-name" match="ent[@type~'location|GPE|LOC|loc|Location|City|Country']" use="normalize-space(.)"/>
<xsl:key name="loc-by-id" match="ent[@type~'location|GPE|LOC|loc|Location|City|Country']" use="@id"/>

<xsl:template match="/">
  <placenames>
    <xsl:apply-templates select="//ent[@type~'location|GPE|LOC|loc|Location|City|Country']"/>	
  </placenames>
</xsl:template>

<xsl:template match="ent[@type~'location|GPE|LOC|loc|Location|City|Country']">
  <xsl:variable name="dups" select="key('loc-by-name', normalize-space(.))"/>
  <xsl:if test="count(. | $dups[1]) = 1">
    <xsl:variable name="near" select="key('loc-by-id', $dups/@near)"/>
    <xsl:variable name="contained-by" select="key('loc-by-id', $dups/@contained-by)"/>
    <xsl:variable name="contains" select="key('loc-by-id', $dups/@contains)"/>
    <placename name="{normalize-space(.)}" id="{@id}">

      <xsl:if test="$near">
        <xsl:attribute name="near">
          <xsl:value-of select="key('loc-by-name', normalize-space($near[1]))/@id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="$contains">
        <xsl:attribute name="contains">
          <xsl:value-of select="key('loc-by-name', normalize-space($contains[1]))/@id"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="$contained-by">
        <xsl:attribute name="contained-by">
          <xsl:value-of select="key('loc-by-name', normalize-space($contained-by[1]))/@id"/>
        </xsl:attribute>
      </xsl:if>

      <xsl:copy-of select="($dups/@altname)[1]"/>
      <xsl:copy-of select="($dups/@abbrev-for)[1]"/>

    </placename>
  </xsl:if>
</xsl:template>

</xsl:stylesheet>
