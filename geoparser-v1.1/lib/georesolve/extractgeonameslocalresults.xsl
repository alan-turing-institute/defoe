<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:output method="xml" indent="yes"/>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="rows">
  <xsl:apply-templates select="row">
<!--    <xsl:sort select="@population" data-type="number" order="descending"/>
-->
  </xsl:apply-templates>
</xsl:template>

<xsl:template match="row">
 <xsl:if test="position() &lt;= 20">
  <place>
    <xsl:apply-templates mode="extract" select="@name"/>
    <xsl:apply-templates mode="extract" select="@geonameId"/>
    <xsl:apply-templates mode="extract" select="@plid"/>
    <xsl:apply-templates mode="extract" select="@fclass"/>
    <xsl:apply-templates mode="extract" select="@latitude"/>
    <xsl:apply-templates mode="extract" select="@longitude"/>
    <xsl:apply-templates mode="extract" select="@country"/>
    <xsl:apply-templates mode="extract" select="@population"/>
  </place>
 </xsl:if>
</xsl:template>

<xsl:template mode="extract" match="@population">
  <xsl:attribute name="pop"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@name">
  <xsl:attribute name="name"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@geonameId">
  <xsl:attribute name="gazref">geonames:<xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@plid">
  <xsl:attribute name="gazref">pleiades:<xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass[.='A']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="../@fcode='PCLI'">country</xsl:when>
      <xsl:when test="../@fcode='ADM1'">civila</xsl:when>
      <xsl:when test="../@fcode='TERR' and ../@name='Antarctica'">country</xsl:when>
      <xsl:otherwise>civil</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass[.='H']">
  <xsl:attribute name="type">water</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass[.='L']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="../@fcode='CONT'">continent</xsl:when>
      <xsl:otherwise>rgn</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass[.='P']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="../@fcode='PPLC'">pplc</xsl:when>
      <xsl:when test="../@fcode='PPLA'">ppla</xsl:when>
      <xsl:otherwise>ppl</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass[.='R']">
  <xsl:attribute name="type">road</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass[.='S']">
  <xsl:attribute name="type">fac</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass[.='T']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="starts-with(../@fcode, 'ISL')">rgn</xsl:when>
      <xsl:otherwise>mtn</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@fclass">
  <xsl:attribute name="type">other</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@latitude">
  <xsl:attribute name="lat"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@longitude">
  <xsl:attribute name="long"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="@country">
  <xsl:attribute name="in-cc"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

</xsl:stylesheet>
