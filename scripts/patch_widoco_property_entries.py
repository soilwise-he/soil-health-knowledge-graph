"""Prepare a WIDOCO 1.4.25 JAR with property-entry and datatype-link fixes.

LODE's Object/Datatype Property templates require child XML elements, so they
omit declarations whose labels are serialized in separate rdf:Description
elements. Remove that presentation filter from the entries and their tables of
contents. Link five external datatypes to their official documentation instead
of nonexistent local entries. OWLAPI and RDF serialization remain unchanged.

build_widoco.py applies these fixes automatically. To prepare the JAR separately:
    python scripts/patch_widoco_property_entries.py
    java -jar .cache/widoco/widoco-1.4.25-property-entries.jar ...

The original checksum-verified JAR is preserved. RDF input and generated HTML
are not rewritten by this helper.
"""

import argparse
import hashlib
from pathlib import Path
import tempfile
from zipfile import ZipFile


ROOT = Path(__file__).resolve().parents[1]
JAR_SHA256 = "be57a270fffb91e55810fa308717e704a44e2e7c027a3d68125a49da6c8b4e2b"
STYLESHEET = "lode/extraction.xsl"
REPLACEMENTS = {
    "exists(//owl:ObjectProperty/element())": "exists(//owl:ObjectProperty)",
    "exists(//owl:DatatypeProperty/element())": "exists(//owl:DatatypeProperty)",
    "/rdf:RDF/(owl:ObjectProperty)[exists(element())]": "/rdf:RDF/(owl:ObjectProperty)",
    "/rdf:RDF/owl:DatatypeProperty[exists(element())]": "/rdf:RDF/owl:DatatypeProperty",
}
DATATYPE_DOCUMENTATION = {
    "http://www.w3.org/2001/XMLSchema#gYearMonth": "https://www.w3.org/TR/xmlschema11-2/#gYearMonth",
    "http://www.w3.org/2001/XMLSchema#date": "https://www.w3.org/TR/xmlschema11-2/#date",
    "http://www.w3.org/2001/XMLSchema#gYear": "https://www.w3.org/TR/xmlschema11-2/#gYear",
    "http://www.w3.org/2001/XMLSchema#int": "https://www.w3.org/TR/xmlschema11-2/#int",
    "http://qudt.org/schema/qudt/LatexString": "https://qudt.org/schema/qudt/LatexString",
}


def patch_stylesheet(data):
    """Fix property selection and five datatype links in the pinned XSLT."""
    text = data.decode("utf-8")
    for original, replacement in REPLACEMENTS.items():
        if text.count(original) != 2:
            raise ValueError(f"Unexpected WIDOCO stylesheet: {original!r}")
        text = text.replace(original, replacement)

    # f:findEntityId returns IDs for rdfs:Datatype declarations, although LODE
    # never renders those entries. Override only these five known link targets;
    # retain the displayed label and original datatype IRI in the title.
    link_branch = '        <xsl:choose>\n            <xsl:when test="$anchor = \'\'">'
    if text.count(link_branch) != 1:
        raise ValueError("Unexpected WIDOCO datatype-link template")
    datatype_branches = "".join(
        f'            <xsl:when test=". = \'{iri}\'">\n'
        f'                <a href="{url}" title="{{.}}" target="_blank" rel="noopener noreferrer">\n'
        '                    <xsl:value-of select="$label"/>\n'
        '                </a>\n'
        '            </xsl:when>\n'
        for iri, url in DATATYPE_DOCUMENTATION.items()
    )
    text = text.replace(
        link_branch,
        '        <xsl:choose>\n' + datatype_branches + '            <xsl:when test="$anchor = \'\'">',
    )
    return text.encode("utf-8")


def patch_jar(source, output):
    """Write a separate JAR, preserving every entry except the LODE stylesheet."""
    source, output = source.resolve(), output.resolve()
    if source == output:
        raise ValueError("The patched JAR must not overwrite the original JAR")
    if hashlib.sha256(source.read_bytes()).hexdigest() != JAR_SHA256:
        raise ValueError("Expected the pinned WIDOCO 1.4.25 JDK 17 JAR")
    with ZipFile(source) as archive:
        patched = patch_stylesheet(archive.read(STYLESHEET))
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(dir=output.parent, suffix=".jar.tmp", delete=False) as handle:
            temporary = Path(handle.name)
        try:
            with ZipFile(temporary, "w") as result:
                result.comment = archive.comment
                for entry in archive.infolist():
                    data = patched if entry.filename == STYLESHEET else archive.read(entry)
                    result.writestr(entry, data)
            temporary.replace(output)
        finally:
            temporary.unlink(missing_ok=True)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--jar", type=Path, default=ROOT / ".cache/widoco/widoco-1.4.25.jar",
        help="Existing original WIDOCO 1.4.25 JDK 17 JAR",
    )
    parser.add_argument(
        "--output", type=Path,
        default=ROOT / ".cache/widoco/widoco-1.4.25-property-entries.jar",
        help="Separate JAR containing the rendering fix",
    )
    args = parser.parse_args()
    output = patch_jar(args.jar, args.output)
    print(f"Patched only {STYLESHEET}: {output}")


if __name__ == "__main__":
    main()
