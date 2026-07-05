import re


def generate_slug(name: str):
    slug = name.lower()

    slug = re.sub(r"[^a-z0-9]+", "-", slug)

    slug = slug.strip("-")

    return slug