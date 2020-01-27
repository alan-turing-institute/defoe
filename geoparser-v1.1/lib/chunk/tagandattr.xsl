<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:template match="rg|pg|ag|sg">
  <xsl:apply-templates select="node()"/>
</xsl:template>

<xsl:template match="ng[not(w[last()][.~'^[a-z]' and @headn and @event and @tmln])]">
  <xsl:apply-templates select="node()"/>
</xsl:template>

<xsl:template match="vg[.~'^.+going$' and following-sibling::*[1][self::vg and @tense='inf']]">
  <xsl:apply-templates select="node()"/>
</xsl:template>

<xsl:template match="vg|ng">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<!-- use this to mark the first word of all verb groups as B-VP -->
<xsl:template match="vg//w[1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">B-VP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- use this when B-VP is only used to signal start of VP after a VP -->
<!--<xsl:template match="vg//w[1]">
  <xsl:choose>
    <xsl:when test="../preceding-sibling::*[1][self::vg]">
      <xsl:copy>
        <xsl:apply-templates select="@*"/>
        <xsl:attribute name="group">B-VP</xsl:attribute>
        <xsl:apply-templates select="node()"/>
      </xsl:copy>
    </xsl:when>
    <xsl:otherwise>
      <xsl:copy>
        <xsl:apply-templates select="@*"/>
        <xsl:attribute name="group">I-VP</xsl:attribute>
        <xsl:apply-templates select="node()"/>
      </xsl:copy>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>-->

<!-- all non-initial words in verb groups marked as I-VP -->
<xsl:template match="vg//w[position() > 1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">I-VP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- use this to mark the first word of all noun groups as B-NP -->
<xsl:template match="ng//w[1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">B-NP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- use this when B-NP is only used to signal start of NP after a NP -->
<!--<xsl:template match="ng//w[1]">
  <xsl:choose>
    <xsl:when test="../preceding-sibling::*[1][self::ng]">
      <xsl:copy>
        <xsl:apply-templates select="@*"/>
        <xsl:attribute name="group">B-NP</xsl:attribute>
        <xsl:apply-templates select="node()"/>
      </xsl:copy>
    </xsl:when>
    <xsl:otherwise>
      <xsl:copy>
        <xsl:apply-templates select="@*"/>
        <xsl:attribute name="group">I-NP</xsl:attribute>
        <xsl:apply-templates select="node()"/>
      </xsl:copy>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>-->

<!-- all non-initial words in noun groups marked as I-NP -->
<xsl:template match="ng//w[position() > 1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">I-NP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- use this to mark the first word of all adverb groups as B-ADVP -->
<xsl:template match="rg//w[1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">B-ADVP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- all non-initial words in adverb groups marked as I-ADVP -->
<xsl:template match="rg//w[position() > 1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">I-ADVP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- use this to mark the first word of all adjective groups as B-ADJP -->
<xsl:template match="ag//w[1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">B-ADJP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- all non-initial words in adjective groups marked as I-ADJP -->
<xsl:template match="ag//w[position() > 1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">I-ADJP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- use this to mark the first word of all preposition groups as B-PP -->
<xsl:template match="pg//w[1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">B-PP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- all non-initial words in preposition groups marked as I-PP -->
<xsl:template match="pg//w[position() > 1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">I-PP</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- use this to mark the first word of all complementiser groups as B-SBAR -->
<xsl:template match="sg//w[1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">B-SBAR</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- all non-initial words in complementiser groups marked as I-SBAR -->
<xsl:template match="sg//w[position() > 1]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">I-SBAR</xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- all other words marked as O -->
<xsl:template match="w">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="group">O</xsl:attribute>
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
