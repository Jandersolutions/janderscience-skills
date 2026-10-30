#!/usr/bin/env python3
"""
SuperSkills Mesh Builder
=========================
Consolidates 1,300+ skills from `headcount` and `skills-ia` into:
1. Unified Agent Skills package aligned with `agentskills.io`
2. High-performance JSON Agent Registry for `Agentic Mesh`
3. Formal RDF/Turtle Knowledge Graph instances for `Open Ontologies`
"""

import os
import re
import json
import glob
from pathlib import Path
from typing import Dict, List, Any

# Root paths
BASE_DIR = Path(__file__).resolve().parent.parent
SOURCES_DIR = BASE_DIR / "sources"
REGISTRY_DIR = BASE_DIR / "registry"
ONTOLOGIES_DIR = BASE_DIR / "ontologies"
PACKAGES_DIR = BASE_DIR / "mesh_workforce"

REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
ONTOLOGIES_DIR.mkdir(parents=True, exist_ok=True)
PACKAGES_DIR.mkdir(parents=True, exist_ok=True)

# Mapping skills-ia categories to headcount standard departments
CATEGORY_TO_DEPARTMENT = {
    "carreira": "people",
    "codigo": "technology",
    "conteudo-copy": "demand-generation",
    "design-branding": "marketing",
    "direcao-criativa": "marketing",
    "financeiro": "finance",
    "juridico-advocacia": "legal-risk",
    "lideranca-equipes": "executive",
    "marketing": "marketing",
    "operacoes": "operations",
    "produto": "product",
    "rotina": "operations",
    "seo": "demand-generation"
}

# 16 Standard Headcount Departments and their missions
DEPARTMENTS_META = {
    "executive": {
        "name": "Office of the CEO & Strategy",
        "description": "Executive leadership, strategic direction, governance, board relations and high-level decision making.",
        "charter": "Set organizational purpose, allocate strategic capital, and own cross-functional escalation."
    },
    "corporate-strategy": {
        "name": "Corporate Strategy",
        "description": "Long-range strategic planning, M&A, competitive intelligence, and market positioning.",
        "charter": "Analyze competitive dynamics, assess industry disruption, and drive strategic portfolio choices."
    },
    "technology": {
        "name": "Technology & Engineering",
        "description": "Software engineering, system architecture, DevOps, APIs, and cloud infrastructure.",
        "charter": "Design, build, deploy, and maintain robust, scalable and secure technological systems."
    },
    "it-operations": {
        "name": "IT Operations & Infrastructure",
        "description": "Internal systems, enterprise IT tooling, workstation management, and network availability.",
        "charter": "Ensure operational uptime, seamless internal toolchains, and employee technological support."
    },
    "product": {
        "name": "Product Management",
        "description": "Product discovery, roadmap prioritization, feature specification, and UX alignment.",
        "charter": "Translate customer problems and strategic goals into delightful, viable product experiences."
    },
    "security": {
        "name": "Information Security (SecOps)",
        "description": "Cybersecurity, threat modeling, vulnerability management, compliance (SOC2/ISO27001) and incident response.",
        "charter": "Protect organizational assets, enforce zero-trust posture, and maintain security hygiene."
    },
    "data-analytics": {
        "name": "Data & Analytics",
        "description": "Business intelligence, data pipelines, warehousing, metric modeling, and predictive analytics.",
        "charter": "Transform raw operational data into trusted, actionable decision support models."
    },
    "marketing": {
        "name": "Brand & Product Marketing",
        "description": "Brand narrative, positioning, creative direction, design systems, and market messaging.",
        "charter": "Establish unmistakable brand identity and communicate value clearly to target markets."
    },
    "demand-generation": {
        "name": "Demand Generation & Growth",
        "description": "Paid media, SEO, performance marketing, content syndication, and inbound acquisition funnels.",
        "charter": "Generate sustainable, predictable pipeline of qualified leads and customers."
    },
    "revenue": {
        "name": "Revenue & Sales",
        "description": "Enterprise sales, sales engineering, pricing strategy, pipeline velocity, and revenue ops.",
        "charter": "Close revenue predictably, maximize contract values, and optimize sales cycles."
    },
    "customer-experience": {
        "name": "Customer Experience & Success",
        "description": "Onboarding, retention, customer support, NPS, churn prevention, and account expansion.",
        "charter": "Ensure customer value realization, minimize churn, and drive lifetime advocacy."
    },
    "finance": {
        "name": "Finance & Accounting",
        "description": "Budgeting, financial forecasting, FP&A, treasury, unit economics, and accounting controls.",
        "charter": "Maintain financial integrity, optimize capital runway, and ensure accurate fiscal reporting."
    },
    "operations": {
        "name": "Business Operations",
        "description": "Process optimization, workflow automation, operational cadence, and vendor procurement.",
        "charter": "Remove cross-functional friction and ensure reliable daily business execution."
    },
    "pmo": {
        "name": "Program Management Office (PMO)",
        "description": "Cross-functional initiative tracking, delivery milestones, dependency management, and project reporting.",
        "charter": "Keep complex multi-team initiatives on schedule, on budget, and unblocked."
    },
    "people": {
        "name": "People & Talent (HR)",
        "description": "Talent acquisition, organizational design, culture, career progression, and performance reviews.",
        "charter": "Attract, develop, and retain the highest-performing workforce while fostering healthy culture."
    },
    "legal-risk": {
        "name": "Legal, Compliance & Risk",
        "description": "Commercial contracts, IP protection, regulatory compliance (LGPD/GDPR), and liability management.",
        "charter": "Shield the enterprise from legal liability while enabling commercial velocity."
    }
}

def extract_frontmatter(content: str) -> Dict[str, str]:
    """Extracts yaml frontmatter from markdown file."""
    pattern = r"^---\s*\n(.*?)\n---\s*\n"
    match = re.search(pattern, content, re.DOTALL)
    if not match:
        return {}
    
    yaml_text = match.group(1)
    result = {}
    
    # Simple regex-based parser for key-value frontmatter
    # Handles multi-line descriptions or quoted strings
    lines = yaml_text.splitlines()
    current_key = None
    current_val = []
    
    for line in lines:
        kv_match = re.match(r"^([a-zA-Z0-9_\-]+)\s*:\s*(.*)$", line)
        if kv_match:
            if current_key:
                result[current_key] = " ".join(current_val).strip().strip('"\'')
            current_key = kv_match.group(1)
            first_val = kv_match.group(2).strip()
            current_val = [first_val] if first_val else []
        elif current_key and line.startswith(("  ", "    ", "\t")):
            current_val.append(line.strip())
            
    if current_key:
        result[current_key] = " ".join(current_val).strip().strip('"\'')
        
    return result

def determine_autonomy_tier(skill_name: str, desc: str, dept: str) -> int:
    """
    Agentic Mesh 7-Layer Trust Matrix:
    Tier 1: Read-only, research, advisory, draft creation (Low risk, fully autonomous)
    Tier 2: Code generation, configuration, internal review (Audited action)
    Tier 3: Financial movement, legal signing, production deploy, security privilege changes (Human-in-the-Loop)
    """
    text = f"{skill_name} {desc}".lower()
    high_risk_keywords = ["covenants", "treasury", "wire", "transfer", "cfo", "deploy-prod", "privilege", "signing", "lawsuit", "demissao", "pagamento"]
    if any(k in text for k in high_risk_keywords) or dept in ["executive", "legal-risk"]:
        return 3
    
    medium_risk_keywords = ["code", "deploy", "database", "api", "budget", "pricing", "contract", "recruiting", "pipeline"]
    if any(k in text for k in medium_risk_keywords) or dept in ["technology", "finance", "security"]:
        return 2
        
    return 1

def collect_headcount_skills() -> List[Dict[str, Any]]:
    skills = []
    pattern = str(SOURCES_DIR / "headcount" / "plugins" / "*" / "skills" / "*" / "SKILL.md")
    for path_str in glob.glob(pattern):
        p = Path(path_str)
        skill_slug = p.parent.name
        dept_slug = p.parent.parent.parent.name
        
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
            fm = extract_frontmatter(content)
            name = fm.get("name", skill_slug)
            desc = fm.get("description", "")
            
            # If description missing, extract first markdown paragraph
            if not desc:
                body = content.split("---", 2)[-1].strip()
                desc = body.split("\n\n")[0].replace("#", "").strip()[:250]
                
            tier = determine_autonomy_tier(name, desc, dept_slug)
            
            skills.append({
                "id": f"hc-{dept_slug}-{name}",
                "name": name,
                "slug": skill_slug,
                "source": "headcount",
                "department": dept_slug,
                "language": "en-US",
                "description": desc,
                "autonomy_tier": tier,
                "path": str(p.relative_to(BASE_DIR)).replace("\\", "/")
            })
        except Exception as e:
            print(f"Error reading {p}: {e}")
            
    return skills

def collect_skills_ia() -> List[Dict[str, Any]]:
    skills = []
    # In skills-ia, structure is sources/skills-ia/skills/<category>/skills/<skill-slug>/SKILL.md
    pattern = str(SOURCES_DIR / "skills-ia" / "skills" / "*" / "skills" / "*" / "SKILL.md")
    for path_str in glob.glob(pattern):
        p = Path(path_str)
        skill_slug = p.parent.name
        category_slug = p.parent.parent.parent.name
        dept_slug = CATEGORY_TO_DEPARTMENT.get(category_slug, "operations")
        
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
            fm = extract_frontmatter(content)
            name = fm.get("name", skill_slug)
            desc = fm.get("description", "")
            
            if not desc:
                body = content.split("---", 2)[-1].strip()
                desc = body.split("\n\n")[0].replace("#", "").strip()[:250]
                
            tier = determine_autonomy_tier(name, desc, dept_slug)
            
            skills.append({
                "id": f"ia-{dept_slug}-{name}",
                "name": name,
                "slug": skill_slug,
                "source": "skills-ia",
                "category": category_slug,
                "department": dept_slug,
                "language": "pt-BR",
                "description": desc,
                "autonomy_tier": tier,
                "path": str(p.relative_to(BASE_DIR)).replace("\\", "/")
            })
        except Exception as e:
            print(f"Error reading {p}: {e}")
            
    return skills

def generate_rdf_turtle(all_skills: List[Dict[str, Any]]) -> str:
    """Generates RDF Turtle knowledge graph of departments and skills."""
    lines = [
        "@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .",
        "@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .",
        "@prefix owl: <http://www.w3.org/2002/07/owl#> .",
        "@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .",
        "@prefix mesh: <https://agentskills.io/mesh#> .",
        "@prefix dcterms: <http://purl.org/dc/terms/> .",
        "",
        "# -------------------------------------------------------------",
        "# Departments Instances",
        "# -------------------------------------------------------------"
    ]
    
    for dept_id, info in DEPARTMENTS_META.items():
        lines.append(f"mesh:Dept_{dept_id} a mesh:Department ;")
        lines.append(f'    rdfs:label "{info["name"]}" ;')
        lines.append(f'    dcterms:description "{info["description"]}" ;')
        lines.append(f'    mesh:charter "{info["charter"]}" .')
        lines.append("")
        
    lines.append("# -------------------------------------------------------------")
    lines.append(f"# Skills Instances (Total: {len(all_skills)})")
    lines.append("# -------------------------------------------------------------")
    
    for s in all_skills:
        clean_id = re.sub(r"[^a-zA-Z0-9_]", "_", s["id"])
        # Escape quotes in description
        clean_desc = s["description"].replace('"', '\\"').replace('\n', ' ')
        clean_name = s["name"].replace('"', '\\"')
        lines.append(f"mesh:Skill_{clean_id} a mesh:Skill ;")
        lines.append(f'    mesh:skillIdentifier "{s["id"]}" ;')
        lines.append(f'    rdfs:label "{clean_name}" ;')
        lines.append(f'    mesh:belongsToDepartment mesh:Dept_{s["department"]} ;')
        lines.append(f'    mesh:autonomyTier {s["autonomy_tier"]} ;')
        lines.append(f'    mesh:language "{s["language"]}" ;')
        lines.append(f'    mesh:skillSourcePath "{s["path"]}" ;')
        lines.append(f'    mesh:skillDescription "{clean_desc}" .')
        lines.append("")
        
    return "\n".join(lines)

def main():
    print("[1/4] Scanning headcount skills...")
    hc_skills = collect_headcount_skills()
    print(f"      Found {len(hc_skills)} headcount skills across {len(DEPARTMENTS_META)} departments.")
    
    print("[2/4] Scanning skills-ia skills...")
    ia_skills = collect_skills_ia()
    print(f"      Found {len(ia_skills)} skills-ia skills.")
    
    all_skills = hc_skills + ia_skills
    total = len(all_skills)
    print(f"[3/4] Aggregated total: {total} specialized skills.")
    
    # Save Master JSON Registry
    registry_data = {
        "metadata": {
            "title": "SuperSkills Mesh Master Registry",
            "version": "1.0.0",
            "spec": "agentskills.io v1",
            "total_skills": total,
            "total_departments": len(DEPARTMENTS_META),
            "sources": ["tiagopgr/skills-ia", "cbrock84/headcount"]
        },
        "departments": DEPARTMENTS_META,
        "skills": all_skills
    }
    
    registry_file = REGISTRY_DIR / "mesh_registry.json"
    registry_file.write_text(json.dumps(registry_data, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"      Wrote Master Registry to: {registry_file}")
    
    # Save RDF Turtle Knowledge Graph
    print("[4/4] Emitting semantic RDF Turtle knowledge graph...")
    rdf_turtle = generate_rdf_turtle(all_skills)
    ttl_file = ONTOLOGIES_DIR / "workforce_instances.ttl"
    ttl_file.write_text(rdf_turtle, encoding="utf-8")
    print(f"      Wrote Knowledge Graph to: {ttl_file} ({os.path.getsize(ttl_file):,} bytes)")
    
    print("\n[SUCCESS] SuperSkills Mesh Registry & Ontologies successfully generated!")

if __name__ == "__main__":
    main()
