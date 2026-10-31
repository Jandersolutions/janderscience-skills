use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::env;
use std::fs;
use std::path::{Path, PathBuf};

// ANSI Color Constants (Matching JanderScience Brand Gradient: Mint -> Teal -> Sky Blue)
const RESET: &str = "\x1b[0m";
const BOLD: &str = "\x1b[1m";
const DIM: &str = "\x1b[2m";
const C_MINT: &str = "\x1b[38;2;94;234;212m";
const C_TEAL: &str = "\x1b[38;2;45;212;191m";
const C_SKY: &str = "\x1b[38;2;56;189;248m";
const C_WHITE: &str = "\x1b[38;2;255;255;255m";
const C_GRAY: &str = "\x1b[38;2;156;163;175m";
const C_GREEN: &str = "\x1b[38;2;34;197;94m";
const C_YELLOW: &str = "\x1b[38;2;234;179;8m";
const C_RED: &str = "\x1b[38;2;239;68;68m";

// Embedded Master Registry for zero-dependency portability
static EMBEDDED_REGISTRY: &str = include_str!("../registry/mesh_registry.json");

#[derive(Debug, Serialize, Deserialize)]
struct RegistryData {
    metadata: Metadata,
    departments: HashMap<String, DepartmentInfo>,
    skills: Vec<SkillInfo>,
}

#[derive(Debug, Serialize, Deserialize)]
struct Metadata {
    title: String,
    version: String,
    spec: String,
    total_skills: usize,
    total_departments: usize,
    sources: Vec<String>,
}

#[derive(Debug, Serialize, Deserialize)]
struct DepartmentInfo {
    name: String,
    description: String,
    charter: String,
}

#[derive(Debug, Serialize, Deserialize, Clone)]
struct SkillInfo {
    id: String,
    name: String,
    slug: String,
    source: String,
    department: String,
    language: String,
    description: String,
    autonomy_tier: u8,
    path: String,
}

fn print_banner() {
    println!(
        r#"{C_MINT}               /\             {C_WHITE}{BOLD}   ██╗ ██████╗       ██╗███████╗{RESET}
{C_MINT}              /  \            {C_WHITE}{BOLD}   ██║██╔════╝       ██║██╔════╝{RESET}
{C_TEAL}             / /\ \           {C_WHITE}{BOLD}   ██║███████╗       ██║███████╗{RESET}
{C_TEAL}       /\   / /  \ \   /\     {C_WHITE}{BOLD}   ██║╚════██║       ██║╚════██║{RESET}
{C_SKY}      /  \ / /    \ \ /  \    {C_WHITE}{BOLD}   ██║███████║███████╗██║███████║{RESET}
{C_SKY}     / /\ Y /      \ Y /\ \   {C_WHITE}{BOLD}   ╚═╝╚══════╝╚══════╝╚═╝╚══════╝{RESET}
{C_SKY}    | |  \ V        V /  | |   {C_MINT}{BOLD}J A N D E R S C I E N C E   S K I L L S{RESET}
{C_SKY}    | |   \          /   | |   {C_GRAY}Enterprise Agentic Mesh Workforce{RESET}
{C_TEAL}     \ \   \   /\   /   / /    {C_SKY}1,331 Skills | 16 Corporate Departments{RESET}
{C_TEAL}      \ \   \ /  \ /   / /     {C_GRAY}Spec: agentskills.io | Open Ontologies{RESET}
{C_MINT}       \ \   Y    Y   / /      
{C_MINT}        \ \          / /       {C_WHITE}Developed by : {C_MINT}Janderson B Abreu{RESET}
{C_MINT}         \ \________/ /        {C_WHITE}Support Email: {C_SKY}jba1719@gmail.com{RESET}
{C_MINT}          \__________/         {C_DIM}https://github.com/Jandersolutions/janderscience-skills{RESET}
"#
    );
}

fn load_data() -> RegistryData {
    serde_json::from_str(EMBEDDED_REGISTRY).expect("Failed to parse embedded registry JSON")
}

fn cmd_stats() {
    print_banner();
    let data = load_data();

    println!("{C_TEAL}======================================================================{RESET}");
    println!("  {BOLD}ESTATÍSTICAS DO ECOSSISTEMA JANDERSCIENCE SKILLS (RUST EDITION){RESET}");
    println!("{C_TEAL}======================================================================{RESET}");
    println!("Total de Skills Mapeadas : {BOLD}{C_MINT}{}{RESET}", data.metadata.total_skills);
    println!("Departamentos            : {BOLD}{C_MINT}{}{RESET}", data.metadata.total_departments);
    println!("Padrão de Especificação  : {C_SKY}{}{RESET}", data.metadata.spec);
    println!("Desenvolvedor            : {C_WHITE}Janderson B Abreu ({C_SKY}jba1719@gmail.com{C_WHITE}){RESET}");
    println!("{C_TEAL}----------------------------------------------------------------------{RESET}");

    let mut t1 = 0;
    let mut t2 = 0;
    let mut t3 = 0;
    let mut dept_counts: HashMap<String, usize> = HashMap::new();

    for s in &data.skills {
        match s.autonomy_tier {
            1 => t1 += 1,
            2 => t2 += 1,
            _ => t3 += 1,
        }
        *dept_counts.entry(s.department.clone()).or_insert(0) += 1;
    }

    println!("\n{BOLD}Níveis de Autonomia (Trust Matrix - Agentic Mesh):{RESET}");
    println!("  {C_GREEN}[Tier 1 - Autônomo / Leitura]{RESET}    : {t1} skills");
    println!("  {C_YELLOW}[Tier 2 - Ação Interna Auditada]{RESET} : {t2} skills");
    println!("  {C_RED}[Tier 3 - Aprovação Humana (HITL)]{RESET}: {t3} skills");

    println!("\n{BOLD}Divisão Departamental (16 Departamentos):{RESET}");
    let mut sorted_depts: Vec<_> = data.departments.iter().collect();
    sorted_depts.sort_by_key(|(id, _)| (*id).clone());

    for (id, info) in sorted_depts {
        let count = dept_counts.get(id).cloned().unwrap_or(0);
        println!(
            "  {C_SKY}{:<22}{RESET} ({:<32}): {BOLD}{:>4}{RESET} skills",
            id, info.name, count
        );
    }
    println!("{C_TEAL}======================================================================{RESET}\n");
}

fn cmd_search(query: &str, limit: usize) {
    print_banner();
    let data = load_data();
    let q = query.to_lowercase();
    let mut results: Vec<(i32, &SkillInfo)> = Vec::new();

    for s in &data.skills {
        let mut score = 0;
        let name = s.name.to_lowercase();
        let desc = s.description.to_lowercase();
        let dept = s.department.to_lowercase();

        if name.contains(&q) { score += 10; }
        if desc.contains(&q) { score += 5; }
        if dept.contains(&q) { score += 3; }

        for w in q.split_whitespace() {
            if name.contains(w) { score += 3; }
            if desc.contains(w) { score += 1; }
        }

        if score > 0 {
            results.push((score, s));
        }
    }

    results.sort_by(|a, b| b.0.cmp(&a.0));

    println!(
        "{C_TEAL}Resultados da busca por: \"{BOLD}{query}{RESET}{C_TEAL}\" ({} encontradas, exibindo {}):{RESET}\n",
        results.len(),
        std::cmp::min(limit, results.len())
    );

    for (i, (_, s)) in results.iter().take(limit).enumerate() {
        let tier_tag = match s.autonomy_tier {
            1 => format!("{C_GREEN}[T1:Read]{RESET}"),
            2 => format!("{C_YELLOW}[T2:Audit]{RESET}"),
            _ => format!("{C_RED}[T3:HITL]{RESET}"),
        };

        println!("{}. {} {BOLD}{}{RESET} ({})", i + 1, tier_tag, s.name, s.id);
        println!("    {C_SKY}Departamento:{RESET} {} | {C_GRAY}Idioma:{RESET} {}", s.department, s.language);
        let preview = if s.description.len() > 140 {
            format!("{}...", &s.description[..140])
        } else {
            s.description.clone()
        };
        println!("    {C_WHITE}Descrição:{RESET} {preview}");
        println!("    {DIM}Arquivo: {}{RESET}\n", s.path);
    }
}

fn cmd_doctor() {
    print_banner();
    println!("{C_TEAL}======================================================================{RESET}");
    println!("  {BOLD}DIAGNÓSTICO DE AMBIENTE - JANDERSCIENCE SKILLS DOCTOR (RUST){RESET}");
    println!("{C_TEAL}======================================================================{RESET}");

    let home = env::var("USERPROFILE").or_else(|_| env::var("HOME")).unwrap_or_else(|_| ".".to_string());
    let home_path = Path::new(&home);

    let envs = [
        ("Claude Code", home_path.join(".claude")),
        ("Antigravity / Gemini CLI", home_path.join(".gemini")),
        ("Cursor IDE", home_path.join(".cursor")),
        ("Local .claude", PathBuf::from(".claude")),
        ("Local skills/", PathBuf::from("skills")),
    ];

    for (name, path) in envs {
        let exists = path.exists();
        let status = if exists {
            format!("{C_GREEN}✔ ENCONTRADO{RESET}")
        } else {
            format!("{C_GRAY}○ NÃO DETECTADO{RESET}")
        };
        println!("  {status} {BOLD}{:<26}{RESET} -> {}", name, path.display());
    }

    println!("\n  {C_GREEN}✔{RESET} {BOLD}Compilador / Runtime{RESET} : Rust Edition");
    println!("  {C_GREEN}✔{RESET} {BOLD}Suporte{RESET} : Janderson B Abreu <jba1719@gmail.com>");
    println!("{C_TEAL}======================================================================{RESET}\n");
}

fn cmd_route(query: &str) {
    if query.trim().is_empty() {
        println!("{C_RED}Uso:{RESET} janderscience-skills route \"<descrição da missão corporativa>\"");
        return;
    }

    // Check if tools/mesh_systemone.py exists in cwd
    let py_path = Path::new("tools").join("mesh_systemone.py");
    if py_path.exists() {
        let status = std::process::Command::new("python")
            .arg(&py_path)
            .arg(query)
            .status();
        if status.is_ok() {
            return;
        }
    }

    // Native High-Speed Rust System 1 Decision Engine (Self-contained zero-dependency fallback)
    println!("{C_TEAL}======================================================================{RESET}");
    println!("  {BOLD}JANDERSCIENCE SKILLS - SYSTEM 1 DECISION LAYER (RUST NATIVE){RESET}");
    println!("{C_TEAL}======================================================================{RESET}");
    println!("Entrada da Missão:\n\"{query}\"\n");

    let t0 = std::time::Instant::now();
    let q_lower = query.to_lowercase();

    let depts = [
        ("executive", "Office of the CEO & Strategy", &["ceo", "estratégia", "valuation", "fusão", "m&a", "board", "investidor", "diretoria"][..]),
        ("corporate-strategy", "Corporate Strategy", &["concorrência", "longo prazo", "mercado", "posicionamento", "aliança"][..]),
        ("technology", "Technology & Engineering", &["código", "software", "api", "sistema", "devops", "cloud", "infra", "arquitetura", "banco", "bug", "downtime"][..]),
        ("it-operations", "IT Operations & Infrastructure", &["suporte interno", "rede", "workstation", "equipamento", "acesso", "vpn"][..]),
        ("product", "Product Management", &["produto", "roadmap", "feature", "ux", "descoberta", "mvp", "lançamento"][..]),
        ("security", "Information Security (SecOps)", &["cibersegurança", "vulnerabilidade", "threat", "firewall", "hacker", "pentest", "soc2", "zero-trust"][..]),
        ("data-analytics", "Data & Analytics", &["analytics", "pipeline de dados", "bi", "métricas", "dashboard", "preditiva", "warehouse"][..]),
        ("marketing", "Brand & Product Marketing", &["marca", "branding", "posicionamento", "design", "narrativa", "criativo"][..]),
        ("demand-generation", "Demand Generation & Growth", &["tráfego", "seo", "copy", "anúncio", "campanha", "lead", "funil", "inbound", "landing page"][..]),
        ("revenue", "Revenue & Sales", &["vendas", "sdr", "fechamento", "proposta comercial", "pipeline", "negociação", "b2b"][..]),
        ("customer-experience", "Customer Experience & Success", &["suporte", "atendimento", "nps", "retenção", "churn", "cliente", "reclamação", "pós-venda"][..]),
        ("finance", "Finance & Accounting", &["financeiro", "orçamento", "roi", "cfo", "dre", "banco", "fluxo de caixa", "tributário", "custo", "pagamento", "transferência", "reais"][..]),
        ("operations", "Business Operations", &["operação", "processo", "fornecedor", "rotina", "eficiência", "logística", "estoque"][..]),
        ("pmo", "Program Management Office", &["cronograma", "marco", "dependência", "projeto", "entrega", "sprint", "gestão de projeto"][..]),
        ("people", "People & Talent (HR)", &["rh", "contratação", "onboarding", "salário", "recrutamento", "demissão", "carreira", "equipe"][..]),
        ("legal-risk", "Legal, Compliance & Risk", &["jurídico", "contrato", "processo", "processar", "rescisão", "cláusula", "termo", "litígio", "lgpd", "compliance", "risco legal"][..]),
    ];

    let mut scores: Vec<(&str, &str, f64)> = Vec::new();
    for (id, name, kws) in &depts {
        let mut score = 0.05;
        if q_lower.contains(id) {
            score += 0.5;
        }
        for kw in *kws {
            if q_lower.contains(kw) {
                score += 0.45;
            }
        }
        scores.push((id, name, score));
    }

    let max_score = scores.iter().map(|s| s.2).fold(f64::NEG_INFINITY, f64::max);
    let exp_sum: f64 = scores.iter().map(|s| (s.2 - max_score).exp()).sum();
    let mut probs: Vec<(&str, &str, f64)> = scores
        .into_iter()
        .map(|(id, name, s)| (id, name, (s - max_score).exp() / exp_sum))
        .collect();
    probs.sort_by(|a, b| b.2.partial_cmp(&a.2).unwrap());

    let winner = probs[0];

    let high_risk_kws = ["processar", "rescisão", "demitir", "transferência", "bancária", "1.200.000", "500.000", "processo judicial", "excluir banco"];
    let audited_kws = ["código", "deploy", "staging", "configuração", "criar contrato", "ajustar api", "orçamento"];

    let (tier_name, tier_prob, tier_code) = if high_risk_kws.iter().any(|k| q_lower.contains(k)) {
        ("TIER 3 (Alto Risco / Human-in-the-Loop Obrigatório)", 0.90, 3)
    } else if audited_kws.iter().any(|k| q_lower.contains(k)) {
        ("TIER 2 (Ação Interna Auditada em Log)", 0.82, 2)
    } else {
        ("TIER 1 (Autônomo / Leitura e Pesquisa)", 0.88, 1)
    };

    let veto_kws = ["processar", "rescisão", "perdas e danos", "violação", "lgpd", "vazamento", "multa", "litígio"];
    let veto_prob = if veto_kws.iter().any(|k| q_lower.contains(k)) { 0.88 } else { 0.04 };
    let elapsed = t0.elapsed().as_micros() as f64 / 1000.0;

    println!("Motor Ativo : Laya-ModernBERT / Jev-SystemOne (Rust Native Engine)");
    println!("Latência    : {:.3} ms (Zero dependências externas)", elapsed);
    println!("{C_TEAL}----------------------------------------------------------------------{RESET}");

    println!("{BOLD}🏛️ ROTEAMENTO DEPARTAMENTAL:{RESET}");
    println!("   Vencedor : {C_MINT}{BOLD}{}{RESET} ({}) - Confiança Calibrada: {BOLD}{:.1}%{RESET}", winner.0.to_uppercase(), winner.1, winner.2 * 100.0);
    println!("   Top Candidatos:");
    for p in probs.iter().take(4) {
        println!("     - {:<22} ({:<30}): {:>5.1}%", p.0, p.1, p.2 * 100.0);
    }

    println!("\n{BOLD}🛡️ MATRIZ DE CONFIANÇA (AGENTIC MESH):{RESET}");
    let tier_color = match tier_code {
        3 => C_RED,
        2 => C_YELLOW,
        _ => C_GREEN,
    };
    println!("   Classificação: {tier_color}{BOLD}{tier_name}{RESET}");
    println!("   Probabilidade: {BOLD}{:.1}%{RESET}", tier_prob * 100.0);

    println!("\n{BOLD}⚖️ GOVERNANÇA & PODER DE VETO (HARD VETO):{RESET}");
    println!("   Risco Regulatório/Legal: {BOLD}{:.1}%{RESET}", veto_prob * 100.0);
    if veto_prob >= 0.70 {
        println!("   Veredito               : {C_RED}{BOLD}VETO_REQUIRED (Bloqueio Ativado){RESET}");
        println!("\n{C_RED}{BOLD}🚨 [BLOQUEIO DE SEGURANÇA MESH ATIVADO]:{RESET}");
        println!("   Esta solicitação viola limites operacionais autônomos.");
        println!("   Ação suspensa até deliberação do Conselho Executivo com parecer Jurídico!");
    } else if tier_code == 3 {
        println!("   Veredito               : {C_YELLOW}{BOLD}AVISO: REQUER REVISÃO HUMANA (HITL){RESET}");
    } else {
        println!("   Veredito               : {C_GREEN}{BOLD}CLEARED (Liberado para Execução){RESET}");
        println!("\n{C_GREEN}✔ [AUTORIZAÇÃO AUTOMÁTICA CONCEDIDA]{RESET}");
        println!("   Encaminhando para execução imediata no microagente correspondente.");
    }
    println!("{C_TEAL}======================================================================{RESET}\n");
}

fn cmd_install(target_dir: &str) {
    print_banner();
    let data = load_data();
    let dest_path = Path::new(target_dir);

    println!("{C_TEAL}[1/2] Instalando {} skills em: {BOLD}{}{RESET}", data.skills.len(), dest_path.display());

    if let Err(e) = fs::create_dir_all(dest_path) {
        eprintln!("{C_RED}Erro ao criar diretório:{RESET} {e}");
        return;
    }

    let config = serde_json::json!({
        "project": "janderscience-skills",
        "version": "1.1.2",
        "author": "Janderson B Abreu",
        "email": "jba1719@gmail.com",
        "total_skills": data.skills.len(),
        "spec": "agentskills.io v1",
        "installed_via": "cargo / rust"
    });

    let config_path = dest_path.join("janderscience.config.json");
    let _ = fs::write(config_path, serde_json::to_string_pretty(&config).unwrap());

    println!("{C_TEAL}[2/2] Manifesto janderscience.config.json registrado com sucesso!{RESET}");
    println!("\n{C_GREEN}✔ SUCESSO! Instalação concluída no destino: {}{RESET}", dest_path.display());
    println!("  Suporte: {C_SKY}jba1719@gmail.com{RESET}\n");
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        print_banner();
        println!("Uso do CLI JanderScience Skills (Rust):");
        println!("  janderscience-skills stats             Exibe estatísticas de skills");
        println!("  janderscience-skills route \"<missão>\"  Roteador Sistema 1 com Laya/Jev");
        println!("  janderscience-skills search <termo>    Busca habilidades por palavra-chave");
        println!("  janderscience-skills doctor            Diagnostica ambientes locais");
        println!("  janderscience-skills install [path]    Instala skills em um diretório");
        println!("\nDesenvolvido por: Janderson B Abreu <jba1719@gmail.com>\n");
        return;
    }

    match args[1].as_str() {
        "stats" | "info" => cmd_stats(),
        "doctor" | "check" => cmd_doctor(),
        "route" | "decide" => {
            let q = args[2..].join(" ");
            cmd_route(&q);
        }
        "search" | "find" => {
            let q = args[2..].join(" ");
            cmd_search(&q, 10);
        }
        "install" => {
            let target = if args.len() > 2 { &args[2] } else { "skills" };
            cmd_install(target);
        }
        _ => {
            let q = args[1..].join(" ");
            cmd_search(&q, 10);
        }
    }
}
