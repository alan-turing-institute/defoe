<!-- add entries from the xwalk add-on gazetteer -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:key name="byname" match="place" 
	 use="translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="placename">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>

    <xsl:variable name="name" 
        select="translate(@name, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>
    <xsl:variable name="abbrev-for" 
        select="translate(@abbrev-for, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>
    <xsl:variable name="altname" 
        select="translate(@altname, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')"/>

    <xsl:for-each select="document('xwalk-extras.xml')"> <!-- to set context -->
      <xsl:copy-of select="key('byname', $name)"/>
      <xsl:if test="$abbrev-for != ''">
          <xsl:copy-of select="key('byname', $abbrev-for)"/>
      </xsl:if>
      <xsl:if test="$altname != ''">
          <xsl:copy-of select="key('byname', $altname)"/>
      </xsl:if>
    </xsl:for-each>

  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
