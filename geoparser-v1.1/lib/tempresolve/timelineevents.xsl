<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                              xmlns:str="http://exslt.org/strings"
                              extension-element-prefixes="str">

<!-- stylesheet to extract events from pipeline output file, formated for timeline display -->

<xsl:template match="/">
  <data date-time-format="iso8601">
  <xsl:text>&#10;</xsl:text> <!-- &#10; is the newline char -->
    <xsl:apply-templates select="/document/standoff/relations[@source='temprel']" />
  </data>
</xsl:template>

<xsl:template match="relations">
  <xsl:for-each select="relation[@type='simultaneous']">
  <!-- if there are no simultaneous results the events file will have an empty 'data' element -->
    <xsl:text>  </xsl:text>
    <event>
    <!--attributes needed: start, (end), (isDuration), title [there are others] -->

    <!--start, end and isDuration come from rb entity that is second argument to the relation-->
    <!--element content is whole sentence in which event occurs - also collected here-->
    <xsl:for-each select="argument[@arg2='true']">
      <xsl:call-template name="get_start">
        <xsl:with-param name="entid" select="@ref" />
      </xsl:call-template>
    </xsl:for-each>

    <!--title comes from relation's text attribute-->
    <xsl:attribute name="title">
      <xsl:value-of select="@text" />
    </xsl:attribute>

    <!--element content is whole sentence in which event occurs-->
    <xsl:text>&#10;    </xsl:text>
    <xsl:for-each select="argument[@arg1='true']">
      <xsl:call-template name="get_content">
        <xsl:with-param name="eventid" select="@ref" />
      </xsl:call-template>
    </xsl:for-each>
    <xsl:text>&#10;  </xsl:text>
    </event>
    <xsl:text>&#10;</xsl:text>
  </xsl:for-each>
</xsl:template>

<xsl:template name="get_start">
  <xsl:param name="entid" />
  <xsl:apply-templates select="/document/standoff/ents[@source='ner-rb']/ent[@id=$entid]" />
</xsl:template>

<xsl:template match="ents[@source='ner-rb']/ent">
  <!--entity that is 1st part of a simultaneous relation; should have sdate attribute-->
  <xsl:attribute name="start">
    <!-- dummy value in case sdate missing - event will be ignored by timeline  -->
    <xsl:if test="@sdate=false()">
      <xsl:value-of select="'0000-00-00'" />
    </xsl:if>
    <!--sdate attribute is already an ISO8601 format date, so no conversion needed-->
    <xsl:value-of select="concat(@sdate, 'T00:00:00Z')" />
  </xsl:attribute>
  <!--use end date iff present-->
  <xsl:if test="@edate=true()">
    <xsl:attribute name="end">
      <!--as for sdate, conversion is not now needed-->
      <xsl:value-of select="concat(@edate, 'T00:00:00Z')" />
    </xsl:attribute>
    <!--if end date is present this is a duration event-->
    <xsl:attribute name="isDuration">true</xsl:attribute>
  </xsl:if>
</xsl:template>

<xsl:template name="get_content">
  <xsl:param name="eventid" />
  <xsl:apply-templates select="/document/standoff/ents/ent[@id=$eventid]" />
</xsl:template>

<xsl:template match="ents[@source='events']/ent">
  <!--entity that is 2nd part of a simultaneous relation-->
  <xsl:call-template name="fetch_sentence">
    <xsl:with-param name="sw" select="parts/part[1]/@sw" />
  </xsl:call-template>
</xsl:template>

<xsl:template name="fetch_sentence">
  <!-- find the first word of the event (verb phrase) string -->
  <xsl:param name="sw" />
  <xsl:apply-templates select="//s/w[@id=$sw]" />
</xsl:template>

<xsl:template match="w">
  <!-- sentence wanted is the parent element of this "event" word -->
  <xsl:value-of select=".." />
</xsl:template>

</xsl:stylesheet>