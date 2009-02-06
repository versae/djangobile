<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
		xmlns:func="http://exslt.org/functions"
		xmlns:my="my://own.uri"
		extension-element-prefixes="func">
  
  <xsl:output method="text"
	      encoding="ISO-8859-1"
	      indent="yes"/>

  <!--
    roland: count devices stored in WURFL
    send comments, questions to roland guelle <roldriguez@users.sourceforge.net>
  -->

  <xsl:template match="/">
*****************************************************************************
Useragents: <xsl:value-of select="count(//device)"/>
Devices: <xsl:value-of select="count(//device[@actual_device_root='true'])"/>
Capabilities: <xsl:value-of select="count(//devices[1]/device[1]/group/capability)"/>
*****************************************************************************
<xsl:text>
</xsl:text>
  </xsl:template>
</xsl:stylesheet>
