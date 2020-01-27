<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:str="http://exslt.org/strings" xmlns:xlink="http://www.w3.org/1999/xlink" exclude-result-prefixes="str xlink">

<xsl:output method="xml" indent="yes"/>

<xsl:param name="gazetteer"/>
<xsl:param name="host"/>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="placename">

  <xsl:variable name="query" select="concat($host, '/ws/search?maxRows=20&amp;name=', str:encode-uri(@name, true()), '&amp;searchVariants=true&amp;gazetteer=', $gazetteer)"/>
  <xsl:variable name="abbrev-query" select="concat($host, '/ws/search?maxRows=20&amp;name=', str:encode-uri(@abbrev-for, true()), '&amp;searchVariants=true&amp;gazetteer=', $gazetteer)"/>
  <xsl:variable name="alt-query" select="concat($host, '/ws/search?maxRows=20&amp;name=', str:encode-uri(@altname, true()), '&amp;searchVariants=true&amp;gazetteer=', $gazetteer)"/>

  <xsl:copy>
    <xsl:apply-templates select="@*"/>
<!--<xsl:message>about to do first query</xsl:message>-->
    <xsl:apply-templates mode="extract" select="document($query)"/>
    <xsl:if test="@abbrev-for">
<!--<xsl:message>about to do second query</xsl:message>-->
      <xsl:apply-templates mode="extract" select="document($abbrev-query)"/>
    </xsl:if>
    <xsl:if test="@altname">
<!--<xsl:message>about to do third query</xsl:message>-->
      <xsl:apply-templates mode="extract" select="document($alt-query)"/>
    </xsl:if>
<!--<xsl:message>done queries</xsl:message>-->

  </xsl:copy>
<!--<xsl:message>done placename</xsl:message>-->
</xsl:template>

<xsl:template mode="extract" match="/">
  <xsl:apply-templates mode="extract" select="unlock/feature"/>
</xsl:template>

<xsl:template mode="extract" match="feature">
  <place>
    <xsl:apply-templates mode="extract" select="name"/>
    <xsl:apply-templates mode="extract" select="identifier"/>
    <xsl:apply-templates mode="extract" select="unlockFeatureCode"/>
    <xsl:apply-templates mode="extract" select="gazetteer"/>
    <xsl:apply-templates mode="extract" select="uriins"/>
    <xsl:apply-templates mode="extract" select="uricdda"/>
    <xsl:apply-templates mode="extract" select="madsid"/>
    <xsl:apply-templates mode="extract" select="variantid"/>
    <xsl:apply-templates mode="extract" select="unlockfpsrc"/>
    <xsl:apply-templates mode="extract" select="adminLevel2"/>
    <xsl:call-template name="bounding-box"/>
    <xsl:apply-templates mode="extract" select="attestations"/>
  </place>
</xsl:template>

<xsl:template mode="extract" match="name">
  <xsl:attribute name="name"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="identifier">
  <xsl:attribute name="gazref">deep:<xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="gazetteer">
  <xsl:attribute name="gazetteer"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="uriins">
  <xsl:attribute name="uriins"><xsl:value-of select="@xlink:href"/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="uricdda">
  <xsl:attribute name="uricdda"><xsl:value-of select="@xlink:href"/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="madsid">
  <xsl:attribute name="madsid"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="variantid">
  <xsl:attribute name="variantid"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="unlockfpsrc">
  <xsl:attribute name="unlockfpsrc"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="adminLevel2">
  <xsl:attribute name="deepcounty"><xsl:value-of select="."/></xsl:attribute>
</xsl:template>

<xsl:template mode="extract" match="attestations">
  <xsl:copy>
    <xsl:apply-templates select="attestation"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="attestation">
  <xsl:copy>
    <xsl:apply-templates select="date|source"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="date|source">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template mode="extract" match="unlockFeatureCode">
  <xsl:variable name="type" select="document('')//type[starts-with(current(), @unlock)][1]"/>
  <xsl:choose>
    <xsl:when test="$type">
      <xsl:copy-of select="$type/@type"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:attribute name="type">civil</xsl:attribute>
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
  <type unlock="county" type="civila"/> 
  <type unlock="field name" type="fac"/> 
</foo:types>

</xsl:stylesheet>
