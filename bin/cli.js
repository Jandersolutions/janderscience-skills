#!/usr/bin/env node

/**
 * JanderScience Skills CLI & Installer
 * =====================================
 * Enterprise Agentic Mesh Workforce
 * 1,331 Specialized Skills Across 16 Corporate Departments
 * 
 * Developed by: Janderson B Abreu
 * Support Email: jba1719@gmail.com
 * Specification: agentskills.io v1 | Open Ontologies | Agentic Mesh
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');
const { spawnSync } = require('child_process');

// ANSI Color Helpers
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';
const DIM = '\x1b[2m';
const C_DIM = '\x1b[2m';

// Brand Truecolors: Mint (#5eead4) -> Teal (#2dd4bf) -> Sky Blue (#38bdf8)
const C_MINT = '\x1b[38;2;94;234;212m';
const C_TEAL = '\x1b[38;2;45;212;191m';
const C_SKY = '\x1b[38;2;56;189;248m';
const C_PLUM = '\x1b[38;2;168;85;247m';
const C_WHITE = '\x1b[38;2;255;255;255m';
const C_GRAY = '\x1b[38;2;156;163;175m';
const C_GREEN = '\x1b[38;2;34;197;94m';
const C_YELLOW = '\x1b[38;2;234;179;8m';
const C_RED = '\x1b[38;2;239;68;68m';

const BASE_DIR = path.resolve(__dirname, '..');
const REGISTRY_FILE = path.join(BASE_DIR, 'registry', 'mesh_registry.json');

function getBanner() {
  return `
${C_MINT}               /\\             ${C_WHITE}${BOLD}   ██╗ ██████╗       ██╗███████╗${RESET}
${C_MINT}              /  \\            ${C_WHITE}${BOLD}   ██║██╔════╝       ██║██╔════╝${RESET}
${C_TEAL}             / /\\ \\           ${C_WHITE}${BOLD}   ██║███████╗       ██║███████╗${RESET}
${C_TEAL}       /\\   / /  \\ \\   /\\     ${C_WHITE}${BOLD}   ██║╚════██║       ██║╚════██║${RESET}
${C_SKY}      /  \\ / /    \\ \\ /  \\    ${C_WHITE}${BOLD}   ██║███████║███████╗██║███████║${RESET}
${C_SKY}     / /\\ Y /      \\ Y /\\ \\   ${C_WHITE}${BOLD}   ╚═╝╚══════╝╚══════╝╚═╝╚══════╝${RESET}
${C_SKY}    | |  \\ V        V /  | |   ${C_MINT}${BOLD}J A N D E R S C I E N C E   S K I L L S${RESET}
${C_SKY}    | |   \\          /   | |   ${C_GRAY}Enterprise Agentic Mesh Workforce${RESET}
${C_TEAL}     \\ \\   \\   /\\   /   / /    ${C_SKY}1,331 Skills | 16 Corporate Departments${RESET}
${C_TEAL}      \\ \\   \\ /  \\ /   / /     ${C_GRAY}Spec: agentskills.io | Open Ontologies${RESET}
${C_MINT}       \\ \\   Y    Y   / /      
${C_MINT}        \\ \\          / /       ${C_WHITE}Developed by : ${C_MINT}Janderson B Abreu${RESET}
${C_MINT}         \\ \\________/ /        ${C_WHITE}Support Email: ${C_SKY}jba1719@gmail.com${RESET}
${C_MINT}          \\__________/         ${C_DIM}https://github.com/Jandersolutions/janderscience-skills${RESET}
`;
}

function loadRegistry() {
  if (!fs.existsSync(REGISTRY_FILE)) {
    console.error(`${C_RED}Error:${RESET} Registry file not found at ${REGISTRY_FILE}.`);
    console.error(`Run 'python tools/mesh_builder.py' first.`);
    process.exit(1);
  }
  return JSON.parse(fs.readFileSync(REGISTRY_FILE, 'utf8'));
}

// ---------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------

function showStats() {
  const data = loadRegistry();
  const meta = data.metadata;
  const skills = data.skills;
  const depts = data.departments;

  console.log(getBanner());
  console.log(`${C_TEAL}======================================================================${RESET}`);
  console.log(`  ${BOLD}ESTATÍSTICAS DO ECOSSISTEMA JANDERSCIENCE SKILLS${RESET}`);
  console.log(`${C_TEAL}======================================================================${RESET}`);
  console.log(`Total de Skills Mapeadas : ${BOLD}${C_MINT}${meta.total_skills}${RESET}`);
  console.log(`Departamentos Corporativos: ${BOLD}${C_MINT}${meta.total_departments}${RESET}`);
  console.log(`Padrão de Especificação  : ${C_SKY}${meta.spec}${RESET}`);
  console.log(`Autor e Mantenedor       : ${C_WHITE}Janderson B Abreu (${C_SKY}jba1719@gmail.com${C_WHITE})${RESET}`);
  console.log(`${C_TEAL}----------------------------------------------------------------------${RESET}`);

  const tiers = { 1: 0, 2: 0, 3: 0 };
  const deptCounts = {};
  for (const s of skills) {
    tiers[s.autonomy_tier || 1] = (tiers[s.autonomy_tier || 1] || 0) + 1;
    deptCounts[s.department] = (deptCounts[s.department] || 0) + 1;
  }

  console.log(`\n${BOLD}Níveis de Autonomia (Trust Matrix - Agentic Mesh):${RESET}`);
  console.log(`  ${C_GREEN}[Tier 1 - Autônomo / Leitura]${RESET}    : ${tiers[1]} skills`);
  console.log(`  ${C_YELLOW}[Tier 2 - Ação Interna Auditada]${RESET} : ${tiers[2]} skills`);
  console.log(`  ${C_RED}[Tier 3 - Aprovação Humana (HITL)]${RESET}: ${tiers[3]} skills`);

  console.log(`\n${BOLD}Divisão Departamental (16 Departamentos):${RESET}`);
  for (const [deptId, info] of Object.entries(depts)) {
    const count = deptCounts[deptId] || 0;
    console.log(`  ${C_SKY}${deptId.padEnd(22)}${RESET} (${info.name.padEnd(32)}): ${BOLD}${count.toString().padStart(4)}${RESET} skills`);
  }
  console.log(`${C_TEAL}======================================================================${RESET}\n`);
}

function searchSkills(query, limit = 10) {
  const data = loadRegistry();
  const q = query.toLowerCase();
  const results = [];

  for (const s of data.skills) {
    let score = 0;
    const name = s.name.toLowerCase();
    const desc = s.description.toLowerCase();
    const dept = s.department.toLowerCase();

    if (name.includes(q)) score += 10;
    if (desc.includes(q)) score += 5;
    if (dept.includes(q)) score += 3;

    for (const w of q.split(' ')) {
      if (name.includes(w)) score += 3;
      if (desc.includes(w)) score += 1;
    }

    if (score > 0) results.push({ score, skill: s });
  }

  results.sort((a, b) => b.score - a.score);

  console.log(getBanner());
  console.log(`${C_TEAL}Resultados da busca por: "${BOLD}${query}${RESET}${C_TEAL}" (${results.length} encontradas, exibindo ${Math.min(limit, results.length)}):${RESET}\n`);

  for (let i = 0; i < Math.min(limit, results.length); i++) {
    const s = results[i].skill;
    const tierTag = s.autonomy_tier === 1 ? `${C_GREEN}[T1:Read]${RESET}` : (s.autonomy_tier === 2 ? `${C_YELLOW}[T2:Audit]${RESET}` : `${C_RED}[T3:HITL]${RESET}`);
    console.log(`${(i + 1).toString().padStart(2)}. ${tierTag} ${BOLD}${s.name}${RESET} (${s.id})`);
    console.log(`    ${C_SKY}Departamento:${RESET} ${s.department} | ${C_GRAY}Idioma:${RESET} ${s.language}`);
    console.log(`    ${C_WHITE}Descrição:${RESET} ${s.description.substring(0, 150)}...`);
    console.log(`    ${DIM}Arquivo: ${s.path}${RESET}\n`);
  }
}

function doctor() {
  console.log(getBanner());
  console.log(`${C_TEAL}======================================================================${RESET}`);
  console.log(`  ${BOLD}DIAGNÓSTICO DE AMBIENTE - JANDERSCIENCE SKILLS DOCTOR${RESET}`);
  console.log(`${C_TEAL}======================================================================${RESET}`);

  const home = os.homedir();
  const envs = [
    { name: 'Claude Code', path: path.join(home, '.claude'), desc: 'Pasta de configuração do Claude CLI' },
    { name: 'Antigravity / Gemini CLI', path: path.join(home, '.gemini'), desc: 'Pasta do Antigravity CLI e Gemini' },
    { name: 'Cursor IDE', path: path.join(home, '.cursor'), desc: 'Configurações globais do Cursor' },
    { name: 'Local .claude', path: path.join(process.cwd(), '.claude'), desc: 'Configuração local do projeto Claude' },
    { name: 'Local skills/', path: path.join(process.cwd(), 'skills'), desc: 'Diretório local padrão de Agent Skills' }
  ];

  for (const env of envs) {
    const exists = fs.existsSync(env.path);
    const status = exists ? `${C_GREEN}✔ ENCONTRADO${RESET}` : `${C_GRAY}○ NÃO DETECTADO${RESET}`;
    console.log(`  ${status} ${BOLD}${env.name.padEnd(26)}${RESET} -> ${env.path}`);
  }

  console.log(`\n  ${C_GREEN}✔${RESET} ${BOLD}Node.js${RESET} : ${process.version}`);
  console.log(`  ${C_GREEN}✔${RESET} ${BOLD}Sistema Operacional${RESET} : ${os.type()} ${os.release()} (${os.arch()})`);
  console.log(`  ${C_GREEN}✔${RESET} ${BOLD}Suporte${RESET} : Janderson B Abreu <jba1719@gmail.com>`);
  console.log(`${C_TEAL}======================================================================${RESET}\n`);
}

// ---------------------------------------------------------------------
// Installer Engine
// ---------------------------------------------------------------------

function copyDirRecursive(src, dest) {
  if (!fs.existsSync(dest)) {
    fs.mkdirSync(dest, { recursive: true });
  }
  const entries = fs.readdirSync(src, { withFileTypes: true });
  for (const entry of entries) {
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      copyDirRecursive(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function installSkills(targetDir, selectedDept = null) {
  const data = loadRegistry();
  const skillsToInstall = selectedDept 
    ? data.skills.filter(s => s.department === selectedDept)
    : data.skills;

  console.log(`\n${C_TEAL}[1/3] Preparando instalação de ${BOLD}${skillsToInstall.length}${RESET}${C_TEAL} skills...${RESET}`);
  console.log(`      Destino: ${BOLD}${targetDir}${RESET}`);

  if (!fs.existsSync(targetDir)) {
    fs.mkdirSync(targetDir, { recursive: true });
  }

  let count = 0;
  for (const s of skillsToInstall) {
    const fullSrcPath = path.join(BASE_DIR, s.path);
    if (fs.existsSync(fullSrcPath)) {
      const skillFolderName = s.slug || s.name;
      const targetSkillDir = path.join(targetDir, skillFolderName);
      if (!fs.existsSync(targetSkillDir)) {
        fs.mkdirSync(targetSkillDir, { recursive: true });
      }
      fs.copyFileSync(fullSrcPath, path.join(targetSkillDir, 'SKILL.md'));
      
      // Copy references folder if present in parent
      const refSrc = path.join(path.dirname(fullSrcPath), 'references');
      if (fs.existsSync(refSrc)) {
        copyDirRecursive(refSrc, path.join(targetSkillDir, 'references'));
      }
      count++;
    }
  }

  console.log(`${C_TEAL}[2/3] Gravando manifesto janderscience.config.json...${RESET}`);
  const configContent = {
    project: "janderscience-skills",
    version: "1.0.0",
    developer: "Janderson B Abreu",
    support: "jba1719@gmail.com",
    installed_skills_count: count,
    installed_at: new Date().toISOString(),
    standard: "agentskills.io v1",
    ontology_source: "Open Ontologies (Oxigraph)",
    governance: "Agentic Mesh 7-Layer Trust Matrix"
  };
  fs.writeFileSync(path.join(targetDir, 'janderscience.config.json'), JSON.stringify(configContent, null, 2), 'utf8');

  console.log(`${C_TEAL}[3/3] Criando arquivo CLAUDE.md / AGENTS.md para integração imediata...${RESET}`);
  const agentsMdContent = `# JanderScience Skills: Enterprise Agentic Workforce
Total de Habilidades Instaladas: ${count}
Autor: Janderson B Abreu (jba1719@gmail.com)
Padrão: agentskills.io com Progressive Disclosure

Para usar qualquer habilidade, mencione a tarefa ou use o nome da skill.
`;
  fs.writeFileSync(path.join(targetDir, 'AGENTS.md'), agentsMdContent, 'utf8');

  console.log(`\n${C_GREEN}✔ SUCESSO! ${BOLD}${count} habilidades foram instaladas com sucesso!${RESET}`);
  console.log(`  Local: ${targetDir}`);
  console.log(`  Suporte: ${C_SKY}jba1719@gmail.com${RESET}\n`);
}

function interactiveInstaller() {
  console.log(getBanner());
  console.log(`${C_TEAL}======================================================================${RESET}`);
  console.log(`  ${BOLD}INSTALADOR OFICIAL JANDERSCIENCE SKILLS${RESET}`);
  console.log(`${C_TEAL}======================================================================${RESET}`);
  console.log(`Escolha onde deseja instalar as 1.331 habilidades de IA:\n`);

  const home = os.homedir();
  const options = [
    { label: 'Instalar em Claude Code (~/.claude/skills/)', path: path.join(home, '.claude', 'skills') },
    { label: 'Instalar em Antigravity / Gemini CLI (~/.gemini/skills/)', path: path.join(home, '.gemini', 'skills') },
    { label: 'Instalar no Projeto Atual (./skills/) para Cursor / VS Code', path: path.join(process.cwd(), 'skills') },
    { label: 'Instalar apenas 1 Departamento específico', path: 'dept_select' },
    { label: 'Rodar Diagnóstico dos Agentes Locais (Doctor)', path: 'doctor' },
    { label: 'Sair sem instalar', path: 'exit' }
  ];

  options.forEach((opt, idx) => {
    console.log(`  ${C_MINT}[${idx + 1}]${RESET} ${opt.label}`);
  });

  const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout
  });

  rl.question(`\n${BOLD}Digite o número da opção desejada (1-${options.length}): ${RESET}`, (ans) => {
    const choice = parseInt(ans.trim(), 10) - 1;
    rl.close();

    if (isNaN(choice) || choice < 0 || choice >= options.length) {
      console.log(`${C_RED}Opção inválida.${RESET}`);
      return;
    }

    const selected = options[choice];
    if (selected.path === 'exit') {
      console.log('Operação cancelada.');
      return;
    }

    if (selected.path === 'doctor') {
      doctor();
      return;
    }

    if (selected.path === 'dept_select') {
      const data = loadRegistry();
      const depts = Object.keys(data.departments);
      console.log(`\nDepartamentos disponíveis:\n`);
      depts.forEach((d, i) => console.log(`  ${C_SKY}[${i + 1}]${RESET} ${d}`));
      
      const rlDept = readline.createInterface({ input: process.stdin, output: process.stdout });
      rlDept.question(`\nEscolha o departamento (1-${depts.length}): `, (dAns) => {
        const dIdx = parseInt(dAns.trim(), 10) - 1;
        rlDept.close();
        if (dIdx >= 0 && dIdx < depts.length) {
          const chosenDept = depts[dIdx];
          const dest = path.join(process.cwd(), 'skills', chosenDept);
          installSkills(dest, chosenDept);
        } else {
          console.log(`${C_RED}Opção inválida.${RESET}`);
        }
      });
      return;
    }

    installSkills(selected.path);
  });
}

function routeMission(query) {
  const pyScript = path.join(BASE_DIR, 'tools', 'mesh_systemone.py');
  if (fs.existsSync(pyScript)) {
    const result = spawnSync('python', [pyScript, query], { stdio: 'inherit' });
    if (result.error) {
      console.error(`${C_RED}Erro ao executar motor Sistema 1:${RESET} ${result.error.message}`);
    }
  } else {
    console.error(`${C_RED}Erro:${RESET} Módulo tools/mesh_systemone.py não encontrado.`);
  }
}

// ---------------------------------------------------------------------
// CLI Argument Router
// ---------------------------------------------------------------------

function main() {
  const args = process.argv.slice(2);
  const cmd = args[0] ? args[0].toLowerCase() : '';

  if (cmd === '' || cmd === 'install' || cmd === 'i') {
    if (args.includes('--all')) {
      const dest = path.join(process.cwd(), 'skills');
      installSkills(dest);
    } else {
      interactiveInstaller();
    }
  } else if (cmd === 'stats' || cmd === 'info') {
    showStats();
  } else if (cmd === 'doctor' || cmd === 'check') {
    doctor();
  } else if (cmd === 'route' || cmd === 'decide') {
    const query = args.slice(1).join(' ');
    if (!query) {
      console.log('Uso: janderscience-skills route "<descrição da missão corporativa>"');
      return;
    }
    routeMission(query);
  } else if (cmd === 'search' || cmd === 'find') {
    const query = args.slice(1).join(' ');
    if (!query) {
      console.log('Uso: janderscience-skills search <termo>');
      return;
    }
    searchSkills(query);
  } else if (cmd === 'help' || cmd === '--help' || cmd === '-h') {
    console.log(getBanner());
    console.log(`Uso do CLI JanderScience Skills:
  npx janderscience-skills                  Abre o instalador interativo
  npx janderscience-skills install          Instalador interativo
  npx janderscience-skills install --all    Instala tudo no diretório ./skills
  npx janderscience-skills stats            Exibe as métricas de skills e departamentos
  npx janderscience-skills route "<missão>" Roteador Sistema 1 com Laya/Jev (Triagem, Tiers e Veto)
  npx janderscience-skills search <termo>   Busca habilidades por palavra-chave
  npx janderscience-skills doctor           Diagnostica ambientes locais instalados
  
Suporte: Janderson B Abreu <jba1719@gmail.com>
`);
  } else {
    // Default search
    searchSkills(args.join(' '));
  }
}

main();
