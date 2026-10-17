#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gerenciador Interativo de Conteúdo CSV para thiagogomesverissimo.github.io
Permite adicionar, editar e listar:
- Publicações (content/publications.csv)
- Documentos (content/documents.csv)
- Cursos (content/courses.csv)
- Palestras (content/talks.csv)

Regras:
- O ID é sempre gerado automaticamente (próximo número inteiro).
- Na edição, o usuário informa o ID após ver a lista de itens existentes.
- O ID NUNCA pode ser alterado na edição (preserva integridade de assets/*.pdf).
"""

import csv
import os
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

# Caminhos base resolvidos a partir da localização do script
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent if SCRIPT_DIR.name == "scripts" else SCRIPT_DIR
CONTENT_DIR = PROJECT_ROOT / "content"
ASSETS_DIR = PROJECT_ROOT / "assets"

# Configuração de cores ANSI para o terminal (desativadas se não for TTY)
USE_COLOR = sys.stdout.isatty()


def color(text, code):
    return f"\033[{code}m{text}\033[0m" if USE_COLOR else text


def green(text):
    return color(text, "32")


def yellow(text):
    return color(text, "33")


def cyan(text):
    return color(text, "36")


def bold(text):
    return color(text, "1")


def red(text):
    return color(text, "31")


def dim(text):
    return color(text, "2")


def get_display_path(filepath):
    """Retorna caminho relativo ao projeto se possível, ou o nome do arquivo."""
    try:
        return str(filepath.relative_to(PROJECT_ROOT))
    except (ValueError, AttributeError):
        return f"content/{filepath.name}" if hasattr(filepath, "name") else str(filepath)


FIELDNAMES = ["id", "year", "title", "url"]

CATEGORIES = {
    "1": {
        "key": "publications",
        "name": "Publicações (publications.csv)",
        "singular": "Publicação",
        "file": CONTENT_DIR / "publications.csv",
        "assets_folder": "publications",
    },
    "2": {
        "key": "documents",
        "name": "Documentos (documents.csv)",
        "singular": "Documento",
        "file": CONTENT_DIR / "documents.csv",
        "assets_folder": "documents",
    },
    "3": {
        "key": "courses",
        "name": "Cursos (courses.csv)",
        "singular": "Curso",
        "file": CONTENT_DIR / "courses.csv",
        "assets_folder": "courses",
    },
    "4": {
        "key": "talks",
        "name": "Palestras / Talks (talks.csv)",
        "singular": "Palestra",
        "file": CONTENT_DIR / "talks.csv",
        "assets_folder": "talks",
    },
}


def load_items(filepath):
    """Carrega os itens do arquivo CSV mantendo a ordem original."""
    if not filepath.exists():
        return []
    with open(filepath, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def save_items(filepath, items):
    """Grava os itens no arquivo CSV formatado em UTF-8 com quebras padrão."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, mode="w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        for item in items:
            writer.writerow({
                "id": str(item.get("id", "")).strip(),
                "year": str(item.get("year", "")).strip(),
                "title": str(item.get("title", "")).strip(),
                "url": str(item.get("url", "")).strip(),
            })


def get_next_id(items):
    """
    Calcula o próximo ID automaticamente.
    Encontra o maior ID numérico existente e soma 1.
    Se a lista estiver vazia, retorna 1.
    """
    ids = []
    for it in items:
        raw_id = str(it.get("id", "")).strip()
        if raw_id.isdigit():
            ids.append(int(raw_id))
    return max(ids, default=0) + 1


def check_pdf(assets_folder, item_id):
    """Verifica se existe arquivo PDF vinculado em assets/{folder}/{id}.pdf."""
    target_dir = ASSETS_DIR / assets_folder
    if not target_dir.exists():
        return False
    for ext in [".pdf", ".PDF"]:
        if (target_dir / f"{item_id}{ext}").exists():
            return True
    return False


def display_items(items, assets_folder, filter_text="", show_full=False):
    """Exibe tabela formatada com os itens cadastrados."""
    filtered = items
    if filter_text:
        ft = filter_text.lower()
        filtered = [
            it for it in items
            if ft in it.get("title", "").lower()
            or ft in it.get("year", "").lower()
            or ft == str(it.get("id", "")).strip()
        ]

    if not filtered:
        print(yellow("  Nenhum item encontrado correspondente ao filtro."))
        return []

    term_width = shutil.get_terminal_size((100, 24)).columns
    title_width = max(35, min(80, term_width - 32))

    header = f"{'ID':>4} | {'Ano':^4} | {'PDF':^5} | {'Título':<{title_width}}"
    sep = "-" * len(header)
    print(sep)
    print(bold(header))
    print(sep)

    for it in filtered:
        raw_id = str(it.get("id", "")).strip()
        year = str(it.get("year", "")).strip()
        title = str(it.get("title", "")).strip()
        has_pdf = check_pdf(assets_folder, raw_id)

        pdf_label = "Sim" if has_pdf else "Não"
        pdf_fmt = green(f"{pdf_label:^5}") if has_pdf else dim(f"{pdf_label:^5}")
        id_fmt = cyan(f"{raw_id:>4}")

        if not show_full and len(title) > title_width:
            display_title = title[:title_width - 3] + "..."
        else:
            display_title = title.ljust(title_width)

        url = str(it.get("url", "")).strip()
        url_mark = f" {cyan('🔗')}" if url else ""

        print(f"{id_fmt} | {year:^4} | {pdf_fmt} | {display_title}{url_mark}")

    print(sep)
    count_info = f"Exibindo {len(filtered)} de {len(items)} item(ns)"
    if filter_text:
        count_info += f" (filtro: '{filter_text}')"
    print(dim(f"{count_info} | 🔗 = link cadastrado | PDF = assets/{assets_folder}/<id>.pdf"))
    return filtered


def run_generate_site():
    """Executa o gerador de site generate_site.py."""
    gen_script = PROJECT_ROOT / "scripts" / "generate_site.py"
    if not gen_script.exists():
        print(red(f"Arquivo não encontrado: {gen_script}"))
        return
    print(bold("\nExecutando scripts/generate_site.py..."))
    try:
        subprocess.run([sys.executable, str(gen_script)], cwd=str(PROJECT_ROOT), check=True)
        print(green("✔ Site regerado com sucesso em docs/!"))
    except Exception as e:
        print(red(f"Erro ao executar scripts/generate_site.py: {e}"))


def prompt_generate_site():
    """Pergunta se o usuário deseja regerar o site após uma alteração."""
    ans = input(f"\nDeseja regerar o site agora executando generate_site.py? (s/{bold('N')}): ").strip().lower()
    if ans in ["s", "sim", "y", "yes"]:
        run_generate_site()


def add_item_flow(cat_info):
    """Fluxo interativo para inclusão de novo item com ID automático."""
    items = load_items(cat_info["file"])
    next_id = get_next_id(items)

    print("\n" + "=" * 60)
    print(bold(f" ADICIONAR NOVO ITEM: {cat_info['singular'].upper()}"))
    print("=" * 60)
    print(f"ID gerado automaticamente: {bold(cyan(str(next_id)))} {dim('(imutável, nunca poderá ser alterado)')}")
    print("-" * 60)

    # Ano
    current_year = str(datetime.now().year)
    while True:
        year_input = input(f"Ano [{current_year}]: ").strip()
        if not year_input:
            year = current_year
            break
        if year_input.isdigit() and len(year_input) == 4:
            year = year_input
            break
        print(yellow("⚠️ Por favor, informe um ano válido de 4 dígitos (ex: 2026)."))

    # Título
    while True:
        title = input("Título: ").strip()
        if title:
            break
        print(red("⚠️ O título é obrigatório. Por favor, digite o título."))

    # URL
    url = input("URL ou DOI (opcional, pressione Enter para vazio): ").strip()

    # Confirmação
    print("\n" + bold("Resumo do novo item a ser inserido:"))
    print(f"  ID:     {bold(cyan(str(next_id)))}")
    print(f"  Ano:    {year}")
    print(f"  Título: {title}")
    print(f"  URL:    {url or dim('(vazia)')}")
    print("-" * 60)

    confirm = input(f"Confirmar gravação em {cat_info['file'].name}? ({bold('S')}/n): ").strip().lower()
    if confirm in ["", "s", "sim", "y", "yes"]:
        new_item = {
            "id": str(next_id),
            "year": year,
            "title": title,
            "url": url,
        }
        items.append(new_item)
        save_items(cat_info["file"], items)
        print(green(f"\n✔ Item ID {next_id} inserido com sucesso em {get_display_path(cat_info['file'])}!"))

        pdf_path = f"assets/{cat_info['assets_folder']}/{next_id}.pdf"
        print(dim(f"ℹ Se desejar anexar um PDF a este item, salve-o como: {pdf_path}"))

        prompt_generate_site()
    else:
        print(yellow("\nOperação cancelada. Nenhuma alteração foi salva."))


def edit_item_flow(cat_info):
    """Fluxo interativo para edição de item existente."""
    items = load_items(cat_info["file"])
    if not items:
        print(yellow(f"\nNenhum item cadastrado em {cat_info['name']}."))
        input("\nPressione Enter para continuar...")
        return

    print("\n" + "=" * 60)
    print(bold(f" EDITAR ITEM: {cat_info['singular'].upper()}"))
    print("=" * 60)
    print(dim("O ID é fixo e NÃO pode ser alterado. Veja a lista abaixo para identificar o ID:"))
    print()

    # Mostra a lista completa inicialmente
    display_items(items, cat_info["assets_folder"])

    target_item = None
    while True:
        prompt_text = (
            f"\nDigite o {bold('ID')} do item a editar "
            f"(ou digite um texto para filtrar, ou '0' para cancelar): "
        )
        choice = input(prompt_text).strip()

        if choice in ["0", "c", "cancelar", "sair", "q", ""]:
            print(yellow("Edição cancelada."))
            return

        # Verifica se digitou ID numérico existente
        if choice.isdigit():
            for it in items:
                if str(it.get("id", "")).strip() == choice:
                    target_item = it
                    break

        if target_item:
            break
        else:
            # Tenta filtrar por texto se não for um ID exato
            matches = display_items(items, cat_info["assets_folder"], filter_text=choice)
            if not matches:
                print(red(f"⚠️ Nenhum item encontrado com o ID ou termo '{choice}'."))

    item_id = str(target_item["id"]).strip()
    print("\n" + "=" * 60)
    print(bold(f" Editando Item [ID: {cyan(item_id)}]"))
    print(dim(" (O ID é automático/permanente e nunca pode ser alterado)"))
    print("=" * 60)

    # Informações atuais
    print(f"ID atual:     {bold(cyan(item_id))} {dim('(bloqueado para edição)')}")
    print(f"Ano atual:    {target_item['year']}")
    print(f"Título atual: {target_item['title']}")
    print(f"URL atual:    {target_item['url'] or dim('(vazia)')}")

    has_pdf = check_pdf(cat_info["assets_folder"], item_id)
    pdf_rel = f"assets/{cat_info['assets_folder']}/{item_id}.pdf"
    if has_pdf:
        print(f"PDF vinculado: {green('Encontrado')} ({pdf_rel})")
    else:
        print(f"PDF vinculado: {dim('Não encontrado')} ({pdf_rel})")
    print("-" * 60)

    # Novo ano
    while True:
        new_year = input(f"Novo ano [Enter para manter '{target_item['year']}']: ").strip()
        if not new_year:
            new_year = target_item["year"]
            break
        if new_year.isdigit() and len(new_year) == 4:
            break
        print(yellow("⚠️ Informe um ano de 4 dígitos ou pressione Enter para manter."))

    # Novo título
    new_title = input(f"Novo título [Enter para manter o atual]: ").strip()
    if not new_title:
        new_title = target_item["title"]

    # Nova URL
    curr_url = target_item["url"]
    new_url_input = input(f"Nova URL [Enter para manter, '-' para limpar]: ").strip()
    if not new_url_input:
        new_url = curr_url
    elif new_url_input == "-":
        new_url = ""
    else:
        new_url = new_url_input

    # Resumo das alterações
    print("\n" + bold("Resumo das alterações:"))
    print(f"  ID:     {item_id} {dim('(inalterado)')}")
    year_diff = " (alterado)" if new_year != target_item["year"] else " (mantido)"
    print(f"  Ano:    {new_year}{year_diff}")
    title_diff = " (alterado)" if new_title != target_item["title"] else " (mantido)"
    print(f"  Título: {new_title}{title_diff}")
    url_diff = " (alterada)" if new_url != curr_url else " (mantida)"
    print(f"  URL:    {new_url or dim('(vazia)')}{url_diff}")
    print("-" * 60)

    confirm = input(f"Salvar alterações em {cat_info['file'].name}? ({bold('S')}/n): ").strip().lower()
    if confirm in ["", "s", "sim", "y", "yes"]:
        target_item["year"] = new_year
        target_item["title"] = new_title
        target_item["url"] = new_url
        save_items(cat_info["file"], items)
        print(green(f"\n✔ Item ID {item_id} atualizado com sucesso em {get_display_path(cat_info['file'])}!"))
        prompt_generate_site()
    else:
        print(yellow("\nAlterações descartadas."))


def delete_item_flow(cat_info):
    """Fluxo para exclusão de item com confirmação."""
    items = load_items(cat_info["file"])
    if not items:
        print(yellow(f"\nNenhum item cadastrado em {cat_info['name']}."))
        input("\nPressione Enter para continuar...")
        return

    print("\n" + "=" * 60)
    print(bold(f" EXCLUIR ITEM: {cat_info['singular'].upper()}"))
    print("=" * 60)
    display_items(items, cat_info["assets_folder"])

    choice = input(f"\nDigite o ID do item a excluir (ou '0' para cancelar): ").strip()
    if choice in ["0", "c", "cancelar", "sair", ""]:
        print(yellow("Exclusão cancelada."))
        return

    target_idx = None
    for idx, it in enumerate(items):
        if str(it.get("id", "")).strip() == choice:
            target_idx = idx
            break

    if target_idx is None:
        print(red(f"⚠️ ID '{choice}' não encontrado."))
        return

    target_item = items[target_idx]
    print(yellow(f"\n⚠️ Tem certeza que deseja excluir o item:"))
    print(f"  ID:     {target_item['id']}")
    print(f"  Ano:    {target_item['year']}")
    print(f"  Título: {target_item['title']}")
    print(dim("Atenção: essa ação removerá a linha do arquivo CSV."))

    confirm = input(f"\nDigite '{bold('sim')}' para confirmar a exclusão: ").strip().lower()
    if confirm in ["sim", "s"]:
        items.pop(target_idx)
        save_items(cat_info["file"], items)
        print(green(f"\n✔ Item ID {choice} excluído com sucesso de {cat_info['file'].name}!"))
        prompt_generate_site()
    else:
        print(yellow("Exclusão cancelada."))


def category_menu(cat_info):
    """Menu para gerenciar uma categoria específica."""
    while True:
        items = load_items(cat_info["file"])
        print("\n" + "=" * 60)
        print(bold(f" {cat_info['name'].upper()}"))
        print(dim(f" Arquivo: content/{cat_info['file'].name} | Total: {len(items)} itens"))
        print("=" * 60)
        print("  1. Adicionar novo item (ID automático)")
        print("  2. Editar item existente (escolha por ID)")
        print("  3. Listar todos os itens")
        print("  4. Excluir item")
        print("  0. Voltar ao menu principal")
        print("-" * 60)

        op = input("Escolha uma opção: ").strip()

        if op == "1":
            add_item_flow(cat_info)
        elif op == "2":
            edit_item_flow(cat_info)
        elif op == "3":
            print()
            display_items(items, cat_info["assets_folder"])
            input("\nPressione Enter para continuar...")
        elif op == "4":
            delete_item_flow(cat_info)
        elif op in ["0", "v", "voltar", "q"]:
            break
        else:
            print(red("Opção inválida. Escolha entre 0 e 4."))


def main_menu():
    """Menu interativo principal."""
    while True:
        print("\n" + "=" * 60)
        print(bold("        GERENCIADOR DE CONTEÚDO (CSV) - MODO INTERATIVO"))
        print("=" * 60)
        print("Escolha a seção que deseja gerenciar:\n")

        for key, cat in CATEGORIES.items():
            items = load_items(cat["file"])
            next_id = get_next_id(items)
            print(f"  {bold(key)}. {cat['name']:<35} [{len(items)} itens | próx. ID: {next_id}]")

        print(f"\n  {bold('G')}. Regerar o site agora (generate_site.py)")
        print(f"  {bold('0')}. Sair")
        print("-" * 60)

        op = input("Escolha uma opção: ").strip().lower()

        if op in CATEGORIES:
            category_menu(CATEGORIES[op])
        elif op in ["g", "gerar"]:
            run_generate_site()
        elif op in ["0", "s", "sair", "q", "exit"]:
            print(green("\nAté logo!"))
            break
        else:
            print(red("Opção inválida. Escolha uma opção do menu."))


def main():
    try:
        if len(sys.argv) > 1:
            arg = sys.argv[1].strip().lower()
            if arg in ["--help", "-h"]:
                print("Uso do Gerenciador de Conteúdo:")
                print("  python3 scripts/manage_content.py              (Modo interativo completo)")
                print("  python3 scripts/manage_content.py publications (Abre direto em Publicações)")
                print("  python3 scripts/manage_content.py documents    (Abre direto em Documentos)")
                print("  python3 scripts/manage_content.py courses      (Abre direto em Cursos)")
                print("  python3 scripts/manage_content.py talks        (Abre direto em Palestras)")
                print("  python3 scripts/manage_content.py generate     (Regera o site)")
                return

            if arg in ["generate", "build", "site", "-g"]:
                run_generate_site()
                return

            for key, cat in CATEGORIES.items():
                if arg in [cat["key"], key, cat["assets_folder"]]:
                    category_menu(cat)
                    return

            print(yellow(f"Opção '{arg}' não reconhecida. Iniciando modo interativo..."))

        main_menu()
    except KeyboardInterrupt:
        print(yellow("\n\nOperação interrompida pelo usuário. Até logo!"))
        sys.exit(0)


if __name__ == "__main__":
    main()
