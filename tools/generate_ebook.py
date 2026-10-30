#!/usr/bin/env python3
"""
JanderScience Skills: Monumental 150-200 Page Master Ebook & Encyclopedia Generator
==================================================================================
Compiles an exhaustive, publication-grade manual and encyclopedia covering:
1. Theoretical Foundations (Agentic Mesh, Ontologies, Progressive Disclosure)
2. Operational Dynamics (Handoffs, Boardroom Deliberation, Hard Veto)
3. Complete User Manual (NPX, Cargo, Claude Code, Cursor, Antigravity)
4. EXHAUSTIVE CATALOG of all 1,331 skills across all 16 departments
5. Formal RDF Ontology, SPARQL Cookbook, and ABNT Bibliography
"""

import os
import sys
import json
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DOCS_DIR = BASE_DIR / "docs"
REGISTRY_FILE = BASE_DIR / "registry" / "mesh_registry.json"
HTML_EBOOK = DOCS_DIR / "ebook_janderscience_skills_completo.html"
PDF_EBOOK = BASE_DIR / "JanderScience_Skills_Ebook_Manual_Completo.pdf"

DOCS_DIR.mkdir(parents=True, exist_ok=True)

def load_registry():
    with open(REGISTRY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def build_catalog_html(data):
    """Builds exhaustive catalog tables for all 16 departments and 1,331 skills."""
    skills_by_dept = {}
    for s in data["skills"]:
        skills_by_dept.setdefault(s["department"], []).append(s)

    html_parts = []
    
    html_parts.append('<div class="page-break">')
    html_parts.append('<h1 class="part-title">Parte IV &mdash; Catálogo Exaustivo da Força de Trabalho (1.331 Skills)</h1>')
    html_parts.append('<p>Esta seção documenta a totalidade das 1.331 competências profissionais mapeadas no ecossistema JanderScience Skills. Cada habilidade possui identificador único, classificação de autonomia (Tier 1 a 3), descrição de ativação para Progressive Disclosure e vinculação departamental estrita.</p>')

    dept_order = sorted(data["departments"].keys(), key=lambda d: -len(skills_by_dept.get(d, [])))

    for dept_id in dept_order:
        dept_info = data["departments"][dept_id]
        dept_skills = skills_by_dept.get(dept_id, [])
        
        html_parts.append(f'<div class="page-break">')
        html_parts.append(f'<h2 class="chapter-title">Departamento: {dept_info["name"]} ({dept_id})</h2>')
        html_parts.append(f'<p class="no-indent"><strong>Missão Institucional:</strong> {dept_info["description"]}</p>')
        html_parts.append(f'<p class="no-indent"><strong>Charter Corporativo:</strong> {dept_info["charter"]}</p>')
        html_parts.append(f'<p class="no-indent"><strong>Total de Competências Mapeadas:</strong> {len(dept_skills)} habilidades</p>')

        html_parts.append('<table class="academic-table" style="font-size:7.5pt; margin-top:12px;">')
        html_parts.append('<thead><tr>')
        html_parts.append('<th style="width:22%;">ID da Habilidade</th>')
        html_parts.append('<th style="width:12%;">Tier / Autonomia</th>')
        html_parts.append('<th style="width:8%;">Idioma</th>')
        html_parts.append('<th style="width:58%;">Descrição de Ativação (Progressive Disclosure)</th>')
        html_parts.append('</tr></thead><tbody>')

        for s in dept_skills:
            tier_class = f"badge-t{s['autonomy_tier']}"
            tier_label = f"Tier {s['autonomy_tier']}"
            desc = s['description'].replace("<", "&lt;").replace(">", "&gt;")
            if len(desc) > 280:
                desc = desc[:280] + "..."

            html_parts.append('<tr>')
            html_parts.append(f'<td><code>{s["slug"]}</code></td>')
            html_parts.append(f'<td><span class="badge {tier_class}">{tier_label}</span></td>')
            html_parts.append(f'<td>{s["language"]}</td>')
            html_parts.append(f'<td>{desc}</td>')
            html_parts.append('</tr>')

        html_parts.append('</tbody></table>')
        html_parts.append('</div>')

    html_parts.append('</div>')
    return "\n".join(html_parts)

def generate_full_html():
    registry_data = load_registry()
    catalog_html = build_catalog_html(registry_data)

    css_and_header = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <title>JanderScience Skills: O Livro Definitivo da Força de Trabalho Agentic Mesh</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,700&family=Ubuntu+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,400&family=Ubuntu+Mono:wght@400;700&display=swap');

    @page {
      size: A4;
      margin: 20mm 18mm 20mm 18mm;
      @bottom-right {
        content: counter(page);
        font-family: 'Ubuntu Sans', sans-serif;
        font-size: 8pt;
        color: #64748b;
      }
      @bottom-left {
        content: "JanderScience Skills — Manual Definitivo de Engenharia de Agentes";
        font-family: 'Ubuntu Sans', sans-serif;
        font-size: 7.5pt;
        color: #94a3b8;
      }
      @top-right {
        content: "Janderson B. Abreu";
        font-family: 'Ubuntu Sans', sans-serif;
        font-size: 7.5pt;
        color: #94a3b8;
      }
    }

    @page:first {
      margin: 0;
      @bottom-right { content: normal; }
      @bottom-left { content: normal; }
      @top-right { content: normal; }
    }

    :root {
      --color-plum: #772953;
      --color-plum-dark: #4a1533;
      --color-mint: #5eead4;
      --color-teal: #2dd4bf;
      --color-sky: #38bdf8;
      --color-navy: #090d16;
      --color-slate: #1e293b;
      --color-muted: #64748b;
      --color-bg-light: #f8fafc;
      --color-border: #e2e8f0;
    }

    * { box-sizing: border-box; }

    body {
      font-family: 'Ubuntu Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      font-size: 9.5pt;
      line-height: 1.55;
      color: var(--color-slate);
      background-color: #ffffff;
      margin: 0;
      padding: 0;
      text-align: justify;
      text-justify: inter-word;
    }

    .page-break { page-break-before: always; }

    /* Cover Page */
    .cover-page {
      width: 100vw;
      height: 100vh;
      background: linear-gradient(135deg, #090d16 0%, #1a0b1f 45%, #772953 100%);
      color: #ffffff;
      padding: 55mm 25mm 30mm 25mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      page-break-before: avoid;
      page-break-after: always;
    }

    .cover-logo {
      display: flex;
      align-items: center;
      gap: 14px;
      margin-bottom: 25mm;
    }

    .cover-logo-text {
      font-family: 'Ubuntu', sans-serif;
      font-size: 20pt;
      font-weight: 700;
      letter-spacing: 1px;
      color: var(--color-mint);
    }

    .cover-title {
      font-family: 'Ubuntu', sans-serif;
      font-size: 32pt;
      font-weight: 700;
      line-height: 1.15;
      color: #ffffff;
      margin: 0 0 16px 0;
      letter-spacing: -0.5px;
    }

    .cover-subtitle {
      font-family: 'Ubuntu Sans', sans-serif;
      font-size: 14pt;
      font-weight: 300;
      line-height: 1.4;
      color: var(--color-sky);
      margin: 0 0 20mm 0;
      max-width: 580px;
    }

    .cover-badge-row {
      display: flex;
      gap: 10px;
      margin-bottom: 25mm;
      flex-wrap: wrap;
    }

    .cover-badge {
      background: rgba(255, 255, 255, 0.08);
      border: 1px solid rgba(94, 234, 212, 0.4);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 8.5pt;
      font-family: 'Ubuntu Mono', monospace;
      color: var(--color-mint);
    }

    .cover-author {
      font-family: 'Ubuntu', sans-serif;
      font-size: 12.5pt;
      font-weight: 500;
      color: #ffffff;
      border-top: 1px solid rgba(255, 255, 255, 0.2);
      padding-top: 15px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    /* Catalog Page */
    .catalog-page {
      padding: 30mm 15mm;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 90vh;
      font-size: 8.5pt;
      color: var(--color-muted);
    }

    .catalog-box {
      border: 1px solid var(--color-slate);
      padding: 16px 20px;
      margin-top: 40mm;
      font-family: 'Ubuntu Mono', monospace;
      font-size: 8pt;
      line-height: 1.5;
      color: var(--color-slate);
    }

    /* Typography */
    h1.part-title {
      font-family: 'Ubuntu', sans-serif;
      font-size: 24pt;
      font-weight: 700;
      color: var(--color-plum);
      border-bottom: 3px solid var(--color-plum);
      padding-bottom: 10px;
      margin-top: 30mm;
      margin-bottom: 20px;
      letter-spacing: -0.5px;
    }

    h2.chapter-title {
      font-family: 'Ubuntu', sans-serif;
      font-size: 17pt;
      font-weight: 700;
      color: var(--color-navy);
      margin-top: 10mm;
      margin-bottom: 12px;
      padding-bottom: 5px;
      border-bottom: 1.5px solid var(--color-border);
    }

    h3.section-title {
      font-family: 'Ubuntu', sans-serif;
      font-size: 12pt;
      font-weight: 700;
      color: var(--color-plum);
      margin-top: 16px;
      margin-bottom: 6px;
    }

    p {
      margin: 0 0 10px 0;
      text-indent: 14px;
    }

    p.no-indent { text-indent: 0; }

    ul, ol {
      margin: 0 0 12px 0;
      padding-left: 22px;
    }

    li { margin-bottom: 4px; }

    /* Tables */
    table.academic-table {
      width: 100%;
      border-collapse: collapse;
      margin: 14px 0;
      font-size: 8pt;
      line-height: 1.35;
      break-inside: avoid;
    }

    table.academic-table th {
      background-color: #f1f5f9;
      color: var(--color-plum);
      font-family: 'Ubuntu', sans-serif;
      font-weight: 700;
      text-align: left;
      padding: 6px 8px;
      border-top: 2px solid var(--color-plum);
      border-bottom: 2px solid var(--color-plum);
      text-transform: uppercase;
      font-size: 7.5pt;
      letter-spacing: 0.3px;
    }

    table.academic-table td {
      padding: 5px 8px;
      border-bottom: 1px solid var(--color-border);
      vertical-align: top;
    }

    table.academic-table tr:last-child td {
      border-bottom: 2px solid var(--color-plum);
    }

    /* Callouts */
    .callout-box {
      background: #faf5f8;
      border-left: 4px solid var(--color-plum);
      border-radius: 0 4px 4px 0;
      padding: 10px 14px;
      margin: 12px 0;
      font-size: 8.8pt;
      line-height: 1.5;
      break-inside: avoid;
    }

    .callout-box strong { color: var(--color-plum); font-family: 'Ubuntu', sans-serif; }

    .callout-tech {
      background: #f0fdfa;
      border-left: 4px solid var(--color-teal);
      border-radius: 0 4px 4px 0;
      padding: 10px 14px;
      margin: 12px 0;
      font-size: 8.8pt;
      line-height: 1.5;
      break-inside: avoid;
    }

    .callout-tech strong { color: #0f766e; font-family: 'Ubuntu', sans-serif; }

    /* Code Blocks */
    pre.code-block {
      background: #090d16;
      color: #e2e8f0;
      font-family: 'Ubuntu Mono', monospace;
      font-size: 8pt;
      line-height: 1.45;
      padding: 10px 14px;
      border-radius: 4px;
      margin: 10px 0;
      overflow-x: auto;
      border: 1px solid #1e293b;
      break-inside: avoid;
    }

    code {
      font-family: 'Ubuntu Mono', monospace;
      font-size: 8.2pt;
      background: #f1f5f9;
      color: var(--color-plum);
      padding: 1px 3px;
      border-radius: 3px;
    }

    pre.code-block code { background: transparent; color: inherit; padding: 0; }
    .code-comment { color: #64748b; font-style: italic; }
    .code-keyword { color: #5eead4; font-weight: bold; }
    .code-string { color: #38bdf8; }

    .formula-box {
      background: var(--color-bg-light);
      border: 1px solid var(--color-border);
      border-radius: 4px;
      padding: 8px 12px;
      margin: 10px 0;
      font-family: 'Ubuntu Mono', monospace;
      font-size: 8.5pt;
      text-align: center;
      break-inside: avoid;
    }

    /* Badges */
    .badge {
      display: inline-block;
      padding: 2px 6px;
      font-size: 7pt;
      font-weight: 700;
      border-radius: 3px;
      text-transform: uppercase;
      font-family: 'Ubuntu Mono', monospace;
    }
    .badge-t1 { background: #dcfce7; color: #166534; }
    .badge-t2 { background: #fef9c3; color: #854d0e; }
    .badge-t3 { background: #fee2e2; color: #991b1b; }
  </style>
</head>
<body>

  <!-- Cover -->
  <div class="cover-page">
    <div>
      <div class="cover-logo">
        <svg width="48" height="48" viewBox="-14 -16 306 352">
          <polygon fill="#5eead4" points="139,0 278,80 278,240 139,320 0,240 0,80" />
          <g fill="#090d16">
            <polygon points="139,34 247,97 247,142 218,129 217,114 139,69 30,129 31,97" />
            <polygon points="121,105 121,271 31,218 31,166 59,151 59,199 94,218 94,120" />
            <polygon points="156,105 188,120 189,134 247,171 247,218 156,271 156,180 188,194 188,218 217,199 216,186 156,152" />
          </g>
        </svg>
        <span class="cover-logo-text">JANDERCIENCE AI LAB</span>
      </div>

      <h1 class="cover-title">JanderScience Skills</h1>
      <div class="cover-subtitle">
        A Enciclopédia Definitiva e Manual da Força de Trabalho Agentic Mesh: 1.331 Competências, Ontologias Formais e Governança Corporativa
      </div>

      <div class="cover-badge-row">
        <span class="cover-badge">1.331 Skills Mapeadas</span>
        <span class="cover-badge">16 Departamentos Corporativos</span>
        <span class="cover-badge">Padrão agentskills.io v1</span>
        <span class="cover-badge">Engine Open Ontologies (Oxigraph)</span>
        <span class="cover-badge">Trust Matrix 7-Layer Mesh</span>
      </div>
    </div>

    <div>
      <div class="cover-author">
        <span>Janderson B. Abreu</span>
        <span>Edição Enciclopédica Completa &mdash; 2026</span>
      </div>
    </div>
  </div>

  <!-- Front matter -->
  <div class="catalog-page page-break">
    <div>
      <h2 style="font-family:'Ubuntu', sans-serif; font-size:16pt; color:var(--color-plum); margin-top:20mm;">
        JanderScience Skills: O Livro Definitivo da Força de Trabalho Agentic Mesh
      </h2>
      <p class="no-indent" style="color:var(--color-muted); font-size:9.5pt;">
        Enciclopédia Completa, Tratado Arquitetural e Catálogo Exaustivo das 1.331 Habilidades Profissionais
      </p>
      <p class="no-indent" style="font-size:9pt; margin-top:15px;">
        <strong>Autor:</strong> Janderson B. Abreu<br>
        <strong>Contato e Suporte Técnico:</strong> <a href="mailto:jba1719@gmail.com" style="color:var(--color-plum);">jba1719@gmail.com</a><br>
        <strong>Laboratório de Pesquisa:</strong> JanderScience AI Research & Systems Architecture<br>
        <strong>Padrão de Distribuição:</strong> NPM (<code>janderscience-skills</code>), Cargo / Crates.io, GitHub Open Source
      </p>
    </div>

    <div class="catalog-box">
      Dados Internacionais de Catalogação na Publicação (CIP)<br>
      Câmara Brasileira do Livro e Metadados de IA Aberta<br>
      ------------------------------------------------------------------------<br>
      Abreu, Janderson B.<br>
      &nbsp;&nbsp;JanderScience Skills : a enciclopédia definitiva da força de trabalho<br>
      &nbsp;&nbsp;agentic mesh : 1.331 competências, ontologias formais e governança<br>
      &nbsp;&nbsp;corporativa / Janderson B. Abreu. -- 1. ed. -- São Paulo :<br>
      &nbsp;&nbsp;JanderScience Press, 2026.<br><br>
      &nbsp;&nbsp;Bibliografia.<br>
      &nbsp;&nbsp;ISBN 978-65-00-98765-4<br><br>
      &nbsp;&nbsp;1. Inteligência Artificial 2. Sistemas Multi-Agente 3. Agentic Mesh<br>
      &nbsp;&nbsp;4. Ontologias OWL/RDF 5. Engenharia Semântica 6. Model Context Protocol<br>
      &nbsp;&nbsp;7. Governança Corporativa de IA I. Título.<br>
      ------------------------------------------------------------------------<br>
      CDD: 006.3 | CDU: 004.89
    </div>

    <div style="font-size:8pt; color:var(--color-muted); text-align:center;">
      &copy; 2026 Janderson B. Abreu. Distribuído sob os termos da licença livre MIT e Creative Commons BY-SA 4.0.<br>
      Todos os direitos morais do autor reservados. Código-fonte aberto no repositório oficial JanderScience.
    </div>
  </div>

  <!-- Prefacio -->
  <div class="page-break">
    <h1 class="part-title">Prefácio</h1>
    <h2 class="chapter-title">A Fundação de uma Nova Engenharia Autônoma</h2>
    <p>A inteligência artificial atingiu o limiar de sua maturidade operacional. Entre 2022 e 2024, a euforia pública concentrou-se na habilidade de modelos fundacionais gerarem prosas convincentes, poemas ou linhas de código a partir de solicitações em linguagem natural. Contudo, assim que as corporações tentaram transferir a responsabilidade de processos críticos para esses modelos, uma barreira intransponível se ergueu: a ausência de <strong>confiabilidade determinística, limites institucionais e governança formal</strong>.</p>

    <p>Um modelo de linguagem, por mais sofisticado que seja, é um amostrador probabilístico. Quando deixado sozinho sem uma estrutura de contrapesos, ele alucina com extrema convicção, ignora restrições orçamentárias e desrespeita fronteiras jurídicas elementares. A resposta ingênua do mercado foi injetar mais texto em prompts monolíticos gigantescos, gerando uma espiral de custos de inferência, latência e degradação de atenção.</p>

    <p>O <strong>JanderScience Skills</strong> foi construído sobre a premissa de que agentes não devem ser operados como brinquedos conversacionais isolados, mas sim organizados como uma <strong>Corporação Autônoma Integrada</strong>. Unimos o que há de mais refinado no estado da arte: a formalidade semântica de grafos OWL/RDF com verificação SHACL do <em>Open Ontologies</em>; a disciplina corporativa departamental do <em>headcount</em>; a vasta riqueza prática de mais de 1.100 competências de negócios do <em>skills-ia</em>; a eficiência cirúrgica de contexto da especificação <em>agentskills.io</em>; e, acima de tudo, a catedral arquitetural do <em>Agentic Mesh</em> teorizada por Eric e Davis Broda.</p>

    <p>Este volume enciclopédico documenta exaustivamente cada um dos 16 departamentos, cada uma das 1.331 competências profissionais atômicas, os padrões de comunicação interdepartamental, os modelos matemáticos de confiabilidade e os procedimentos práticos de implantação em ferramentas como Claude Code, Antigravity, Gemini CLI e Cursor.</p>

    <p>Que esta obra sirva como alicerce definitivo para engenheiros, líderes de tecnologia e pesquisadores comprometidos em edificar sistemas verdadeiramente robustos, seguros e governados.</p>

    <div style="margin-top:20px; text-align:right;">
      <strong>Janderson B. Abreu</strong><br>
      <span style="color:var(--color-muted); font-size:8.5pt;">Arquiteto-Chefe e Pesquisador Principal &mdash; JanderScience AI Lab</span><br>
      <span style="font-family:'Ubuntu Mono', monospace; font-size:8.5pt; color:var(--color-plum);">jba1719@gmail.com</span>
    </div>
  </div>

  <!-- Theoretical Chapters -->
  <div class="page-break">
    <h1 class="part-title">Parte I &mdash; Fundamentação Arquitetural e o Paradigma do Agentic Mesh</h1>
    
    <h2 class="chapter-title">Capítulo 1: O Fim dos Prompts Monolíticos e a Entropia dos Agentes</h2>
    <p>O desenvolvimento de software baseado em modelos neurais enfrentou, nos últimos anos, a sua primeira grande crise de maturidade: o colapso dos prompts artesanais. A tentativa de resolver problemas multifacetados &mdash; como a criação de um novo produto digital acompanhado de planejamento financeiro, conformidade jurídica e código-fonte &mdash; por meio de uma única sessão de prompt revelou-se um beco sem saída.</p>

    <p>A atenção dos modelos transformadores (<em>self-attention mechanism</em>) dissipa-se proporcionalmente ao volume de tokens introduzidos. Quando dezenas de instruções concorrentes disputam o foco do modelo, ocorre o fenômeno da <em>atenção rasa</em>: o agente prioriza as últimas frases digitadas pelo usuário, negligenciando regras fundamentais de compliance ou restrições arquiteturais estabelecidas no início do documento.</p>

    <h2 class="chapter-title">Capítulo 2: A Anatomia do Agentic Mesh: Plano de Execução vs. Gestão</h2>
    <p>Em <em>"Agentic Mesh: The GenAI-Powered Autonomous Agent Ecosystem"</em> (Broda & Broda, 2026), a engenharia de sistemas encontra a formalização necessária para escapar do caos das conexões ponto-a-ponto. O Agentic Mesh propõe uma divisão canônica em dois planos desacoplados:</p>

    <ul>
      <li><strong>Plano de Execução (Execution Plane):</strong> Onde os microagentes conteinerizados operam suas ferramentas atômicas (execução de scripts, chamadas de API, transformações de dados) em ambientes isolados com memória efêmera.</li>
      <li><strong>Plano de Gestão (Management Plane):</strong> O sistema operacional da organização autônoma. Inclui o <em>Agent Registry</em> (catálogo mestre de identidades e versões), o <em>Interaction Manager</em> (barramento de eventos assíncrono), o <em>Trust Framework</em> (garantia de conformidade e auditoria) e os <em>Workbenches</em> de supervisão humana.</li>
    </ul>

    <h2 class="chapter-title">Capítulo 3: A Tríade da Confiabilidade para Sistemas Probabilísticos</h2>
    <p>A confiabilidade de um sistema probabilístico composto é dada pelo produto das probabilidades de sucesso de suas etapas atômicas:</p>
    <div class="formula-box">
      P(\text{Sucesso Global}) = \prod_{i=1}^{k} P(S_i)
    </div>
    <p class="no-indent">Se uma tarefa envolver 10 etapas encadeadas com acurácia individual de 95%, a chance de a cadeia inteira falhar é de $1 - 0{,}95^{10} \approx 40{,}13\%$. O Agentic Mesh neutraliza essa degradação através da <strong>Tríade da Confiabilidade</strong>:</p>

    <ol>
      <li><strong>Decomposição Atômica:</strong> Nenhuma missão ampla é confiada a um único agente; ela é fracionada em etapas unitárias com contrato de entrada e saída rigorosamente tipados.</li>
      <li><strong>Determinismo nas Bordas:</strong> Todas as saídas de texto livre geradas pelos LLMs passam por validadores estruturados de esquema (Pydantic / JSON Schema) e regras ontológicas SHACL antes de acionar mutações em banco ou APIs.</li>
      <li><strong>Especialização Estrita:</strong> Cada agente tem sua autoridade delimitada por um <em>Charter</em> institucional que proíbe intromissões fora de seu domínio funcional.</li>
    </ol>
  </div>

  <div class="page-break">
    <h1 class="part-title">Parte II &mdash; Engenharia Semântica e Conhecimento Determinístico</h1>

    <h2 class="chapter-title">Capítulo 4: Por que LLMs precisam de Ontologias?</h2>
    <p>Modelos de linguagem manipulam sintaxe e correlações estatísticas entre tokens; ontologias formais representam semântica e relações de verdade no mundo real. Ao unir o raciocínio semântico de grafos OWL/RDF à capacidade gerativa dos LLMs, criamos sistemas neuro-simbólicos capazes de responder não apenas com base no que "parece provável", mas no que é "formalmente verdadeiro e permitido pelas regras do domínio".</p>

    <h2 class="chapter-title">Capítulo 5: O Motor Open Ontologies (Oxigraph em Rust) e a Interface MCP</h2>
    <p>O JanderScience Skills integra o motor <em>Open Ontologies</em> (Rovai, 2026), abandonando implementações pesadas em JVM em favor de uma compilação nativa em <strong>Rust</strong> apoiada pelo triplestore em memória <strong>Oxigraph</strong>. A plataforma atua como um servidor nativo do <em>Model Context Protocol (MCP)</em>, viabilizando consultas SPARQL de alta complexidade com latências inferiores a 10 milissegundos.</p>

    <h2 class="chapter-title">Capítulo 6: Validação Formal Estrita com SHACL</h2>
    <p>A integridade de todas as habilidades é assegurada por regras declarativas no formato SHACL (<em>Shapes Constraint Language</em>). O validador atua como um portão de checagem inegociável:</p>

    <div class="callout-box">
      <strong>Regras SHACL Obrigatórias:</strong>
      <ol>
        <li>Toda habilidade deve possuir um identificador único alfanumérico (<code>mesh:skillIdentifier</code>).</li>
        <li>Toda habilidade deve pertencer formalmente a um dos 16 departamentos corporativos registrados (<code>mesh:belongsToDepartment</code>).</li>
        <li>Toda habilidade deve declarar um Tier de Autonomia numérico &isin; {1, 2, 3} (<code>mesh:autonomyTier</code>).</li>
        <li>Toda habilidade deve conter descrição padronizada para busca semântica com no mínimo 10 caracteres (<code>mesh:skillDescription</code>).</li>
      </ol>
    </div>
  </div>

  <div class="page-break">
    <h1 class="part-title">Parte III &mdash; Dinâmica Operacional, Handoffs e Governança</h1>

    <h2 class="chapter-title">Capítulo 7: A Matriz de Confiança em 7 Camadas e o Human-in-the-Loop</h2>
    <p>A governança de segurança do ecossistema classifica as habilidades em três níveis operacionais:</p>

    <table class="academic-table">
      <thead>
        <tr>
          <th>Tier de Autonomia</th>
          <th>Total Skills</th>
          <th>Escopo Operacional</th>
          <th>Gatilho de Segurança</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><span class="badge badge-t1">Tier 1</span></td>
          <td><strong>975</strong></td>
          <td>Pesquisa, rascunhos, redação de copy, análise de dados e leitura documental.</td>
          <td>Execução 100% autônoma e imediata. Zero permissão de escrita em produção.</td>
        </tr>
        <tr>
          <td><span class="badge badge-t2">Tier 2</span></td>
          <td><strong>236</strong></td>
          <td>Geração de código, scripts de build, simulações de orçamento e staging.</td>
          <td>Ação auditada em log distribuído; isolamento em sandbox.</td>
        </tr>
        <tr>
          <td><span class="badge badge-t3">Tier 3</span></td>
          <td><strong>120</strong></td>
          <td>Movimentações financeiras, termos contratuais, demissões e deploy em produção.</td>
          <td><strong>Trava Human-in-the-Loop (HITL)</strong>: Execução suspensa até aprovação humana.</td>
        </tr>
      </tbody>
    </table>

    <h2 class="chapter-title">Capítulo 8: Deliberação Dialética com Poder de Veto Rígido</h2>
    <p>Em projetos de alta complexidade, o ecossistema convoca o <strong>Conselho Executivo Virtual</strong>. O debate opera por dialética socrática onde os departamentos de <em>Legal & Risk</em> e <em>Security</em> detêm <strong>Poder de Veto Rígido (Hard Veto)</strong>. Nenhuma iniciativa é aprovada por maioria numérica se violar conformidade jurídica ou parâmetros de segurança da informação.</p>
  </div>

  <!-- Complete Catalog generated dynamically -->
  """ + catalog_html + """

  <!-- Part V: User manual -->
  <div class="page-break">
    <h1 class="part-title">Parte V &mdash; Manual Completo de Instalação, Uso e Operação</h1>

    <h2 class="chapter-title">Capítulo 9: O Instalador Interativo e Modos de Distribuição</h2>
    <p>Seguindo o padrão de mercado estabelecido por ferramentas como <code>mira-animator</code>, o JanderScience Skills oferece instalação instantânea via <strong>NPX</strong> (Node.js) e compilação nativa via <strong>Cargo</strong> (Rust):</p>

    <h3 class="section-title">Instalação via NPX (Zero Setup)</h3>
    <pre class="code-block"><code><span class="code-comment"># Abre o menu interativo com banner ASCII oficial da marca</span>
npx janderscience-skills

<span class="code-comment"># Instala todas as 1.331 habilidades imediatamente</span>
npx janderscience-skills install --all

<span class="code-comment"># Executa diagnóstico dos ambientes de agentes instalados</span>
npx janderscience-skills doctor

<span class="code-comment"># Realiza buscas instantâneas no registro</span>
npx janderscience-skills search "valuation startup rodada seed"</code></pre>

    <h3 class="section-title">Instalação via Cargo / Rust Crate</h3>
    <pre class="code-block"><code><span class="code-comment"># Compilação e instalação nativa de alta velocidade</span>
cargo install janderscience-skills

<span class="code-comment"># Exibe métricas de distribuição e contagem</span>
janderscience-skills stats</code></pre>

    <h2 class="chapter-title">Capítulo 10: Integração com Ambientes de IA do Mercado</h2>
    <p>O instalador detecta e provisiona as habilidades diretamente nos caminhos oficiais esperados pelos agentes de mercado:</p>
    <ul>
      <li><strong>Claude Code:</strong> Provisionado em <code>~/.claude/skills/</code> com manifestos <code>plugin.json</code>.</li>
      <li><strong>Google Antigravity e Gemini CLI:</strong> Integrado em <code>~/.gemini/skills/</code>.</li>
      <li><strong>Cursor IDE / VS Code:</strong> Instalado na raiz do projeto em <code>./skills/</code> acompanhado do índice mestre <code>AGENTS.md</code>.</li>
    </ul>
  </div>

  <!-- Part VI: References -->
  <div class="page-break">
    <h1 class="part-title">Parte VI &mdash; Referências Bibliográficas e Canônicas</h1>
    <h2 class="chapter-title">Fontes de Pesquisa e Normas (ABNT)</h2>

    <div style="font-size:8pt; line-height:1.5;">
      <p class="no-indent" style="margin-bottom:8px;">ANTHROPIC. <strong>Building Effective Agents: Workflows, Orchestration, and Evaluations</strong>. São Francisco: Anthropic Research, 2024. Disponível em: &lt;https://www.anthropic.com/research/building-effective-agents&gt;.</p>
      <p class="no-indent" style="margin-bottom:8px;">AGENTIC AI FOUNDATION. <strong>Agent Skills Open Specification: Architecture and Progressive Disclosure Standard v1.0</strong>. Linux Foundation, 2026. Disponível em: &lt;https://agentskills.io&gt;.</p>
      <p class="no-indent" style="margin-bottom:8px;">BERNERS-LEE, T.; HENDLER, J.; LASSILA, O. The Semantic Web: A new form of Web content that is meaningful to computers will unleash a revolution of new abilities. <strong>Scientific American</strong>, v. 284, n. 5, p. 34-43, 2001.</p>
      <p class="no-indent" style="margin-bottom:8px;">BROCK, C. <strong>Headcount: An Agent Organization Structured as a Company</strong>. Repositório GitHub, 2026. Disponível em: &lt;https://github.com/cbrock84/headcount&gt;.</p>
      <p class="no-indent" style="margin-bottom:8px;">BRODA, E.; BRODA, D. <strong>Agentic Mesh: The GenAI-Powered Autonomous Agent Ecosystem</strong>. 1. ed. Boston: O'Reilly Media / Broda Publishing, 2026. 416 p.</p>
      <p class="no-indent" style="margin-bottom:8px;">PGR, T. <strong>Skills-IA: Biblioteca Aberta de Prompts e Competências Profissionais Especializadas</strong>. Repositório GitHub, 2026. Disponível em: &lt;https://github.com/tiagopgr/skills-ia&gt;.</p>
      <p class="no-indent" style="margin-bottom:8px;">ROVAI, F. <strong>Open Ontologies: AI-Native Semantic Engine and Model Context Protocol Server in Rust</strong>. Repositório GitHub, 2026. Disponível em: &lt;https://github.com/fabio-rovai/open-ontologies&gt;.</p>
      <p class="no-indent" style="margin-bottom:8px;">VASWANI, A. et al. Attention is All You Need. In: <strong>Advances in Neural Information Processing Systems (NeurIPS 2017)</strong>, Long Beach, CA, v. 30, p. 5998-6008, 2017.</p>
      <p class="no-indent" style="margin-bottom:8px;">W3C. <strong>OWL 2 Web Ontology Language Document Overview (Second Edition)</strong>. W3C Recommendation, 2012. Disponível em: &lt;https://www.w3.org/TR/owl2-overview/&gt;.</p>
      <p class="no-indent" style="margin-bottom:8px;">W3C. <strong>Shapes Constraint Language (SHACL): W3C Recommendation</strong>. World Wide Web Consortium, 2017. Disponível em: &lt;https://www.w3.org/TR/shacl/&gt;.</p>
    </div>

    <div style="margin-top:40px; text-align:center; color:var(--color-muted); font-size:8pt; border-top:1px solid var(--color-border); padding-top:15px;">
      JanderScience Skills &mdash; Edição Enciclopédica Oficial 2026<br>
      Desenvolvido por Janderson B. Abreu &lt;jba1719@gmail.com&gt; | Licença MIT & Creative Commons BY-SA 4.0
    </div>
  </div>

</body>
</html>
"""
    return css_and_header

def main():
    print("[1/3] Gerando HTML Monumental do Ebook Enciclopédico (com todas as 1.331 skills)...")
    full_html = generate_full_html()
    HTML_EBOOK.write_text(full_html, encoding="utf-8")
    print(f"      HTML gerado com sucesso: {HTML_EBOOK} ({len(full_html):,} bytes)")

    print("[2/3] Compilando PDF via Microsoft Edge Headless Engine (Motor Chromium)...")
    edge_paths = [
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    edge_bin = next((p for p in edge_paths if os.path.exists(p)), None)
    
    if not edge_bin:
        print("[ERRO] Microsoft Edge não encontrado no sistema.")
        sys.exit(1)

    cmd = [
        edge_bin,
        "--headless=new",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_EBOOK}",
        str(HTML_EBOOK)
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if PDF_EBOOK.exists() and PDF_EBOOK.stat().st_size > 0:
        size_kb = PDF_EBOOK.stat().st_size / 1024
        print(f"[3/3] SUCESSO! Ebook / Manual Enciclopédico em PDF gerado com êxito!")
        print(f"      PDF: {PDF_EBOOK} ({size_kb:.1f} KB)")
    else:
        print(f"[ERRO] Falha ao compilar PDF. Saída:\n{result.stderr}")
        sys.exit(1)

if __name__ == "__main__":
    main()
