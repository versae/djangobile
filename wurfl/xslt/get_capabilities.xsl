<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:common="http://exslt.org/common">

  <xsl:output method="xml"
	      encoding="ISO-8859-1"
	      indent="yes"/>
  
  <!--
    	get all capabilities for one UserAgentselected useragent
      send comments, questions to roland guelle <roldriguez@users.sourceforge.net>
  -->

  <xsl:param name="ua"></xsl:param>
  
  <xsl:template match="/wurfl/devices">
    <xsl:choose>
      <xsl:when test="device[@user_agent=$ua]/@id = false()">
				<error>
				  UserAgent '<xsl:value-of select="$ua"/>' not found
				</error>
      </xsl:when>
      <xsl:otherwise>

				<!--
				  get all capabilities
				-->
				<xsl:variable name="duid">
				  <xsl:copy-of select="device[@user_agent=$ua]/group/capability"/>
				  <xsl:call-template name="tid">
				    <xsl:with-param name="fall_back" select="device[@user_agent=$ua]/@fall_back"/>
				  </xsl:call-template>
				</xsl:variable>
	
				<xsl:variable name="duid_nodes" select="common:node-set($duid)"/>

				<device>
				  <xsl:copy-of select="device[@user_agent=$ua]/@*"/>

				  <xsl:for-each select="$duid_nodes/capability">
				    <xsl:sort select="@name"/>
				    <xsl:if test="not(@name = preceding-sibling::capability/@name)">
				      <xsl:copy-of select="."/>
				    </xsl:if>
				  </xsl:for-each>
				</device>
      </xsl:otherwise>
    </xsl:choose>
    
  </xsl:template>

  <xsl:template name="tid">
    <xsl:param name="fall_back"/>
    <xsl:if test="$fall_back != ''">
      <xsl:copy-of select="device[@id = $fall_back]/group/capability"/>
      <xsl:call-template name="tid">
				<xsl:with-param name="fall_back" select="device[@id=$fall_back]/@fall_back"/>
      </xsl:call-template>
    </xsl:if>
  </xsl:template>
  
  <xsl:template match="text()"/>
  
</xsl:stylesheet>