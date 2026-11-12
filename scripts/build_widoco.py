"""Build SHKG documentation with WIDOCO and the two rendering fixes."""

import argparse
import hashlib
from pathlib import Path
import shutil
import subprocess
from urllib.request import urlopen

from patch_widoco_property_entries import JAR_SHA256, patch_jar


ROOT = Path(__file__).resolve().parents[1]
JAR_URL = (
    "https://github.com/dgarijo/Widoco/releases/download/v1.4.25/"
    "widoco-1.4.25-jar-with-dependencies_JDK-17.jar"
)


# Website metadata for the current documentation release.
WIDOCO_PROPERTIES = """\
abstract=The soil health knowledge graph (SHKG) is designed to unify fragmented interpretations of soil health—a concept variably defined across research, policymaking, and agricultural practice—by structuring insights mainly from the European Environment Agency's report Soil Monitoring in Europe: Indicators and Thresholds for Soil Health Assessments. The KG leverages SKOS (Simple Knowledge Organization System) as its core framework to model soil health concepts, soil threat indicators and their critical thresholds, while Dublin Core standardizes metadata for references in the report. Relationships between entities are semantically defined using existing ontologies such as Agrontology and OBO Relation Ontology. The KG is linked to external vocabularies including AGROVOC, GloSIS, ISO 11074:2025, GEMET and INRAE Thesaurus.
authors=Beichen Wang;Luís Moreira de Sousa;Anna Fensel
authorsURI=https://orcid.org/0009-0008-5213-5114;https://orcid.org/0000-0002-5851-2071;https://orcid.org/0000-0002-1391-7104
codeRepository=https://github.com/soilwise-he/soil-health-knowledge-graph
contributors=Paul van Genuchten
dateCreated=12 November, 2026
dateIssued=12 November, 2026
dateModified=12 November, 2026
funder=European Commission
funding=SoilWise HE
introduction=This page documents the soil health knowledge graph. An alternative and searchable documentation of this graph is available [here](https://voc.soilwise-he.containers.wur.nl/).
licenseURI=http://creativecommons.org/licenses/by/4.0/
licenseName=CC-BY-4.0
ontologyName=SoilHealthKG
ontologyNamespaceURI=https://soilwise-he.github.io/soil-health
ontologyTitle=Soil Health Knowledge Graph
ontologyPrefix=she
ontologyRevisionNumber=0.2.7
publisher=Wageningen University & Research
publisherURI=https://www.wur.nl
status=Ontology Specification Beta
JSONLDSerialization=ontology.jsonld
NTSerialization=ontology.nt
RDFXMLSerialization=ontology.owl
TurtleSerialization=ontology.ttl
"""


def get_jar(path):
    """Download the pinned WIDOCO JAR if absent; reject an unexpected checksum."""
    path = path.resolve()
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        with urlopen(JAR_URL, timeout=120) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != JAR_SHA256:
            raise ValueError("Downloaded WIDOCO JAR has an unexpected SHA-256")
        path.write_bytes(data)
    # patch_jar also checks the checksum when reusing a cached JAR.
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--java", default="java", help="Java 17 executable")
    parser.add_argument(
        "--jar", type=Path, default=ROOT / ".cache/widoco/widoco-1.4.25.jar",
        help="Original WIDOCO 1.4.25 JDK 17 JAR; downloaded if absent",
    )
    args = parser.parse_args()
    jar = patch_jar(
        get_jar(args.jar),
        ROOT / ".cache/widoco/widoco-1.4.25-property-entries.jar",
    )
    output = ROOT / "build/site"
    output.mkdir(parents=True, exist_ok=True)
    properties_path = ROOT / "build/widoco.properties"
    properties_path.write_text(WIDOCO_PROPERTIES, encoding="utf-8", newline="\n")
    log_path = ROOT / "build/widoco.log"
    command = [
        args.java, "-Djava.awt.headless=true", "-Dfile.encoding=UTF-8",
        "-jar", str(jar), "-ontFile", str(ROOT / "soil_health_SKOS.ttl"),
        "-outFolder", str(output), "-confFile", str(properties_path),
        "-rewriteAll", "-uniteSections", "-excludeProvenance",
        "-includeAnnotationProperties", "-lang", "en",
    ]
    print(f"Building with WIDOCO 1.4.25; log: {log_path}", flush=True)
    with log_path.open("w", encoding="utf-8") as log:
        subprocess.run(
            command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT,
            check=True, timeout=600,
        )

    # Publish the complete source graph alongside WIDOCO's RDF exports.
    shutil.copyfile(ROOT / "soil_health_SKOS.ttl", output / "soil_health_SKOS.ttl")

    # Serve the English page at the site root without changing its contents.
    shutil.copyfile(output / "index-en.html", output / "index.html")
    (output / ".nojekyll").touch()
    print(f"Documentation generated in {output}")
    print("Preview: python -m http.server 8000 --directory build/site")


if __name__ == "__main__":
    main()
