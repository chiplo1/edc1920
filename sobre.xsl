<?xml version = "1.0" encoding = "UTF-8"?>
<xsl:stylesheet version = "1.0" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">
    <xsl:template match = "/sobre">
        <html>
            <body>
                <xsl:value-of select="description" />
                <xsl:for-each select="objectives/objective">
                    <xsl:value-of select="name"/>
                    <xsl:value-of select="done"/>
                </xsl:for-each>

            </body>
        </html>


    </xsl:template>
</xsl:stylesheet>