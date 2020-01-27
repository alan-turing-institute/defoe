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
  	<ents source="ner-rb">
      <xsl:apply-templates select="//s//enamex[@type='location' or @type='person']|//s//timex" mode="standoff"/>
      <xsl:text>&#10;</xsl:text>
  	</ents>
  </xsl:copy>
</xsl:template>

<xsl:template match="w">
  <xsl:copy>
    <xsl:apply-templates select="@*[name() != 'ne']"/>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!--<xsl:template match="s//*[not(self::w)]">
  <xsl:apply-templates select="node()"/>
</xsl:template>-->

<xsl:template mode="standoff" match="*">
  <xsl:text>&#10;  </xsl:text>
  <ent>
    <xsl:apply-templates select="@*"/>
    <xsl:text>&#10;    </xsl:text>
    <parts>
    <xsl:text>&#10;      </xsl:text>
    <part>
    <xsl:attribute name="sw">
       <xsl:value-of select="(.//w)[1]/@id"/>
    </xsl:attribute>
    <xsl:attribute name="ew">
       <xsl:value-of select="(.//w)[last()]/@id"/>
    </xsl:attribute>
    <xsl:value-of select="normalize-space(.)"/>
    </part>
    <xsl:text>&#10;    </xsl:text>
    </parts>
    <xsl:text>&#10;  </xsl:text>
  </ent>
</xsl:template>

</xsl:stylesheet>
