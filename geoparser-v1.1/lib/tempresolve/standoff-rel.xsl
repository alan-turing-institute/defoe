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
    <relations source="temprel">
      <xsl:apply-templates select="//reln" mode="standoff"/>
      <xsl:text>&#10;</xsl:text>
    </relations>
  </xsl:copy>
</xsl:template>

<xsl:template match="w">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="s//*[not(self::w)]">
  <xsl:apply-templates select="node()"/>
</xsl:template>

<xsl:template mode="standoff" match="reln[@type='simultaneous']">
  <xsl:text>&#10;  </xsl:text>
  <relation>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="text">
       <xsl:value-of select="normalize-space(.)"/>
    </xsl:attribute>
    <xsl:text>&#10;    </xsl:text>
    <argument arg1="true">
      <xsl:attribute name="ref">
        <xsl:value-of select="vg/@id|ng/@id"/>
      </xsl:attribute>
    </argument>
    <xsl:text>&#10;    </xsl:text>
    <argument arg2="true">
      <xsl:attribute name="ref">
        <xsl:value-of select="timex/@id"/>
      </xsl:attribute>
    </argument>
  <xsl:text>&#10;  </xsl:text>
  </relation>
</xsl:template>

<xsl:template mode="standoff" match="reln[@type='before']">
  <xsl:text>&#10;  </xsl:text>
  <relation>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="text">
       <xsl:value-of select="normalize-space(.)"/>
    </xsl:attribute>
    <xsl:text>&#10;    </xsl:text>
    <argument arg1="true">
      <xsl:attribute name="ref">
        <xsl:value-of select="vg[@eventarg1]/@id|ng[@eventarg1]/@id"/>
      </xsl:attribute>
    </argument>
    <xsl:text>&#10;    </xsl:text>
    <argument arg2="true">
      <xsl:attribute name="ref">
        <xsl:value-of select="vg[@eventarg2]/@id|ng[@eventarg2]/@id"/>
      </xsl:attribute>
    </argument>
  <xsl:text>&#10;  </xsl:text>
  </relation>
</xsl:template>

<xsl:template mode="standoff" match="reln[@type='beforeorincl']">
  <xsl:text>&#10;  </xsl:text>
  <relation>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="text">
       <xsl:value-of select="normalize-space(.)"/>
    </xsl:attribute>
    <xsl:text>&#10;    </xsl:text>
    <argument arg1="true">
      <xsl:attribute name="ref">
        <xsl:value-of select="vg/@id"/>
      </xsl:attribute>
    </argument>
    <xsl:text>&#10;    </xsl:text>
    <argument arg2="true">
      <xsl:attribute name="ref">docdate</xsl:attribute>
    </argument>
  <xsl:text>&#10;  </xsl:text>
  </relation>
</xsl:template>

</xsl:stylesheet>
