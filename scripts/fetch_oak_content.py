#!/usr/bin/env python3
"""
Oak National Academy Content Fetcher
Fetches curriculum content from the Oak Open API (Open Government License)
"""

import requests
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


# Oak API Base URL
OAK_API_BASE = "https://open-api.thenational.academy"


@dataclass
class OakLesson:
    """Represents a lesson from Oak Academy"""
    slug: str
    title: str
    subject: str
    key_stage: str
    year: Optional[str]
    unit_title: Optional[str]
    lesson_description: Optional[str]
    video_url: Optional[str]
    transcript: Optional[str]
    quiz_questions: List[Dict[str, Any]]


class OakAPIClient:
    """Client for Oak National Academy Open API"""

    def __init__(self, base_url: str = OAK_API_BASE):
        self.base_url = base_url
        self.session = requests.Session()

    def get_subjects(self, key_stage: str) -> List[Dict[str, Any]]:
        """Get available subjects for a key stage"""
        # Note: Actual API endpoints may differ - check documentation
        url = f"{self.base_url}/api/v1/key-stages/{key_stage}/subjects"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching subjects: {e}")
            return []

    def get_units(self, key_stage: str, subject: str) -> List[Dict[str, Any]]:
        """Get units for a subject"""
        url = f"{self.base_url}/api/v1/key-stages/{key_stage}/subjects/{subject}/units"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching units: {e}")
            return []

    def get_lessons(self, unit_slug: str) -> List[Dict[str, Any]]:
        """Get lessons in a unit"""
        url = f"{self.base_url}/api/v1/units/{unit_slug}/lessons"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching lessons: {e}")
            return []

    def get_lesson_content(self, lesson_slug: str) -> Optional[Dict[str, Any]]:
        """Get full lesson content including video, transcript, and quiz"""
        url = f"{self.base_url}/api/v1/lessons/{lesson_slug}"
        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error fetching lesson content: {e}")
            return None


def save_content(content: Dict[str, Any], filepath: Path):
    """Save content to JSON file"""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    print(f"Saved: {filepath}")


def fetch_key_stage_content(
    client: OakAPIClient,
    key_stage: str,
    output_dir: Path,
    subjects: Optional[List[str]] = None
):
    """Fetch all content for a key stage"""
    print(f"\n=== Fetching {key_stage} content ===")

    # Get subjects
    all_subjects = client.get_subjects(key_stage)
    if subjects:
        all_subjects = [s for s in all_subjects if s.get('slug') in subjects]

    for subject in all_subjects:
        subject_slug = subject.get('slug', 'unknown')
        print(f"\nSubject: {subject_slug}")

        # Get units
        units = client.get_units(key_stage, subject_slug)

        for unit in units:
            unit_slug = unit.get('slug', 'unknown')
            print(f"  Unit: {unit_slug}")

            # Get lessons
            lessons = client.get_lessons(unit_slug)

            for lesson in lessons:
                lesson_slug = lesson.get('slug', 'unknown')

                # Get full lesson content
                content = client.get_lesson_content(lesson_slug)

                if content:
                    filepath = output_dir / key_stage / subject_slug / unit_slug / f"{lesson_slug}.json"
                    save_content(content, filepath)


def main():
    """Main entry point"""
    # Output directory
    output_dir = Path(__file__).parent.parent / "data" / "oak_content"

    # Initialize client
    client = OakAPIClient()

    # Key stages relevant to our exams
    # KS2 (ages 7-11) - for 11+ prep
    # KS3 (ages 11-14) - foundational for GCSE
    # KS4 (ages 14-16) - GCSE content

    print("Oak National Academy Content Fetcher")
    print("====================================")
    print(f"API Base: {OAK_API_BASE}")
    print(f"Output: {output_dir}")
    print("\nNote: Check Oak API documentation for exact endpoints")
    print("URL: https://open-api.thenational.academy/")

    # Example: Fetch KS2 Maths for 11+ prep
    # Uncomment when ready to fetch
    # fetch_key_stage_content(
    #     client,
    #     key_stage="ks2",
    #     output_dir=output_dir,
    #     subjects=["maths", "english"]
    # )

    # Example: Fetch KS4 for GCSE
    # fetch_key_stage_content(
    #     client,
    #     key_stage="ks4",
    #     output_dir=output_dir,
    #     subjects=["maths", "english", "combined-science"]
    # )

    print("\n[Demo mode - uncomment fetch calls to download content]")
    print("\nAPI Documentation: https://open-api.thenational.academy/")


if __name__ == "__main__":
    main()
