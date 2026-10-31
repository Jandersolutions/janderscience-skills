#!/usr/bin/env python3
"""
JanderScience Skills - System 1 Decision Layer (Jev & Laya Adapter)
===================================================================
Implements non-autoregressive System 1 decision-making for the Agentic Mesh:
- Fast department triage across 16 corporate departments
- Calibrated Autonomy Tier evaluation (Tier 1 / Tier 2 / Tier 3)
- Hard Veto & Compliance guardrail checks (Legal / SecOps)
- Supports both TypeSafe Jev API (cloud) and Laya (local ONNX/Python)

Specification: https://jevai.net | https://github.com/NandhaKishorM/laya
Architecture: JanderScience Skills + Agentic Mesh (Broda & Broda)
"""

import os
import sys
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

BASE_DIR = Path(__file__).resolve().parent.parent
REGISTRY_FILE = BASE_DIR / "registry" / "mesh_registry.json"

# Department definitions for System 1 Choice Question
DEPARTMENTS_OPTIONS = {
    "executive": "Office of the CEO: Liderança executiva, estratégia macro, fusões e escalada de decisões",
    "corporate-strategy": "Corporate Strategy: Planejamento estratégico de longo prazo e inteligência competitiva",
    "technology": "Technology & Engineering: Desenvolvimento de software, código, arquitetura, devops e APIs",
    "it-operations": "IT Operations: Infraestrutura interna, ferramentas corporativas e suporte técnico",
    "product": "Product Management: Descoberta de produto, roadmap, UX e especificações funcionais",
    "security": "Information Security (SecOps): Cibersegurança, modelagem de ameaças, zero-trust e resposta a incidentes",
    "data-analytics": "Data & Analytics: Business intelligence, pipelines de dados, métricas e análises preditivas",
    "marketing": "Brand & Product Marketing: Narrativa de marca, branding, design systems e posicionamento",
    "demand-generation": "Demand Generation: Tráfego pago, SEO, copywriting persuasivo e funis de vendas",
    "revenue": "Revenue & Sales: Vendas B2B/Enterprise, propostas comerciais, precificação e fechamento",
    "customer-experience": "Customer Experience: Sucesso do cliente, suporte, retenção, pós-venda e NPS",
    "finance": "Finance & Accounting: Gestão financeira, tributário, valuation, fluxo de caixa e unit economics",
    "operations": "Business Operations: Otimização de processos, fluxos de trabalho e rotinas operacionais",
    "pmo": "PMO: Gestão de projetos, cronogramas, marcos de entrega e dependências entre equipes",
    "people": "People & Talent (HR): Recrutamento, planos de carreira, cultura e gestão de pessoas",
    "legal-risk": "Legal, Compliance & Risk: Contratos, LGPD, litígios, termos de serviço e risco regulatório"
}

def build_decision_payload(state_text: str) -> Dict[str, Any]:
    """
    Builds standard System 1 Question Schema compatible with both Jev API and Laya.
    Contains three concurrent decision dimensions:
    1. department (choice) -> Routes to 1 of 16 departments
    2. autonomy_tier (choice) -> Evaluates Tier 1 (Read), Tier 2 (Audited), Tier 3 (HITL)
    3. compliance_veto (noul) -> Calibrated probability of hard veto / regulatory danger
    """
    return {
        "model": "jev-latest",  # or "laya-multilingual"
        "state": state_text,
        "questions": {
            "department": {
                "type": "choice",
                "instructions": "Qual departamento corporativo possui autoridade primária para resolver essa demanda?",
                "options": DEPARTMENTS_OPTIONS
            },
            "autonomy_tier": {
                "type": "choice",
                "instructions": "Avalie o nível de risco e autoridade exigido pela ação conforme a Matriz de Confiança em 7 Camadas do Agentic Mesh:",
                "options": {
                    "tier_1": "Tier 1: Leitura, pesquisa, redação de rascunhos consultivos (execução autônoma permitida, sem efeitos colaterais externos)",
                    "tier_2": "Tier 2: Ação interna auditada, geração de código, alteração de banco/staging (requer registro em log e limites de escrita)",
                    "tier_3": "Tier 3: Alto risco, movimentação financeira, rescisão/processo judicial, demissão, deploy de produção (aprovação humana obrigatória / HITL)"
                }
            },
            "compliance_veto": {
                "type": "noul",
                "instructions": "A solicitação envolve ameaça iminente de litígio legal, violação de LGPD, quebra contratual grave ou risco de segurança crítico"
            }
        }
    }

def evaluate_via_jev_api(payload: Dict[str, Any], api_key: str) -> Dict[str, Any]:
    """Calls TypeSafe Jev API (https://jevai.net)"""
    import urllib.request
    
    url = "https://api.typesafe.ai/v1/systemone"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers=headers,
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))

def evaluate_heuristic_simulated(state_text: str) -> Dict[str, Any]:
    """
    High-fidelity offline calibrated simulator matching Laya / Jev response format.
    Used for local testing when API key is not present or offline demonstration.
    """
    text_lower = state_text.lower()
    
    # 1. Department scoring
    dept_scores = {}
    for d, desc in DEPARTMENTS_OPTIONS.items():
        score = 0.05
        if d in text_lower:
            score += 0.5
        keywords = desc.lower().replace(":", " ").replace(",", " ").split()
        for kw in keywords:
            if len(kw) > 4 and kw in text_lower:
                score += 0.15
        dept_scores[d] = score
        
    # Specific semantic boosts
    if any(k in text_lower for k in ["contrato", "processar", "rescisão", "jurídico", "lgpd", "processo"]):
        dept_scores["legal-risk"] = dept_scores.get("legal-risk", 0) + 1.2
    if any(k in text_lower for k in ["api", "caiu", "downtime", "código", "bug", "deploy"]):
        dept_scores["technology"] = dept_scores.get("technology", 0) + 0.8
    if any(k in text_lower for k in ["cliente", "reclamando", "suporte", "atendimento"]):
        dept_scores["customer-experience"] = dept_scores.get("customer-experience", 0) + 0.6
    if any(k in text_lower for k in ["pagamento", "transferência", "roi", "cfo", "banco", "reais"]):
        dept_scores["finance"] = dept_scores.get("finance", 0) + 1.1

    # Softmax normalization
    import math
    max_s = max(dept_scores.values())
    exp_scores = {k: math.exp(v - max_s) for k, v in dept_scores.items()}
    total_exp = sum(exp_scores.values())
    dept_probs = {k: round(v / total_exp, 4) for k, v in exp_scores.items()}
    best_dept = max(dept_probs.items(), key=lambda x: x[1])

    # 2. Autonomy Tier evaluation
    is_t3 = any(k in text_lower for k in ["processar", "rescisão", "demitir", "transferência", "500.000", "bancária", "processo judicial", "excluir banco"])
    is_t2 = any(k in text_lower for k in ["código", "deploy", "staging", "configuração", "criar contrato", "ajustar api"])
    
    if is_t3:
        tier_probs = {"tier_1": 0.02, "tier_2": 0.08, "tier_3": 0.90}
        tier_choice = "tier_3"
        veto_prob = 0.88
    elif is_t2:
        tier_probs = {"tier_1": 0.15, "tier_2": 0.78, "tier_3": 0.07}
        tier_choice = "tier_2"
        veto_prob = 0.12
    else:
        tier_probs = {"tier_1": 0.89, "tier_2": 0.09, "tier_3": 0.02}
        tier_choice = "tier_1"
        veto_prob = 0.04

    return {
        "engine": "Laya-ModernBERT / Jev-SystemOne (Simulated Benchmark)",
        "latency_ms": 28.4,
        "results": {
            "department": {
                "winner": best_dept[0],
                "confidence": best_dept[1],
                "probabilities": dict(sorted(dept_probs.items(), key=lambda x: -x[1])[:5])
            },
            "autonomy_tier": {
                "winner": tier_choice,
                "confidence": tier_probs[tier_choice],
                "probabilities": tier_probs
            },
            "compliance_veto": {
                "probability": veto_prob,
                "verdict": "VETO_REQUIRED" if veto_prob >= 0.70 else "WARNING" if veto_prob >= 0.30 else "CLEARED"
            }
        }
    }

def dispatch_decision(state_text: str) -> Dict[str, Any]:
    """Dispatches decision to Jev API (if key present) or local Laya engine"""
    t0 = time.perf_counter()
    api_key = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("JEV_API_KEY")
    
    payload = build_decision_payload(state_text)
    
    if api_key:
        try:
            raw_res = evaluate_via_jev_api(payload, api_key)
            elapsed = (time.perf_counter() - t0) * 1000
            return {
                "engine": "TypeSafe Jev (Cloud API)",
                "latency_ms": round(elapsed, 2),
                "results": raw_res
            }
        except Exception as e:
            print(f"[Warning] Jev API call failed ({e}). Falling back to local Laya engine.", file=sys.stderr)
            
    res = evaluate_heuristic_simulated(state_text)
    res["latency_ms"] = round((time.perf_counter() - t0) * 1000, 2)
    return res

def route_mesh_mission(state_text: str):
    """Full Agentic Mesh routing pipeline using System 1 decision engine"""
    print("="*70)
    print("🌐 JANDERSCIENCE SKILLS - SYSTEM 1 DECISION LAYER (JEV & LAYA)")
    print("="*70)
    print(f"Entrada da Missão:\n\"{state_text}\"\n")
    
    decision = dispatch_decision(state_text)
    res = decision["results"]
    
    print(f"Motor Ativo : {decision['engine']}")
    print(f"Latência    : {decision['latency_ms']} ms (Inclusa rede / inferência)")
    print("-" * 70)
    
    # Department
    dept = res["department"]
    print(f"🏛️ ROTEAMENTO DEPARTAMENTAL:")
    print(f"   Vencedor : {dept['winner'].upper()} (Confiança Calibrada: {dept['confidence']*100:.1f}%)")
    print(f"   Top Candidatos:")
    for d, prob in dept['probabilities'].items():
        print(f"     - {d:<22}: {prob*100:>5.1f}%")
        
    # Autonomy Tier
    tier = res["autonomy_tier"]
    tier_map = {
        "tier_1": ("TIER 1 (Autônomo / Leitura)", "\033[92m"),
        "tier_2": ("TIER 2 (Ação Interna Auditada)", "\033[93m"),
        "tier_3": ("TIER 3 (Alto Risco / Human-in-the-Loop)", "\033[91m")
    }
    tier_label, _ = tier_map.get(tier['winner'], (tier['winner'], ""))
    print(f"\n🛡️ MATRIZ DE CONFIANÇA (AGENTIC MESH):")
    print(f"   Classificação: {tier_label}")
    print(f"   Probabilidade: {tier['confidence']*100:.1f}%")
    
    # Compliance Veto
    veto = res["compliance_veto"]
    print(f"\n⚖️ GOVERNANÇA & PODER DE VETO (HARD VETO):")
    print(f"   Risco Regulatório/Legal: {veto['probability']*100:.1f}%")
    print(f"   Veredito               : {veto['verdict']}")
    
    if veto['verdict'] == "VETO_REQUIRED":
        print("\n🚨 [BLOQUEIO DE SEGURANÇA MESH ATIVADO]:")
        print("   Esta solicitação viola limites operacionais autônomos.")
        print("   Ação suspensa até deliberação do Conselho Executivo com parecer Jurídico!")
    elif tier['winner'] == "tier_3":
        print("\n⚠️ [HUMAN-IN-THE-LOOP OBRIGATÓRIO]:")
        print("   Rascunho será gerado pelo especialista, mas a execução final requer assinatura humana.")
    else:
        print("\n✅ [AUTORIZAÇÃO AUTOMÁTICA CONCEDIDA]:")
        print("   Encaminhando para execução imediata no microagente correspondente.")
    print("="*70 + "\n")

if __name__ == "__main__":
    test_query = (
        "Nosso cliente corporativo quer rescindir o contrato antes do prazo "
        "porque a API caiu duas vezes e está ameaçando nos processar por perdas e danos. O que fazer?"
    )
    if len(sys.argv) > 1:
        test_query = " ".join(sys.argv[1:])
    route_mesh_mission(test_query)
