<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:str="http://exslt.org/strings" exclude-result-prefixes="str">

<xsl:output method="xml" indent="yes"/>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="placename">

  <xsl:variable name="query" select="concat('http://sws.geonames.org/search?maxRows=20&amp;name_equals=', str:encode-uri(@name, true()))"/>
  <xsl:variable name="abbrev-query" select="concat('http://sws.geonames.org/search?maxRows=20&amp;&amp;name_equals=', str:encode-uri(@abbrev-for, true()))"/>
  <xsl:variable name="alt-query" select="concat('http://sws.geonames.org/search?maxRows=20&amp;&amp;name_equals=', str:encode-uri(@altname, true()))"/>

  <xsl:copy>
    <xsl:apply-templates select="@*"/>

    <xsl:apply-templates mode="extract" select="document($query)"/>
    <xsl:if test="@abbrev-for">
      <xsl:apply-templates mode="extract" select="document($abbrev-query)"/>
    </xsl:if>
    <xsl:if test="@altname">
      <xsl:apply-templates mode="extract" select="document($alt-query)"/>
    </xsl:if>

  </xsl:copy>
</xsl:template>

<xsl:template mode="extract" match="/">
  <xsl:apply-templates mode="extract" select="geonames/geoname"/>
</xsl:template>

<xsl:template mode="extract" match="geoname">
  <place>
    <xsl:apply-templates mode="extract" select="name"/>
    <xsl:apply-templates mode="extract" select="geonameId"/>
    <xsl:apply-templates mode="extract" select="fcl"/>
    <xsl:apply-templates mode="extract" select="lat"/>
    <xsl:apply-templates mode="extract" select="lng"/>
    <xsl:apply-templates mode="extract" select="countryCode"/>
  </place>
</xsl:template>

<xsl:template mode="extract" match="name">
  <xsl:attribute name="name"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="geonameId">
  <xsl:attribute name="gazref">geonames:<xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl[.='A']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="../fcode='PCLI'">country</xsl:when>
      <xsl:when test="../fcode='ADM1'">civila</xsl:when>
      <xsl:when test="../fcode='TERR' and ../name='Antarctica'">country</xsl:when>
      <xsl:otherwise>civil</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl[.='H']">
  <xsl:attribute name="type">water</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl[.='L']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="../fcode='CONT'">continent</xsl:when>
      <xsl:otherwise>rgn</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl[.='P']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="../fcode='PPLC'">pplc</xsl:when>
      <xsl:when test="../fcode='PPLA'">ppla</xsl:when>
      <xsl:otherwise>ppl</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl[.='R']">
  <xsl:attribute name="type">road</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl[.='S']">
  <xsl:attribute name="type">fac</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl[.='T']">
  <xsl:attribute name="type">
    <xsl:choose>
      <xsl:when test="starts-with(../fcode, 'ISL')">rgn</xsl:when>
      <xsl:otherwise>mtn</xsl:otherwise>
    </xsl:choose>
  </xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="fcl">
  <xsl:attribute name="type">other</xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="lat">
  <xsl:attribute name="lat"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="lng">
  <xsl:attribute name="long"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="countryCode">
  <xsl:attribute name="in-cc"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

</xsl:stylesheet>
