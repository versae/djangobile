<?xml version="1.0" encoding="ISO-8859-1"?>
<xsl:stylesheet version="1.0"
		xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
  
  <xsl:output method="html"
	      encoding="ISO-8859-1"
	      indent="yes"/>

  <!--
    roland: xslt for transform into a html page.
    useful if your friends are asking if their brand new device is supported by WURFL
    send comments, questions to roland guelle <roldriguez@users.sourceforge.net>
  -->
  
  <xsl:template match="/">
    <html>
      <head>
	<title><xsl:value-of select="/wurfl/version/ver"/></title>
      </head>
      <body>

	<!--
	  device informations
	-->
	<div>
	  <h1><xsl:value-of select="/wurfl/version/ver"/></h1>
	  <xsl:apply-templates select="/wurfl/devices/device"/>
	</div>
	
	<!--
	  version informations
	-->
	<div>
	  <xsl:apply-templates select="/wurfl/version"/>
	</div>

      </body>
    </html>
  </xsl:template>

  <xsl:template match="device">
    <div>
      <h5><xsl:value-of select="@id"/></h5>
      <ul>
	<li>
	  <xsl:for-each select="@*">
	    <u><xsl:value-of select="name()"/></u><xsl:text> </xsl:text><i><xsl:value-of select="."/></i><br/>
	  </xsl:for-each>
	  <xsl:for-each select="*">
	    <ul>
	      <li>
		<xsl:for-each select="@*">
		  <u><xsl:value-of select="name()"/></u><xsl:text> </xsl:text><i><xsl:value-of select="."/></i><br/>
		</xsl:for-each>
		<xsl:for-each select="*">
		  <ul>
		    <li>
		      <xsl:for-each select="@*">
			<u><xsl:value-of select="name()"/></u><xsl:text> </xsl:text><i><xsl:value-of select="."/></i><br/>
		      </xsl:for-each>
		    </li>
		  </ul>
		</xsl:for-each>
	      </li>
	    </ul>
	  </xsl:for-each>
	</li>
      </ul>
    </div>
  </xsl:template>

  <xsl:template match="version">
    <hr/>
    <h4><a href="{official_url}"><xsl:value-of select="ver"/></a></h4>
    <h4><xsl:value-of select="last_updated"/></h4>
    
    <p>
      <xsl:value-of select="statement"/>
    </p>

    <h4>Thanks to:</h4>
    
    <p>
      <h5>Maintainer</h5>
      <ul>
	<xsl:for-each select="maintainers/maintainer">
	  <li>
	    <a href="mailto:{@email}"><xsl:value-of select="@name"/></a> / <a href="mailto:{@home_page}">www</a>
	  </li>
	</xsl:for-each>
      </ul>
    </p>

    <p>
      <h5>Authors</h5>
      <ul>
	<xsl:for-each select="authors/author">
	  <li>
	    <a href="mailto:{@email}"><xsl:value-of select="@name"/></a> / <a href="mailto:{@home_page}">www</a>
	  </li>
	</xsl:for-each>
      </ul>
    </p>

    <p>
      <h5>Contributors</h5>
      <ul>
	<xsl:for-each select="contributors/contributor">
	  <li>
	    <a href="mailto:{@email}"><xsl:value-of select="@name"/></a>
	  </li>
	</xsl:for-each>
      </ul>
    </p>
  </xsl:template>
</xsl:stylesheet>