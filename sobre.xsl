<?xml version = "1.0" encoding = "UTF-8"?>
<xsl:stylesheet version = "1.0" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">
    <xsl:template match = "/about">
                <xsl:value-of select="description" />
                    <xsl:for-each select="objectives/objective">
                        <xsl:value-of select="name"/>
                    </xsl:for-each>
                    <xsl:for-each select="authors/author">
                        <xsl:value-of select="nome"/><br />
                    <xsl:value-of select="numero"/> <br />
                </xsl:for-each>
    </xsl:template>
</xsl:stylesheet>