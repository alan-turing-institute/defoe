<!-- Convert dates to day numbers and back. -->

<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:c="http://ltg.ed.ac.uk">

<xsl:variable name="four-years" select="4 * 365 + 1"/>
<xsl:variable name="hundred-years" select="25 * $four-years - 1"/>
<xsl:variable name="four-hundred-years" select="4 * $hundred-years + 1"/>

<!-- convert a day, month, and year to a number and output it -->

<xsl:template name="compute-day-number">
  <xsl:param name="day"/>
  <xsl:param name="month"/>
  <xsl:param name="year"/>
  <xsl:variable name="year-days" select="($year - 1) * 365 + floor(($year - 1) div 4) - floor(($year - 1) div 100) + floor(($year - 1) div 400)"/>
  <xsl:choose>
    <xsl:when test="$year mod 4 = 0 and ($year mod 100 != 0 or $year mod 400 = 0)">
      <xsl:value-of select="$year-days + document('')//c:leap/c[position()=$month] + $day - 1"/>
    </xsl:when>
    <xsl:otherwise>
      <xsl:value-of select="$year-days + document('')//c:normal/c[position()=$month] + $day - 1"/>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<!-- output the weekday (Monday etc) of a day number -->

<xsl:template name="compute-weekday">
  <xsl:param name="day-number"/>
  <xsl:value-of select="document('')//c:daynames/d[position() = ($day-number mod 7) + 1]"/>
</xsl:template>

<!-- output a number for a weekday (Sunday=1) -->

<xsl:template name="compute-weekdaynum">
  <xsl:param name="weekday"/>
  <xsl:if test="$weekday='Sunday'">
    <xsl:value-of select="7"/>
  </xsl:if>
  <xsl:if test="$weekday='Monday'">
    <xsl:value-of select="1"/>
  </xsl:if>
  <xsl:if test="$weekday='Tuesday'">
    <xsl:value-of select="2"/>
  </xsl:if>
  <xsl:if test="$weekday='Wednesday'">
    <xsl:value-of select="3"/>
  </xsl:if>
  <xsl:if test="$weekday='Thursday'">
    <xsl:value-of select="4"/>
  </xsl:if>
  <xsl:if test="$weekday='Friday'">
    <xsl:value-of select="5"/>
  </xsl:if>
  <xsl:if test="$weekday='Saturday'">
    <xsl:value-of select="6"/>
  </xsl:if>
</xsl:template>

<!-- given a day number, output the date as y-m-d -->

<xsl:template name="compute-date">
  <xsl:param name="day-number"/>
  <xsl:call-template name="compute-date-100">
    <xsl:with-param name="year" select="400 * floor($day-number div $four-hundred-years) + 1"/>
    <xsl:with-param name="day-number" select="$day-number mod $four-hundred-years"/>
  </xsl:call-template>
</xsl:template>

<xsl:template name="compute-date-100">
  <xsl:param name="day-number"/>
  <xsl:param name="year"/>
  <xsl:choose>
    <xsl:when test="$day-number = $four-hundred-years - 1">
      <xsl:value-of select="$year+399"/>
      <xsl:text>-12-31</xsl:text>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="compute-date-4">
        <xsl:with-param name="year" select="$year + 100 * floor($day-number div $hundred-years)"/>
        <xsl:with-param name="day-number" select="$day-number mod $hundred-years"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="compute-date-4">
  <xsl:param name="day-number"/>
  <xsl:param name="year"/>
  <xsl:call-template name="compute-date-1">
    <xsl:with-param name="year" select="$year + 4 *floor($day-number div $four-years)"/>
    <xsl:with-param name="day-number" select="$day-number mod $four-years"/>
  </xsl:call-template>
</xsl:template>

<xsl:template name="compute-date-1">
  <xsl:param name="day-number"/>
  <xsl:param name="year"/>
  <xsl:choose>
    <xsl:when test="$day-number = $four-years - 1">
      <xsl:value-of select="$year+3"/>
      <xsl:text>12-31</xsl:text>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="compute-month">
        <xsl:with-param name="year" select="$year + floor($day-number div 365)"/>
        <xsl:with-param name="day-number" select="$day-number mod 365"/>
        <xsl:with-param name="month" select="1"/>
        <xsl:with-param name="months" select="document('')//c:leap/*"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="compute-month">
  <xsl:param name="day-number"/>
  <xsl:param name="year"/>
  <xsl:param name="month"/>
  <xsl:choose>
    <xsl:when test="$year mod 4 = 0 and ($year mod 100 != 0 or $year mod 400 = 0)">
      <xsl:call-template name="compute-month-1">
        <xsl:with-param name="year" select="$year"/>
        <xsl:with-param name="day-number" select="$day-number mod 365"/>
        <xsl:with-param name="month" select="1"/>
        <xsl:with-param name="months" select="document('')//c:leap/*"/>
      </xsl:call-template>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="compute-month-1">
        <xsl:with-param name="year" select="$year"/>
        <xsl:with-param name="day-number" select="$day-number mod 365"/>
        <xsl:with-param name="month" select="1"/>
        <xsl:with-param name="months" select="document('')//c:normal/*"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<xsl:template name="compute-month-1">
  <xsl:param name="day-number"/>
  <xsl:param name="year"/>
  <xsl:param name="month"/>
  <xsl:param name="months"/>
  <xsl:choose>
    <xsl:when test="$day-number &lt; $months[position() = $month+1]">
      <xsl:variable name="day">
        <xsl:value-of select="$day-number - $months[position() = $month] + 1"/>
      </xsl:variable>
      <xsl:value-of select="$year"/>
      <xsl:text>-</xsl:text>
      <xsl:choose>
        <xsl:when test="$month &lt; 10">
          <xsl:text>0</xsl:text>
          <xsl:value-of select="$month"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$month"/>
        </xsl:otherwise>
      </xsl:choose>
      <xsl:text>-</xsl:text>
      <xsl:choose>
        <xsl:when test="$day &lt; 10">
          <xsl:text>0</xsl:text>
          <xsl:value-of select="$day"/>
        </xsl:when>
        <xsl:otherwise>
          <xsl:value-of select="$day"/>
        </xsl:otherwise>
      </xsl:choose>
    </xsl:when>
    <xsl:otherwise>
      <xsl:call-template name="compute-month-1">
        <xsl:with-param name="year" select="$year"/>
        <xsl:with-param name="day-number" select="$day-number"/>
        <xsl:with-param name="month" select="$month+1"/>
        <xsl:with-param name="months" select="$months"/>
      </xsl:call-template>
    </xsl:otherwise>
  </xsl:choose>
</xsl:template>

<c:normal>
  <c>0</c>
  <c>31</c>
  <c>59</c>
  <c>90</c>
  <c>120</c>
  <c>151</c>
  <c>181</c>
  <c>212</c>
  <c>243</c>
  <c>273</c>
  <c>304</c>
  <c>334</c>
  <c>365</c>
</c:normal>

<c:leap>
  <c>0</c>
  <c>31</c>
  <c>60</c>
  <c>91</c>
  <c>121</c>
  <c>152</c>
  <c>182</c>
  <c>213</c>
  <c>244</c>
  <c>274</c>
  <c>305</c>
  <c>335</c>
  <c>365</c>
</c:leap>

<c:daynames>
  <d>Monday</d>
  <d>Tuesday</d>
  <d>Wednesday</d>
  <d>Thursday</d>
  <d>Friday</d>
  <d>Saturday</d>
  <d>Sunday</d>
</c:daynames>

</xsl:stylesheet>
