#!/usr/bin/env python3
"""
Download Free 11+ Papers and Resources
Downloads legally available free practice papers from official sources
"""

import os
import requests
from pathlib import Path
from urllib.parse import urlparse
import time

# Output directory
DATA_DIR = Path(__file__).parent.parent / "data"
PAPERS_DIR = DATA_DIR / "past_papers"
CURRICULUM_DIR = DATA_DIR / "curriculum"


# Free official resources
RESOURCES = {
    "curriculum": [
        {
            "name": "KS2 National Curriculum",
            "url": "https://assets.publishing.service.gov.uk/media/5a81a9abe5274a2e8ab55319/PRIMARY_national_curriculum.pdf",
            "filename": "ks2_national_curriculum.pdf"
        },
        {
            "name": "KS3/4 National Curriculum",
            "url": "https://assets.publishing.service.gov.uk/media/5da7291840f0b6598f806433/Secondary_national_curriculum_corrected_PDF.pdf",
            "filename": "ks3_ks4_national_curriculum.pdf"
        },
    ],
    "gl_familiarisation": [
        # GL Assessment provides free familiarisation materials
        # These would be downloaded from their official site after registration
        # Placeholder - actual URLs require login
    ],
    "exam_board_specs": [
        {
            "name": "AQA GCSE Maths Specification",
            "url": "https://filestore.aqa.org.uk/resources/mathematics/specifications/AQA-8300-SP-2015.PDF",
            "filename": "aqa_gcse_maths_spec.pdf"
        },
    ]
}

# Links to free paper collections (for user reference, not automated download)
FREE_PAPER_SOURCES = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    FREE 11+ PRACTICE PAPER SOURCES                           ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  OFFICIAL EXAM BOARD RESOURCES:                                              ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║  • GL Assessment: https://11plus.gl-assessment.co.uk/                        ║
║    → Free familiarisation papers (requires registration)                     ║
║                                                                              ║
║  • CGP Books: https://www.cgpbooks.co.uk/info/preparing-for-the-11-plus     ║
║    → Free practice tests                                                     ║
║                                                                              ║
║  • Collins: https://collins.co.uk/pages/revision-collins-11-free-resources  ║
║    → Free 11+ resources                                                      ║
║                                                                              ║
║  COMMUNITY COLLECTIONS:                                                      ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║  • SATs Papers: https://www.sats-papers.co.uk/11-plus-papers/               ║
║    → 450+ free papers with answers                                           ║
║                                                                              ║
║  • Maths Genie: https://www.mathsgenie.co.uk/                               ║
║    → Free GCSE maths papers                                                  ║
║                                                                              ║
║  GCSE PAST PAPERS (OFFICIAL):                                               ║
║  ─────────────────────────────────────────────────────────────────────────── ║
║  • AQA: https://www.aqa.org.uk/find-past-papers-and-mark-schemes            ║
║  • Edexcel: https://qualifications.pearson.com/.../past-papers.html         ║
║  • OCR: https://www.ocr.org.uk/qualifications/past-paper-finder/            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""


def download_file(url: str, dest: Path, name: str) -> bool:
    """Download a file with progress indication"""
    try:
        print(f"  Downloading: {name}")
        print(f"    URL: {url}")

        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        total_size = int(response.headers.get('content-length', 0))

        dest.parent.mkdir(parents=True, exist_ok=True)

        with open(dest, 'wb') as f:
            if total_size == 0:
                f.write(response.content)
            else:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    pct = (downloaded / total_size) * 100
                    print(f"    Progress: {pct:.1f}%", end='\r')

        size_mb = dest.stat().st_size / (1024 * 1024)
        print(f"    ✓ Saved: {dest.name} ({size_mb:.1f} MB)")
        return True

    except Exception as e:
        print(f"    ✗ Failed: {e}")
        return False


def main():
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║              ExamTutor - Free Resource Downloader                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Download curriculum documents
    print("\n📚 Downloading National Curriculum Documents...")
    print("=" * 60)

    for resource in RESOURCES["curriculum"]:
        dest = CURRICULUM_DIR / resource["filename"]
        if dest.exists():
            print(f"  ✓ Already exists: {resource['name']}")
        else:
            download_file(resource["url"], dest, resource["name"])
        time.sleep(0.5)

    # Download exam board specs
    print("\n📋 Downloading Exam Board Specifications...")
    print("=" * 60)

    for resource in RESOURCES.get("exam_board_specs", []):
        dest = CURRICULUM_DIR / "specifications" / resource["filename"]
        if dest.exists():
            print(f"  ✓ Already exists: {resource['name']}")
        else:
            download_file(resource["url"], dest, resource["name"])
        time.sleep(0.5)

    # Show free paper sources
    print(FREE_PAPER_SOURCES)

    # Create a reference file
    ref_file = PAPERS_DIR / "FREE_PAPER_SOURCES.txt"
    ref_file.parent.mkdir(parents=True, exist_ok=True)
    with open(ref_file, 'w') as f:
        f.write(FREE_PAPER_SOURCES)

    print(f"\n✓ Reference saved to: {ref_file}")

    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    curriculum_files = list(CURRICULUM_DIR.glob("*.pdf"))
    print(f"  Curriculum PDFs: {len(curriculum_files)}")
    for f in curriculum_files:
        size_mb = f.stat().st_size / (1024 * 1024)
        print(f"    • {f.name} ({size_mb:.1f} MB)")

    print("\n📌 Next steps:")
    print("   1. Visit the links above to download practice papers manually")
    print("   2. Register at GL Assessment for official familiarisation papers")
    print("   3. Run generate_questions.py to create AI-generated practice")


if __name__ == "__main__":
    main()
