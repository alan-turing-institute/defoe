<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">

<xsl:import href="dates.xsl"/>

<xsl:key name="timex" match="timex" use="@id"/>

<xsl:variable name="docwdaynum">
  <xsl:value-of select="/document/meta/attr[@name='docdate']/@wdaynum"/>
</xsl:variable>

<xsl:variable name="docdaynum">
  <xsl:value-of select="/document/meta/attr[@name='docdate']/@day-number"/>
</xsl:variable>

<xsl:variable name="docdate">
  <xsl:value-of select="/document/meta/attr[@name='docdate']/@date"/>
</xsl:variable>

<xsl:variable name="docmonth">
  <xsl:value-of select="/document/meta/attr[@name='docdate']/@month"/>
</xsl:variable>

<xsl:variable name="docyear">
  <xsl:value-of select="/document/meta/attr[@name='docdate']/@year"/>
</xsl:variable>

<xsl:template match="node()|@*">
  <xsl:copy>
    <xsl:apply-templates select="node()|@*"/>
  </xsl:copy>
</xsl:template>

<!-- next August, this September, in February -->
<xsl:template match="ent[@month~'.' and not(@year) and not(@date)]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
      <xsl:if test="key('timex', @id)[@docdaterel='before']">
        <xsl:if test="@month=$docmonth and (@trel='same' or not(@trel))">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month=$docmonth and @trel='before'">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear - 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month=$docmonth and @trel='after'">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear + 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &lt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &gt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear - 1"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="key('timex', @id)[@docdaterel='after']">
        <xsl:if test="@month=$docmonth and (@trel='same' or not(@trel))">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month=$docmonth and @trel='before'">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear - 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month=$docmonth and @trel='after'">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear + 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &lt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear + 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &gt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="not(key('timex', @id)[@docdaterel])">
        <xsl:attribute name="year">
          <xsl:value-of select="$docyear"/>
        </xsl:attribute>
      </xsl:if>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- last March 16, on Feb. 8th -->
<xsl:template match="ent[@month~'.' and @date~'.' and not(@year)]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
      <xsl:if test="key('timex', @id)[@docdaterel='before']">
        <xsl:if test="@month=$docmonth and @date &lt;= $docdate">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month=$docmonth and @date &gt; $docdate">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear - 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &lt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &gt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear - 1"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="key('timex', @id)[@docdaterel='after']">
        <xsl:if test="@month=$docmonth and @date &lt;= $docdate">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear + 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month=$docmonth and @date &gt; $docdate">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month=$docmonth and @date = $docdate">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &lt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear + 1"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@month &gt; $docmonth">
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="not(key('timex', @id)[@docdaterel])">
        <xsl:attribute name="year">
          <xsl:value-of select="$docyear"/>
        </xsl:attribute>
      </xsl:if>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- last Tuesday, next Wednesday, Friday -->
<xsl:template match="ent[@day~'.' and not(@date)]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
      <xsl:if test="key('timex', @id)[@docdaterel='before']">
        <xsl:if test="@wdaynum=$docwdaynum">
          <xsl:attribute name="day-number">
            <xsl:value-of select="$docdaynum"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@wdaynum &lt; $docwdaynum">
          <xsl:attribute name="day-number">
            <xsl:value-of select="$docdaynum - ($docwdaynum - @wdaynum)"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@wdaynum &gt; $docwdaynum">
          <xsl:attribute name="day-number">
            <xsl:value-of select="($docdaynum + (@wdaynum - $docwdaynum)) - 7"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="key('timex', @id)[@docdaterel='after']">
        <xsl:if test="@wdaynum=$docwdaynum">
          <xsl:attribute name="day-number">
            <xsl:value-of select="$docdaynum"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@wdaynum &lt; $docwdaynum">
          <xsl:attribute name="day-number">
            <xsl:value-of select="($docdaynum - ($docwdaynum - @wdaynum)) + 7"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="@wdaynum &gt; $docwdaynum">
          <xsl:attribute name="day-number">
            <xsl:value-of select="$docdaynum + (@wdaynum - $docwdaynum)"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="not(key('timex', @id)[@docdaterel])">
        <xsl:if test="@wdaynum=$docwdaynum">
          <xsl:attribute name="day-number">
            <xsl:value-of select="$docdaynum"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<!-- yesterday, tomorrow, today -->
<!-- last month, next month, this month -->
<!-- last year, next year, this year -->
<!-- a year ago, three months ago -->
<!-- the constraint on initial 'the' is to block 'the past three months' -->

 
<xsl:template match="ent[not(.//part[.~'^the ']) and @type='date' and @trel and not(@date or @day or @month or @year)]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
      <xsl:if test="@trel='before' and @unit='day'">
        <xsl:attribute name="day-number">
          <xsl:value-of select="$docdaynum - @quty"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@trel='after' and @unit='day'">
        <xsl:attribute name="day-number">
          <xsl:value-of select="$docdaynum + @quty"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@trel='same' and @unit='day'">
        <xsl:attribute name="day-number">
          <xsl:value-of select="$docdaynum"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@trel='before' and @unit='year'">
        <xsl:attribute name="year">
          <xsl:value-of select="$docyear - @quty"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@trel='after' and @unit='year'">
        <xsl:attribute name="year">
          <xsl:value-of select="$docyear + @quty"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@trel='same' and @unit='year'">
        <xsl:attribute name="year">
          <xsl:value-of select="$docyear"/>
        </xsl:attribute>
      </xsl:if>
      <xsl:if test="@trel='before' and @unit='month'">
        <xsl:if test="(@quty mod 12) &lt; $docmonth">
          <xsl:attribute name="month">
            <xsl:value-of select="$docmonth - (@quty mod 12)"/>
          </xsl:attribute>
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear - floor(@quty div 12)"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="(@quty mod 12) &gt;= $docmonth">
          <xsl:attribute name="month">
            <xsl:value-of select="$docmonth + 12 - (@quty mod 12)"/>
          </xsl:attribute>
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear - 1 - floor(@quty div 12)"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="@trel='after' and @unit='month'">
        <xsl:if test="$docmonth + (@quty mod 12) &lt;= 12">
          <xsl:attribute name="month">
            <xsl:value-of select="$docmonth + (@quty mod 12)"/>
          </xsl:attribute>
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear + floor(@quty div 12)"/>
          </xsl:attribute>
        </xsl:if>
        <xsl:if test="$docmonth + (@quty mod 12) &gt; 12">
          <xsl:attribute name="month">
            <xsl:value-of select="$docmonth + (@quty mod 12) - 12"/>
          </xsl:attribute>
          <xsl:attribute name="year">
            <xsl:value-of select="$docyear + 1 + floor(@quty div 12)"/>
          </xsl:attribute>
        </xsl:if>
      </xsl:if>
      <xsl:if test="@trel='same' and @unit='month'">
        <xsl:attribute name="month">
          <xsl:value-of select="$docmonth"/>
        </xsl:attribute>
        <xsl:attribute name="year">
          <xsl:value-of select="$docyear"/>
        </xsl:attribute>
      </xsl:if>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="ent[@unit='quarter' and not(@year)]">
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="year">
      <xsl:value-of select="$docyear"/>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

<xsl:template match="ent[@day-number~'.' and not(@day)]">
  <xsl:variable name="wday">
    <xsl:call-template name="compute-weekday">
      <xsl:with-param name="day-number" select="@day-number"/>
    </xsl:call-template>
  </xsl:variable>
  <xsl:copy>
    <xsl:apply-templates select="@*"/>
    <xsl:attribute name="day">
      <xsl:value-of select="$wday"/>
    </xsl:attribute>
    <xsl:attribute name="wdaynum">
      <xsl:call-template name="compute-weekdaynum">
        <xsl:with-param name="weekday" select="$wday"/>
      </xsl:call-template>
    </xsl:attribute>
    <xsl:apply-templates select="node()"/>
  </xsl:copy>
</xsl:template>

</xsl:stylesheet>
