<!-- Convert inline markup to standoff. -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="standoff">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
    <xsl:text>&#10;</xsl:text>
    <ents source="events">
      <xsl:apply-templates select="//vg|//ng" mode="standoff"/>
      <xsl:text>&#10;</xsl:text>
    </ents>
  </xsl:copy>
</xsl:template>

<xsl:template mode="standoff" match="vg">
  <xsl:text>&#10;  </xsl:text>
  <ent type="event">
    <xsl:variable name="head">
      <xsl:value-of select="w[@headv][last()]"/>
    </xsl:variable>
    <xsl:variable name="lemma">
      <xsl:value-of select="w[@headv][last()]/@l"/>
    </xsl:variable>
    <xsl:variable name="id">
      <xsl:value-of select="w[@headv][last()]/@id"/>
    </xsl:variable>
    <xsl:attribute name="subtype">
       <xsl:value-of select="$lemma"/>
    </xsl:attribute>
    <xsl:apply-templates select="@*"/>
    <parts><part>
    <xsl:attribute name="sw">
       <xsl:value-of select="$id"/>
    </xsl:attribute>
    <xsl:attribute name="ew">
       <xsl:value-of select="$id"/>
    </xsl:attribute>
    <xsl:value-of select="$head"/>
  </part></parts></ent>
</xsl:template>

<xsl:template mode="standoff" match="ng">
  <xsl:text>&#10;  </xsl:text>
  <ent type="event">
    <xsl:variable name="head">
      <xsl:value-of select="w[@headn][last()]"/>
    </xsl:variable>
    <xsl:variable name="vstem">
      <xsl:value-of select="w[@headn][last()]/@vstem"/>
    </xsl:variable>
    <xsl:variable name="id">
      <xsl:value-of select="w[@headn][last()]/@id"/>
    </xsl:variable>
    <xsl:attribute name="nominal">true</xsl:attribute>
    <xsl:attribute name="subtype">
       <xsl:value-of select="$vstem"/>
    </xsl:attribute>
    <xsl:apply-templates select="@*"/>
    <parts><part>
    <xsl:attribute name="sw">
       <xsl:value-of select="$id"/>
    </xsl:attribute>
    <xsl:attribute name="ew">
       <xsl:value-of select="$id"/>
    </xsl:attribute>
    <xsl:value-of select="$head"/>
  </part></parts></ent>
</xsl:template>

</xsl:stylesheet>
