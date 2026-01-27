/**
 * PIPELINE MONITOR - Colmena Autónoma
 * Monitorea specs y coordina handoff entre Claudes
 * 
 * Uso: node pipeline_monitor.js
 * Requiere: .env con GITHUB_TOKEN
 */

const https = require('https');
const net = require('net');

// Config
const CONFIG = {
  GITHUB_TOKEN: process.env.GITHUB_TOKEN,
  REPO_OWNER: 'Pvrolomx',
  REPO_NAME: 'canal',
  POLL_INTERVAL: 60000,      // 60 segundos
  STALE_THRESHOLD: 600000,   // 10 minutos
  CLAUDE_AGENTS: [
    { name: 'Claude_A', ip: '127.0.0.1', port: 9997 },  // Ajustar IPs/puertos
    { name: 'Claude_B', ip: '127.0.0.1', port: 9998 }
  ]
};

let currentAgentIndex = 0;

// Fetch desde GitHub API
async function fetchGitHub(path) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'api.github.com',
      path: `/repos/${CONFIG.REPO_OWNER}/${CONFIG.REPO_NAME}/contents/${path}`,
      headers: {
        'Authorization': `token ${CONFIG.GITHUB_TOKEN}`,
        'Accept': 'application/vnd.github.v3.raw',
        'User-Agent': 'Pipeline-Monitor'
      }
    };
    
    https.get(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (res.statusCode === 200) {
          try {
            resolve(JSON.parse(data));
          } catch {
            resolve(data);
          }
        } else if (res.statusCode === 404) {
          resolve(null);
        } else {
          reject(new Error(`GitHub API error: ${res.statusCode}`));
        }
      });
    }).on('error', reject);
  });
}

// Verificar si hay SPEC pendiente
async function checkForNewSpec() {
  try {
    const files = await fetchGitHub('pipeline');
    if (!files) return null;
    
    // Buscar archivos SPEC_*.md que no sean el template
    const specs = files.filter(f => 
      f.name.startsWith('SPEC_') && 
      f.name.endsWith('.md') && 
      f.name !== 'SPEC_TEMPLATE.md'
    );
    
    return specs.length > 0 ? specs[0].name : null;
  } catch (err) {
    console.error('[ERROR] checkForNewSpec:', err.message);
    return null;
  }
}

// Obtener progress actual
async function getProgress() {
  try {
    return await fetchGitHub('pipeline/progress.json');
  } catch (err) {
    console.error('[ERROR] getProgress:', err.message);
    return null;
  }
}

// Verificar si el proceso está estancado
function isStale(progress) {
  if (!progress || !progress.last_update) return false;
  const lastUpdate = new Date(progress.last_update).getTime();
  const now = Date.now();
  return (now - lastUpdate) > CONFIG.STALE_THRESHOLD;
}

// Trigger a Claude via TCP
function triggerClaude(action, context = {}) {
  const agent = CONFIG.CLAUDE_AGENTS[currentAgentIndex];
  console.log(`[TRIGGER] ${agent.name} - Action: ${action}`);
  
  const client = new net.Socket();
  client.connect(agent.port, agent.ip, () => {
    const message = JSON.stringify({ action, context, timestamp: new Date().toISOString() });
    client.write(message);
    client.end();
  });
  
  client.on('error', (err) => {
    console.error(`[ERROR] No se pudo conectar a ${agent.name}:`, err.message);
    // Intentar con el siguiente agente
    currentAgentIndex = (currentAgentIndex + 1) % CONFIG.CLAUDE_AGENTS.length;
  });
  
  client.on('data', (data) => {
    console.log(`[RESPONSE] ${agent.name}:`, data.toString());
  });
}

// Loop principal
async function monitorLoop() {
  console.log(`[${new Date().toISOString()}] Checking pipeline status...`);
  
  const progress = await getProgress();
  
  if (!progress) {
    console.log('[STATUS] No progress file found');
    return;
  }
  
  // Estado IDLE - buscar nuevo SPEC
  if (progress.status === 'IDLE') {
    const newSpec = await checkForNewSpec();
    if (newSpec) {
      console.log(`[NEW SPEC] Found: ${newSpec}`);
      triggerClaude('START', { spec: newSpec });
    } else {
      console.log('[STATUS] IDLE - No pending specs');
    }
    return;
  }
  
  // En progreso - verificar si está estancado
  if (progress.status === 'IN_PROGRESS') {
    if (isStale(progress)) {
      console.log(`[STALE] Process stalled. Last update: ${progress.last_update}`);
      console.log(`[HANDOFF] Switching to next agent...`);
      currentAgentIndex = (currentAgentIndex + 1) % CONFIG.CLAUDE_AGENTS.length;
      triggerClaude('CONTINUE', { 
        spec: progress.spec_name,
        lastStage: Object.keys(progress.stages).find(s => !progress.stages[s].completed)
      });
    } else {
      console.log(`[STATUS] IN_PROGRESS - Agent: ${progress.current_agent}`);
    }
    return;
  }
  
  // Completado
  if (progress.status === 'DEPLOYED' || progress.status === 'VERIFIED') {
    console.log(`[COMPLETE] ${progress.spec_name}`);
    console.log(`[URL] ${progress.deploy_url}`);
  }
}

// Iniciar monitor
console.log('='.repeat(50));
console.log('PIPELINE MONITOR - Colmena Autónoma');
console.log('='.repeat(50));
console.log(`Poll interval: ${CONFIG.POLL_INTERVAL / 1000}s`);
console.log(`Stale threshold: ${CONFIG.STALE_THRESHOLD / 1000}s`);
console.log(`Agents: ${CONFIG.CLAUDE_AGENTS.map(a => a.name).join(', ')}`);
console.log('='.repeat(50));

// Primera ejecución inmediata
monitorLoop();

// Loop continuo
setInterval(monitorLoop, CONFIG.POLL_INTERVAL);
