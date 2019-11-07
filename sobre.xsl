<?xml version = "1.0" encoding = "UTF-8" ?>
<xsl:stylesheet version = "1.0" xmlns:xsl = "http://www.w3.org/1999/XSL/Transform">
    <xsl:template match = "/about">
                    <li style="font-size:20px;">
                        <xsl:value-of select="description" /><br />
                    </li>
                    <br />
                    <li style="font-size:19px;">
                        <xsl:value-of select="objetivo"/>
                    </li>
                    <xsl:for-each select="objectives/objective"><br />
                        <li style="font-size:15px;">
                            <xsl:value-of select="name"/><br />
                        </li>
                    </xsl:for-each>
                    <br />
                    <li style="font-size:19px;">
                        <xsl:value-of select="autores"/>
                    </li>
                    <xsl:for-each select="authors/author"><br />
                        <li style="font-size:15px;">
                            <xsl:value-of select="nome"/><br />
                        </li>
                        <li style="font-size:15px;">
                            <xsl:value-of select="numero"/><br />
                        </li>
                    </xsl:for-each>

        <br/>
    </xsl:template>
</xsl:stylesheet>