<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:str="http://exslt.org/strings" exclude-result-prefixes="str">

<xsl:output method="xml" indent="yes"/>

<xsl:param name="gazetteer"/>
<xsl:param name="host"/>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="placename">

  <xsl:variable name="query" select="concat($host, '/ws/search?maxRows=20&amp;name=', str:encode-uri(@name, true()), '&amp;gazetteer=', $gazetteer)"/>
  <xsl:variable name="abbrev-query" select="concat($host, '/ws/search?maxRows=20&amp;name=', str:encode-uri(@abbrev-for, true()), '&amp;gazetteer=', $gazetteer)"/>
  <xsl:variable name="alt-query" select="concat($host, '/ws/search?maxRows=20&amp;name=', str:encode-uri(@altname, true()), '&amp;gazetteer=', $gazetteer)"/>

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
  <xsl:apply-templates mode="extract" select="unlock/feature[gazetteer!='Meridian2/MasterMap']"/>
</xsl:template>

<xsl:template mode="extract" match="feature">
  <place>
    <xsl:apply-templates mode="extract" select="name"/>
    <xsl:apply-templates mode="extract" select="identifier"/>
    <xsl:apply-templates mode="extract" select="unlockFeatureCode"/>
    <xsl:apply-templates mode="extract" select="gazetteer"/>
    <xsl:call-template name="bounding-box"/>
  </place>
</xsl:template>

<xsl:template mode="extract" match="name">
  <xsl:attribute name="name"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="identifier">
  <xsl:attribute name="gazref">unlock:<xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="gazetteer">
  <xsl:attribute name="gazetteer"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="unlockFeatureCode">
  <xsl:variable name="type" select="document('')//type[starts-with(current(), @unlock)][1]"/>
  <xsl:choose>
    <xsl:when test="$type">
      <xsl:copy-of select="$type/@type"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:attribute name="type">other</xsl:attribute>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="bounding-box">
  <xsl:attribute name="lat">
    <xsl:value-of select="(miny + maxy) div 2"/>
  </xsl:attribute>
  <xsl:attribute name="long">
    <xsl:value-of select="(minx + maxx) div 2"/>
  </xsl:attribute>
</xsl:template>

<!-- XXX improve this list -->

<foo:types xmlns:foo="http://example.org">
  <type unlock="EDINA.A" type="other"/> 
  <type unlock="EDINA.B.D.C.B" type="civila"/> 
  <type unlock="EDINA.B.D.C.C" type="civila"/> 
  <type unlock="EDINA.B" type="civil"/> 
  <type unlock="EDINA.C" type="water"/> 
  <type unlock="EDINA.D" type="other"/> 
  <type unlock="EDINA.E.V.B.B" type="ppla"/> 
  <type unlock="EDINA.E.V" type="ppl"/> 
  <type unlock="EDINA.E" type="fac"/> 
  <type unlock="EDINA.F" type="mtn"/> 
  <type unlock="EDINA.G" type="rgn"/> 
</foo:types>

</xsl:stylesheet>
