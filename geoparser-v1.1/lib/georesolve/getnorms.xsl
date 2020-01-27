<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:param name="georesfile" select="''"/>
<xsl:key name="placename" match="placename" use="@name"/>

<xsl:template match="standoff">
  <xsl:copy>
    <xsl:if test="$georesfile=''">
      <xsl:message terminate="yes">$georesfile not set</xsl:message>
    </xsl:if>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="ent[@type~'(GPE|LOC|loc|location|Location|Country|City)']">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:variable name="ent">
      <xsl:value-of select="normalize-space(.)"/>
    </xsl:variable>
    <xsl:for-each select="document($georesfile, .)"> 
      <xsl:for-each select="key('placename', $ent)">
        <xsl:attribute name="lat">
          <xsl:value-of select="place[@rank='1']/@lat"/>
        </xsl:attribute>
        <xsl:attribute name="long">
          <xsl:value-of select="place[@rank='1']/@long"/>
        </xsl:attribute>
        <xsl:attribute name="gazref">
          <xsl:value-of select="place[@rank='1']/@gazref"/>
        </xsl:attribute>
        <xsl:if test="place[@rank='1']/@uirins">
          <xsl:attribute name="uriins">
            <xsl:value-of select="place[@rank='1']/@uriins"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="place[@rank='1']/@uricdda">
          <xsl:attribute name="uricdda">
            <xsl:value-of select="place[@rank='1']/@uricdda"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="place[@rank='1']/@in-cc">
          <xsl:attribute name="in-country">
            <xsl:value-of select="place[@rank='1']/@in-cc"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="place[@rank='1']/@type">
          <xsl:attribute name="feat-type">
            <xsl:value-of select="place[@rank='1']/@type"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="place[@rank='1']/@pop">
          <xsl:attribute name="pop-size">
            <xsl:value-of select="place[@rank='1']/@pop"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:for-each>
    </xsl:for-each>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- identity transform -->

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
