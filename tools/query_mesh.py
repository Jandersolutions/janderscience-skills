#!/usr/bin/env python3
"""
SuperSkills Mesh CLI & Fast Router
===================================
Query, discover, and inspect 1,330+ skills across 16 corporate departments.
Implements the Progressive Disclosure paradigm from agentskills.io and Agentic Mesh.

Usage:
  python tools/query_mesh.py search "SEO e funil"
  python tools/query_mesh.py dept finance
  python tools/query_mesh.py get hc-finance-chief-financial-officer
  python tools/query_mesh.py stats
"""

import sys
import json
from pathlib import Path

REGISTRY_PATH = Path(__file__).resolve().parent.parent / "registry" / "mesh_registry.json"

def load_registry():
    if not REGISTRY_PATH.exists():
        print(f"Error: Registry not found at {REGISTRY_PATH}. Run 'python tools/mesh_builder.py' first.")
        sys.exit(1)
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def show_stats(data):
    meta = data["metadata"]
    skills = data["skills"]
    depts = data["departments"]
    
    print("\n" + "="*60)
    print(f"  {meta['title']} v{meta['version']}")
    print("="*60)
    print(f"Total Skills Mapped      : {meta['total_skills']}")
    print(f"Total Departments        : {meta['total_departments']}")
    print(f"Specification Compliance : {meta['spec']}")
    print(f"Sources                  : {', '.join(meta['sources'])}")
    print("-"*60)
    
    tier_counts = {1: 0, 2: 0, 3: 0}
    lang_counts = {}
    dept_counts = {}
    
    for s in skills:
        tier_counts[s.get("autonomy_tier", 1)] += 1
        lang = s.get("language", "unknown")
        lang_counts[lang] = lang_counts.get(lang, 0) + 1
        dept = s.get("department", "unknown")
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
        
    print("\nAutonomy Tiers (Agentic Mesh Trust Framework):")
    print(f"  Tier 1 (Read-Only / Research)        : {tier_counts[1]} skills")
    print(f"  Tier 2 (Audited Action / Internal)   : {tier_counts[2]} skills")
    print(f"  Tier 3 (High-Risk / Human Approval)  : {tier_counts[3]} skills")
    
    print("\nLanguage Distribution:")
    for lang, count in sorted(lang_counts.items(), key=lambda x: -x[1]):
        print(f"  {lang:<10} : {count:>4} skills")
        
    print("\nDepartment Breakdown (16 Departments):")
    for dept_id, info in depts.items():
        count = dept_counts.get(dept_id, 0)
        print(f"  {dept_id:<22} ({info['name']:<32}): {count:>4} skills")
    print("="*60 + "\n")

def search_skills(data, query, limit=10):
    q = query.lower()
    skills = data["skills"]
    results = []
    
    for s in skills:
        score = 0
        name = s["name"].lower()
        desc = s["description"].lower()
        dept = s["department"].lower()
        
        if q in name:
            score += 10
        if q in desc:
            score += 5
        if q in dept:
            score += 3
            
        # Token match
        words = q.split()
        for w in words:
            if w in name:
                score += 3
            if w in desc:
                score += 1
                
        if score > 0:
            results.append((score, s))
            
    results.sort(key=lambda x: -x[0])
    
    print(f"\nSearch results for: '{query}' (Found {len(results)} matches, showing top {min(limit, len(results))}):\n")
    for i, (score, s) in enumerate(results[:limit], 1):
        tier_icon = "[T1:Read]" if s["autonomy_tier"] == 1 else ("[T2:Audit]" if s["autonomy_tier"] == 2 else "[T3:HITL]")
        print(f"{i:2d}. {tier_icon} {s['id']}")
        print(f"    Department : {s['department']} | Lang: {s['language']}")
        print(f"    Desc       : {s['description'][:140]}...")
        print(f"    Path       : {s['path']}\n")

def list_department(data, dept_slug):
    depts = data["departments"]
    if dept_slug not in depts:
        print(f"Department '{dept_slug}' not found. Available: {', '.join(depts.keys())}")
        return
        
    info = depts[dept_slug]
    skills = [s for s in data["skills"] if s["department"] == dept_slug]
    
    print("\n" + "="*70)
    print(f"  Department: {info['name']} ({dept_slug})")
    print("="*70)
    print(f"Mission : {info['description']}")
    print(f"Charter : {info['charter']}")
    print(f"Skills  : {len(skills)} mapped capabilities")
    print("-"*70)
    
    for i, s in enumerate(skills, 1):
        tier = f"T{s['autonomy_tier']}"
        print(f"{i:3d}. [{tier}] {s['name']:<42} ({s['language']}) - ID: {s['id']}")
    print("="*70 + "\n")

def inspect_skill(data, skill_id):
    skill = next((s for s in data["skills"] if s["id"] == skill_id or s["name"] == skill_id), None)
    if not skill:
        print(f"Skill '{skill_id}' not found.")
        return
        
    print("\n" + "="*70)
    print(f"  SKILL: {skill['name']}")
    print("="*70)
    print(f"ID            : {skill['id']}")
    print(f"Department    : {skill['department']}")
    print(f"Source Repo   : {skill['source']}")
    print(f"Language      : {skill['language']}")
    print(f"Autonomy Tier : Tier {skill['autonomy_tier']}")
    print(f"Path          : {skill['path']}")
    print("-"*70)
    print("Activation Description (Loaded in Discovery Phase):")
    print(f"\"{skill['description']}\"")
    print("-"*70)
    
    # Read full SKILL.md content
    full_path = Path(__file__).resolve().parent.parent / skill['path']
    if full_path.exists():
        print("Full SKILL.md Content Preview (Loaded in Activation Phase):")
        lines = full_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        preview = lines[:35]
        print("\n".join(preview))
        if len(lines) > 35:
            print(f"\n... [{len(lines)-35} lines truncated. Full instructions available at {skill['path']}]")
    print("="*70 + "\n")

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)
        
    cmd = sys.argv[1].lower()
    data = load_registry()
    
    if cmd == "stats":
        show_stats(data)
    elif cmd == "search":
        if len(sys.argv) < 3:
            print("Usage: python tools/query_mesh.py search <query>")
            return
        query = " ".join(sys.argv[2:])
        search_skills(data, query)
    elif cmd == "dept":
        if len(sys.argv) < 3:
            print("Usage: python tools/query_mesh.py dept <dept-slug>")
            return
        list_department(data, sys.argv[2].lower())
    elif cmd == "get":
        if len(sys.argv) < 3:
            print("Usage: python tools/query_mesh.py get <skill-id>")
            return
        inspect_skill(data, sys.argv[2])
    else:
        # Fallback to search
        search_skills(data, " ".join(sys.argv[1:]))

if __name__ == "__main__":
    main()
