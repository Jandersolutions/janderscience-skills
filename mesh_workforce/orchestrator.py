#!/usr/bin/env python3
"""
Agentic Mesh Multi-Agent Fleet Orchestrator
===========================================
Implements the Agentic Mesh architecture (Eric & Davis Broda) to coordinate
specialized microagents and skills across the 16 corporate departments.

Features:
- Fleet Formation (Hierarchical & Swarm Topologies)
- Mission Decomposition via the Reliability Triad
- 7-Layer Trust Matrix & Human-in-the-Loop (HITL) Gatekeeping
- Progressive Disclosure of Skill Prompts
"""

import sys
import json
from pathlib import Path
from typing import Dict, List, Any

BASE_DIR = Path(__file__).resolve().parent.parent
REGISTRY_PATH = BASE_DIR / "registry" / "mesh_registry.json"

class MeshOrchestrator:
    def __init__(self):
        with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.skills = self.data["skills"]
        self.departments = self.data["departments"]

    def plan_mission(self, mission_goal: str) -> Dict[str, Any]:
        """Decomposes a corporate mission into departmental microagent tasks."""
        goal_lower = mission_goal.lower()
        
        # 0. System 1 Decision Layer (Jev & Laya Triage, Calibrated Tiers & Hard Veto)
        s1_data = None
        try:
            sys.path.insert(0, str(BASE_DIR))
            from tools.mesh_systemone import dispatch_decision
            s1_eval = dispatch_decision(mission_goal)
            s1_data = s1_eval.get("results", {})
        except Exception:
            s1_data = None

        # 1. Department matching
        selected_depts = []
        if s1_data and "department" in s1_data:
            primary_dept = s1_data["department"]["winner"]
            selected_depts.append(primary_dept)
            for cand_dept, prob in s1_data["department"].get("probabilities", {}).items():
                if cand_dept != primary_dept and prob >= 0.08 and cand_dept not in selected_depts:
                    selected_depts.append(cand_dept)

        dept_keywords = {
            "executive": ["estratégia", "investidor", "valuation", "ceo", "decisão", "fundraising", "board", "empresa"],
            "corporate-strategy": ["m&a", "fusão", "aquisição", "mercado", "concorrência", "longo prazo"],
            "technology": ["software", "código", "api", "sistema", "devops", "cloud", "infra", "arquitetura", "banco de dados"],
            "security": ["segurança", "vulnerabilidade", "lgpd", "iso27001", "soc2", "firewall", "hacker", "pentest"],
            "product": ["produto", "feature", "roadmap", "ux", "mvp", "lançamento", "usuário"],
            "finance": ["financeiro", "orçamento", "fluxo de caixa", "custo", "margem", "dre", "contabilidade", "preço", "investimento"],
            "marketing": ["marketing", "marca", "branding", "posicionamento", "design", "copy", "criativo"],
            "demand-generation": ["tráfego", "lead", "seo", "conversão", "anúncio", "campanha", "growth", "inbound", "landing page"],
            "revenue": ["vendas", "sdr", "fechamento", "proposta comercial", "pipeline", "negociação"],
            "legal-risk": ["jurídico", "contrato", "compliance", "processo", "termo", "risco", "privacidade"],
            "people": ["rh", "contratação", "onboarding", "equipe", "salário", "recrutamento", "demissão"],
            "operations": ["operação", "processo", "fornecedor", "rotina", "eficiência", "logística"]
        }
        
        for dept_id, kws in dept_keywords.items():
            if any(k in goal_lower for k in kws) and dept_id not in selected_depts:
                selected_depts.append(dept_id)
                
        if not selected_depts:
            selected_depts = ["executive", "operations"]
            
        # 2. Select relevant skills for each department
        plan_steps = []
        overall_max_tier = 1
        
        for dept_id in selected_depts:
            dept_skills = [s for s in self.skills if s["department"] == dept_id]
            # Match top 1-2 skills
            matched = []
            for s in dept_skills:
                score = sum(1 for word in goal_lower.split() if word in s["name"].lower() or word in s["description"].lower())
                if score > 0:
                    matched.append((score, s))
            matched.sort(key=lambda x: -x[0])
            
            chosen_skills = [m[1] for m in matched[:2]]
            if not chosen_skills and dept_skills:
                chosen_skills = [dept_skills[0]]
                
            for cs in chosen_skills:
                tier = cs["autonomy_tier"]
                if tier > overall_max_tier:
                    overall_max_tier = tier
                plan_steps.append({
                    "department": dept_id,
                    "dept_name": self.departments[dept_id]["name"],
                    "skill_id": cs["id"],
                    "skill_name": cs["name"],
                    "autonomy_tier": tier,
                    "action_type": "Human-in-the-Loop Required" if tier == 3 else ("Audited Execution" if tier == 2 else "Autonomous Execution"),
                    "instruction": cs["description"][:160] + "...",
                    "skill_path": cs["path"]
                })
                
        veto_flag = False
        veto_prob = 0.0
        if s1_data and "compliance_veto" in s1_data:
            veto_prob = s1_data["compliance_veto"].get("probability", 0.0)
            veto_flag = s1_data["compliance_veto"].get("verdict") == "VETO_REQUIRED"

        return {
            "mission": mission_goal,
            "governance": {
                "max_autonomy_tier": overall_max_tier,
                "requires_human_approval": overall_max_tier >= 3,
                "hard_veto_triggered": veto_flag,
                "hard_veto_risk": f"{veto_prob*100:.1f}%",
                "system_one_active": s1_data is not None,
                "compliance_framework": "Agentic Mesh 7-Layer Trust Matrix"
            },
            "departments_involved": [self.departments[d]["name"] for d in selected_depts],
            "execution_plan": plan_steps
        }

def main():
    if len(sys.argv) < 2:
        mission = "Lançar novo SaaS B2B com contrato de serviço, campanha de tráfego pago e modelo financeiro de receita"
    else:
        mission = " ".join(sys.argv[1:])
        
    orchestrator = MeshOrchestrator()
    plan = orchestrator.plan_mission(mission)
    
    print("\n" + "="*70)
    print("  AGENTIC MESH: MULTI-AGENT MISSION PLANNER")
    print("="*70)
    print(f"Mission Goal : \"{plan['mission']}\"")
    print(f"Departments  : {', '.join(plan['departments_involved'])}")
    print(f"Max Tier     : Tier {plan['governance']['max_autonomy_tier']}")
    print(f"Approval Req : {'SIM (Human-in-the-Loop Triggered)' if plan['governance']['requires_human_approval'] else 'NAO (Autonomia Concedida)'}")
    if plan['governance']['hard_veto_triggered']:
        print(f"🚨 HARD VETO : ATIVADO (Risco Regulatório/Legal: {plan['governance']['hard_veto_risk']})")
        print("              Ação suspensa preventivamente pelo Conselho Executivo.")
    print("-"*70)
    print("Decomposed Agent Execution Pipeline:")
    
    for i, step in enumerate(plan['execution_plan'], 1):
        tier_label = f"Tier {step['autonomy_tier']}"
        print(f"\n[Step {i}] {step['dept_name']} | Skill: {step['skill_name']}")
        print(f"       Policy      : [{tier_label}] {step['action_type']}")
        print(f"       Description : {step['instruction']}")
        print(f"       Path        : {step['skill_path']}")
        
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    main()
