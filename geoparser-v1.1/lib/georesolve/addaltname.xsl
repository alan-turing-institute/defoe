<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="ent[@type~'^location|GPE|LOC|loc$' and parts/part[.~'[^A-Za-z ]'] and not(@altname)]">
  <xsl:variable name="altname" select='translate(parts/part, "&apos;.", "")'/>
  <xsl:copy>
    <xsl:attribute name="altname">
      <xsl:value-of select="$altname"/>
    </xsl:attribute>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<!-- delete one character location ents -->
<xsl:template match="ent[@type~'^location|GPE|LOC|loc$' and parts/part[.~'^.$']]">
</xsl:template>

</xsl:stylesheet>
