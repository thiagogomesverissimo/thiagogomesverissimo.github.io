import os
import shutil
import re
import json
import csv
from collections import defaultdict
from pathlib import Path
import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

OUTPUT_DIR = "docs"
CONTENT_DIR = "content"
ASSETS_DIR = "assets"
TEMPLATES_DIR = "templates"

CATEGORIES = [
    {"id": "posts", "titulo": "Posts", "folder": "posts"},
    {"id": "talks", "titulo": "Talks", "folder": "talks"},
    {"id": "publications", "titulo": "Publications", "folder": "publications"},
    {"id": "courses-taken", "titulo": "Courses Taken", "folder": "courses-taken"},
    {"id": "documents", "titulo": "Documents", "folder": "documents"}
]

def load_profile():
    profile_file = os.path.join(CONTENT_DIR, "profile.json")
    if os.path.exists(profile_file):
        with open(profile_file, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"nome": "Seu Nome", "bio": "", "links": []}

def parse_markdown_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    meta = {}
    body = content
    content_normalized = content.replace("\r\n", "\n")

    if content_normalized.startswith("---"):
        parts = content_normalized.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1]) or {}
            except Exception as e:
                print(f"⚠️ Erro ao ler YAML de {filepath}: {e}")
                meta = {}
            body = parts[2].strip()

    title = meta.get("title")
    if not title:
        h1_match = re.search(r"^#\s+(.*)", body, re.MULTILINE)
        if h1_match:
            title = h1_match.group(1).strip()
        else:
            title = Path(filepath).stem.replace("-", " ").replace("_", " ").title()

    body_clean = re.sub(r"^#\s+.*\n?", "", body, count=1).strip()

    html_content = markdown.markdown(
        body_clean,
        extensions=['extra', 'codehilite', 'fenced_code', 'nl2br', 'tables', 'toc']
    )

    date_str = str(meta.get("date", "")) if meta.get("date") is not None else ""
    slug = Path(filepath).stem

    return {
        "title": title,
        "date": date_str,
        "content": html_content,
        "filename": Path(filepath).name,
        "slug": slug
    }

def load_courses():
    """Lê content/courses.csv, agrupa por ano e verifica certificados em assets/courses/{id}.pdf."""
    # Detecta a raiz do projeto (mesmo se o script for chamado de dentro de scripts/)
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent if script_dir.name == "scripts" else script_dir

    csv_file = project_root / "content" / "courses.csv"
    assets_courses_dir = project_root / "assets" / "courses"

    if not csv_file.exists():
        print("⚠️ Ficheiro content/courses.csv não encontrado.")
        return []

    courses_by_year = defaultdict(list)
    found_pdfs = 0

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            course_id = row.get("id", "").strip()
            year = row.get("year", "").strip()
            title_text = row.get("title", "").strip()
            url = (row.get("url") or "").strip()

            # Checa se existe o PDF (testa .pdf e .PDF)
            pdf_file = assets_courses_dir / f"{course_id}.pdf"
            if not pdf_file.exists():
                pdf_file = assets_courses_dir / f"{course_id}.PDF"

            has_pdf = pdf_file.exists()
            if has_pdf:
                found_pdfs += 1

            # Caminho relativo para o HTML em docs/
            pdf_url = f"assets/courses/{pdf_file.name}" if has_pdf else ""

            title_html = markdown.markdown(title_text, extensions=['extra', 'nl2br'])

            courses_by_year[year].append({
                "id": course_id,
                "title": title_text,
                "url": url,
                "title_html": title_html,
                "has_pdf": has_pdf,
                "pdf_url": pdf_url
            })

    sorted_years = sorted(courses_by_year.keys(), reverse=True)

    result = []
    for year in sorted_years:
        result.append({
            "year": year,
            "courses": courses_by_year[year]
        })

    print(f"🎓 Processados cursos de {len(sorted_years)} anos ({found_pdfs} PDF(s) de certificados encontrados).")
    return result

def load_documents():
    """Lê content/documents.csv, agrupa por ano e monta links para PDF/URL dos documentos."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent if script_dir.name == "scripts" else script_dir

    csv_file = project_root / "content" / "documents.csv"
    assets_documents_dir = project_root / "assets" / "documents"

    if not csv_file.exists():
        print("⚠️ Ficheiro content/documents.csv não encontrado.")
        return []

    documents_by_year = defaultdict(list)

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            document_id = row.get("id", "").strip()
            year = row.get("year", "").strip()
            title_text = row.get("title", "").strip()
            url = (row.get("url") or "").strip()

            pdf_file = assets_documents_dir / f"{document_id}.pdf"
            if not pdf_file.exists():
                pdf_file = assets_documents_dir / f"{document_id}.PDF"

            has_pdf = pdf_file.exists()
            pdf_url = f"assets/documents/{pdf_file.name}" if has_pdf else ""

            documents_by_year[year].append({
                "id": document_id,
                "title": title_text,
                "url": url,
                "has_pdf": has_pdf,
                "pdf_url": pdf_url,
                "title_html": markdown.markdown(title_text, extensions=['extra', 'nl2br'])
            })

    result = []
    for year in sorted(documents_by_year.keys(), reverse=True):
        result.append({
            "year": year,
            "documents": documents_by_year[year]
        })

    return result

def load_publications():
    """Lê content/publications.csv, agrupa por ano e monta links para PDF/URL."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent if script_dir.name == "scripts" else script_dir

    csv_file = project_root / "content" / "publications.csv"
    assets_publications_dir = project_root / "assets" / "publications"

    if not csv_file.exists():
        print("⚠️ Ficheiro content/publications.csv não encontrado.")
        return []

    publications_by_year = defaultdict(list)

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            publication_id = row.get("id", "").strip()
            year = row.get("year", "").strip()
            title_text = row.get("title", "").strip()
            url = (row.get("url") or "").strip()

            pdf_file = assets_publications_dir / f"{publication_id}.pdf"
            if not pdf_file.exists():
                pdf_file = assets_publications_dir / f"{publication_id}.PDF"

            has_pdf = pdf_file.exists()
            pdf_url = f"assets/publications/{pdf_file.name}" if has_pdf else ""

            publications_by_year[year].append({
                "id": publication_id,
                "title": title_text,
                "url": url,
                "has_pdf": has_pdf,
                "pdf_url": pdf_url,
                "title_html": markdown.markdown(title_text, extensions=['extra', 'nl2br'])
            })

    result = []
    for year in sorted(publications_by_year.keys(), reverse=True):
        result.append({
            "year": year,
            "publications": publications_by_year[year]
        })

    return result


def load_talks():
    """Lê content/talks.csv, agrupa por ano e monta links para PDF/URL."""
    script_dir = Path(__file__).resolve().parent
    project_root = script_dir.parent if script_dir.name == "scripts" else script_dir

    csv_file = project_root / "content" / "talks.csv"
    assets_talks_dir = project_root / "assets" / "talks"

    if not csv_file.exists():
        print("⚠️ Ficheiro content/talks.csv não encontrado.")
        return []

    talks_by_year = defaultdict(list)

    with open(csv_file, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            talk_id = row.get("id", "").strip()
            year = row.get("year", "").strip()
            title_text = row.get("title", "").strip()
            url = (row.get("url") or "").strip()

            pdf_file = assets_talks_dir / f"{talk_id}.pdf"
            if not pdf_file.exists():
                pdf_file = assets_talks_dir / f"{talk_id}.PDF"

            has_pdf = pdf_file.exists()
            pdf_url = f"assets/talks/{pdf_file.name}" if has_pdf else ""

            talks_by_year[year].append({
                "id": talk_id,
                "title": title_text,
                "url": url,
                "has_pdf": has_pdf,
                "pdf_url": pdf_url,
                "title_html": markdown.markdown(title_text, extensions=['extra', 'nl2br'])
            })

    result = []
    for year in sorted(talks_by_year.keys(), reverse=True):
        result.append({
            "year": year,
            "talks": talks_by_year[year]
        })

    return result


def copy_static_assets():
    destino = os.path.join(OUTPUT_DIR, "assets")
    if os.path.exists(destino):
        shutil.rmtree(destino)
    if os.path.exists(ASSETS_DIR):
        shutil.copytree(ASSETS_DIR, destino)

def process_standalone_pages(env, profile):
    pages_dir = os.path.join(CONTENT_DIR, "pages")
    output_pages_dir = os.path.join(OUTPUT_DIR, "pages")

    if not os.path.exists(pages_dir):
        return

    os.makedirs(output_pages_dir, exist_ok=True)
    template = env.get_template("page.html")

    files = [f for f in os.listdir(pages_dir) if f.endswith(".md")]
    for file in files:
        full_path = os.path.join(pages_dir, file)
        item_data = parse_markdown_file(full_path)
        output_file = os.path.join(output_pages_dir, f"{item_data['slug']}.html")

        html_out = template.render(
            profile=profile,
            page=item_data,
            relative_root="../"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_out)

def process_individual_posts(env, profile, posts):
    output_posts_dir = os.path.join(OUTPUT_DIR, "posts")
    os.makedirs(output_posts_dir, exist_ok=True)
    template = env.get_template("page.html")

    for item_data in posts:
        output_file = os.path.join(output_posts_dir, f"{item_data['slug']}.html")

        html_out = template.render(
            profile=profile,
            page=item_data,
            relative_root="../"
        )

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html_out)

def build_site():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    copy_static_assets()
    profile = load_profile()

    env = Environment(loader=FileSystemLoader(TEMPLATES_DIR))

    process_standalone_pages(env, profile)

    processed_categories = []

    for cat in CATEGORIES:
        if cat["id"] == "courses-taken":
            courses_grouped = load_courses()
            processed_categories.append({
                "id": cat["id"],
                "titulo": cat["titulo"],
                "courses_grouped": courses_grouped
            })
            continue

        if cat["id"] == "documents":
            documents_grouped = load_documents()
            processed_categories.append({
                "id": cat["id"],
                "titulo": cat["titulo"],
                "documents_grouped": documents_grouped
            })
            continue

        if cat["id"] == "publications":
            publications_grouped = load_publications()
            processed_categories.append({
                "id": cat["id"],
                "titulo": cat["titulo"],
                "publications_grouped": publications_grouped
            })
            continue

        if cat["id"] == "talks":
            talks_grouped = load_talks()
            processed_categories.append({
                "id": cat["id"],
                "titulo": cat["titulo"],
                "talks_grouped": talks_grouped
            })
            continue

        folder_path = os.path.join(CONTENT_DIR, cat["folder"]) 
        items = []

        if os.path.exists(folder_path):
            files = [f for f in os.listdir(folder_path) if f.endswith(".md")]
            for file in sorted(files, reverse=True):
                full_path = os.path.join(folder_path, file)
                item_data = parse_markdown_file(full_path)
                item_data["url"] = f"{cat['folder']}/{item_data['slug']}.html"
                items.append(item_data)

        if cat["id"] == "posts":
            process_individual_posts(env, profile, items)

        processed_categories.append({
            "id": cat["id"],
            "titulo": cat["titulo"],
            "entries": items
        })

    template = env.get_template("index.html")

    html_final = template.render(
        profile=profile,
        categories=processed_categories
    )

    output_path = os.path.join(OUTPUT_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_final)

    print(f"\n✅ Site gerado com sucesso em: {output_path}")

if __name__ == "__main__":
    build_site()