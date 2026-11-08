#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Audit Markdown source, standalone card JSON, and mini-program payloads.

Run after tools/build.py so dist/miniprogram and miniprogram/data are freshly generated.
Writes CONSISTENCY_MATRIX.csv and CONSISTENCY_ISSUES.csv at repository root.
"""
import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLS = ROOT / "tools"
CARDS = TOOLS / "cards"
sys.path.insert(0, str(TOOLS))
sys.path.insert(0, str(CARDS))

import build  # noqa: E402
import embed  # noqa: E402


def dump(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def write_csv(path, headers, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)


def main():
    issues = []
    kps, errors, warnings = build.load_knowledge_points()
    _, curriculum_errors = build.load_curriculum(kps)
    for item in errors + curriculum_errors:
        issues.append({"code": "SOURCE_INVALID", "level": "P1", "id": "",
                       "source": "content/", "detail": item})

    source = {kp["id"]: kp for kp in kps}
    if len(source) != len(kps):
        issues.append({"code": "DUPLICATE_SOURCE_ID", "level": "P1", "id": "",
                       "source": "content/", "detail": "Markdown source IDs are not unique"})

    mini_dir = ROOT / "miniprogram" / "data"
    dist_dir = ROOT / "dist" / "miniprogram"
    mini_by_id = {}
    mini_file_by_id = {}
    mini_by_module = {}
    for path in sorted(mini_dir.glob("m[0-9][0-9].json")):
        try:
            records = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            issues.append({"code": "MINI_JSON_INVALID", "level": "P1", "id": "",
                           "source": str(path.relative_to(ROOT)), "detail": str(exc)})
            continue
        mini_by_module[path.stem] = records
        for item in records:
            kid = item.get("id", "")
            if kid in mini_by_id:
                issues.append({"code": "DUPLICATE_MINI_ID", "level": "P1", "id": kid,
                               "source": str(path.relative_to(ROOT)), "detail": "Duplicate mini-program ID"})
            mini_by_id[kid] = item
            mini_file_by_id[kid] = path.name

    for kid in sorted(set(source) - set(mini_by_id)):
        issues.append({"code": "MISSING_MINI_RECORD", "level": "P1", "id": kid,
                       "source": source[kid]["file"], "detail": "No mini-program record"})
    for kid in sorted(set(mini_by_id) - set(source)):
        issues.append({"code": "ORPHAN_MINI_RECORD", "level": "P1", "id": kid,
                       "source": mini_file_by_id[kid], "detail": "Mini-program ID has no Markdown source"})

    fields = ["id", "title", "module", "grade", "tags", "difficulty", "skills",
              "related", "lecture", "examples", "variants"]
    mini_status = {}
    for kid in sorted(set(source) & set(mini_by_id)):
        expected = {key: source[kid].get(key) for key in fields}
        actual = {key: mini_by_id[kid].get(key) for key in fields}
        if dump(expected) != dump(actual):
            diff = [key for key in fields if dump(expected.get(key)) != dump(actual.get(key))]
            mini_status[kid] = "DIFF:" + "|".join(diff)
            issues.append({"code": "MINI_CONTENT_DRIFT", "level": "P1", "id": kid,
                           "source": mini_file_by_id[kid], "detail": "Fields differ: " + ", ".join(diff)})
        else:
            mini_status[kid] = "exact"

    for path in sorted(dist_dir.glob("m[0-9][0-9].json")):
        source_path = mini_dir / path.name
        if not source_path.exists():
            issues.append({"code": "DIST_MODULE_MISSING_SOURCE", "level": "P1", "id": "",
                           "source": str(path.relative_to(ROOT)), "detail": "No matching mini-program source file"})
            continue
        try:
            if dump(json.loads(path.read_text(encoding="utf-8"))) != dump(
                    json.loads(source_path.read_text(encoding="utf-8"))):
                issues.append({"code": "DIST_MINI_DRIFT", "level": "P1", "id": "",
                               "source": str(path.relative_to(ROOT)), "detail": "dist differs from miniprogram/data"})
        except Exception as exc:
            issues.append({"code": "DIST_JSON_INVALID", "level": "P1", "id": "",
                           "source": str(path.relative_to(ROOT)), "detail": str(exc)})

    manifest_expected = []
    for slug, records in sorted(mini_by_module.items()):
        if records:
            manifest_expected.append({"slug": slug, "module": records[0]["module"],
                                      "count": len(records), "file": slug + ".json"})
    for directory in (mini_dir, dist_dir):
        manifest_path = directory / "manifest.json"
        try:
            actual_manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            if dump(actual_manifest) != dump(manifest_expected):
                issues.append({"code": "MANIFEST_DRIFT", "level": "P1", "id": "",
                               "source": str(manifest_path.relative_to(ROOT)),
                               "detail": "Manifest counts/modules do not match module JSON files"})
        except Exception as exc:
            issues.append({"code": "MANIFEST_INVALID", "level": "P1", "id": "",
                           "source": str(manifest_path.relative_to(ROOT)), "detail": str(exc)})

    card_items = []
    card_files = sorted((CARDS / "content").glob("[0-9]*.json"))
    for path in card_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            for item in data.get("items", []):
                item["_file"] = str(path.relative_to(ROOT))
                card_items.append(item)
        except Exception as exc:
            issues.append({"code": "CARD_JSON_INVALID", "level": "P1", "id": "",
                           "source": str(path.relative_to(ROOT)), "detail": str(exc)})

    card_by_id = {}
    for item in card_items:
        kid = item.get("id", "")
        if kid in card_by_id:
            issues.append({"code": "DUPLICATE_CARD_ID", "level": "P1", "id": kid,
                           "source": item["_file"], "detail": "Duplicate standalone card ID"})
        card_by_id[kid] = item
        if kid not in source:
            issues.append({"code": "ORPHAN_CARD_ID", "level": "P1", "id": kid,
                           "source": item["_file"], "detail": "Card ID has no Markdown source"})

    badges = embed.id_badge_map()
    card_status = {}
    for kid, item in sorted(card_by_id.items()):
        if kid not in source:
            card_status[kid] = "orphan"
            continue
        md_path = ROOT / source[kid]["file"]
        md_text = md_path.read_text(encoding="utf-8")
        if kid in embed.MANUAL_MD:
            if "## 速查卡" not in md_text:
                issues.append({"code": "MANUAL_CARD_MISSING", "level": "P1", "id": kid,
                               "source": source[kid]["file"], "detail": "Manual card section is missing"})
                card_status[kid] = "manual-missing"
            else:
                card_status[kid] = "manual-reviewed-separately"
            continue
        match = re.search(r"<!-- card:auto -->[\s\S]*?<!-- /card:auto -->\n*", md_text)
        if not match:
            issues.append({"code": "EMBEDDED_CARD_MISSING", "level": "P1", "id": kid,
                           "source": source[kid]["file"], "detail": "Generated card block is missing"})
            card_status[kid] = "missing"
            continue
        expected_block = embed.blocks_to_md(item.get("blocks") or [], badges.get(kid, "?"),
                                            md_text, item.get("title", ""))
        if match.group(0) != expected_block:
            issues.append({"code": "CARD_EMBED_DRIFT", "level": "P1", "id": kid,
                           "source": source[kid]["file"], "detail": "Embedded Markdown card differs from standalone JSON"})
            card_status[kid] = "drift"
        else:
            card_status[kid] = "exact"

    matrix = []
    for kid, kp in sorted(source.items()):
        card = card_by_id.get(kid)
        matrix.append({
            "id": kid,
            "title": kp["title"],
            "module": kp["module"],
            "module_file": mini_file_by_id.get(kid, ""),
            "markdown_file": kp["file"],
            "mini_record": "yes" if kid in mini_by_id else "no",
            "mini_content": mini_status.get(kid, "missing"),
            "card_source": "yes" if card else "no",
            "card_title": card.get("title", "") if card else "",
            "card_source_file": card.get("_file", "") if card else "",
            "embedded_card": card_status.get(kid, "not-applicable"),
            "grade": dump(kp.get("grade")),
            "skills_count": len(kp.get("skills") or []),
            "examples_count": len(kp.get("examples") or []),
            "variants_count": len(kp.get("variants") or []),
        })

    matrix_fields = ["id", "title", "module", "module_file", "markdown_file", "mini_record",
                     "mini_content", "card_source", "card_title", "card_source_file",
                     "embedded_card", "grade", "skills_count", "examples_count", "variants_count"]
    issue_fields = ["code", "level", "id", "source", "detail"]
    write_csv(ROOT / "CONSISTENCY_MATRIX.csv", matrix_fields, matrix)
    write_csv(ROOT / "CONSISTENCY_ISSUES.csv", issue_fields, issues)

    print("T8 consistency audit")
    print(f"Markdown source: {len(source)} IDs")
    print(f"Mini-program: {len(mini_by_id)} unique IDs in {len(mini_by_module)} modules")
    print(f"Standalone cards: {len(card_by_id)} IDs in {len(card_files)} JSON files")
    print(f"Card blocks: {sum(1 for value in card_status.values() if value == 'exact')} exact, "
          f"{sum(1 for value in card_status.values() if value == 'manual-reviewed-separately')} manual")
    print(f"Issues: {len(issues)}")
    if issues:
        for issue in issues[:100]:
            print(f"[{issue['level']}] {issue['code']} {issue['id']} {issue['detail']}")
        return 1
    print("PASS: Markdown, standalone card JSON, mini-program data and generated dist are aligned.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
