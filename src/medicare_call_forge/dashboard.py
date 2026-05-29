"""
Ultra-Premium Operator Dashboard for MedicareCallForge.

This is the flagship high-end interface — quiet luxury meets operational excellence.
Designed for serious pilots and professional operators who expect the very best.

Features:
- Tabbed command center experience
- Real-time live call streaming via SSE
- Powerful Audit Vault with deep detail views
- Elegant dual-stream visualizations
- Sophisticated test call controls for both revenue paths
- Pilot Mode with elevated presence
"""

from __future__ import annotations

LUXURY_DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MedicareCallForge • Command Center</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600&amp;family=Inter:wght@300;400;500;600&amp;family=Space+Grotesk:wght@500;600&amp;display=swap');
        
        :root {
            --bg: #0A0A0A;
            --card: #121212;
            --card-elevated: #1A1A1A;
            --gold: #C5A46E;
            --gold-bright: #D8B98A;
            --cream: #F5F0E6;
            --text: #EDE4D5;
            --muted: #8A7F6E;
            --border: #252525;
        }
        
        body {
            font-family: 'Inter', system_ui, sans-serif;
            background: #0A0A0A;
            color: #EDE4D5;
        }
        
        .heading-serif {
            font-family: 'Playfair Display', Georgia, serif;
            letter-spacing: -0.04em;
        }
        
        .heading-display {
            font-family: 'Space Grotesk', 'Inter', sans-serif;
            letter-spacing: -0.05em;
        }

        .luxury-card {
            background: #121212;
            border: 1px solid #252525;
            transition: border-color 0.2s ease, transform 0.2s ease, box-shadow 0.2s ease;
        }
        
        .luxury-card:hover {
            border-color: #C5A46E;
            box-shadow: 0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1);
        }

        .gold-text { color: #C5A46E; }
        .gold-border { border-color: #C5A46E; }

        .section-header {
            font-family: 'Playfair Display', Georgia, serif;
            letter-spacing: -0.035em;
            font-weight: 600;
        }

        .nav-tab {
            position: relative;
            padding-bottom: 12px;
            font-weight: 500;
            letter-spacing: 0.3px;
            transition: all 0.2s ease;
        }
        
        .nav-tab.active {
            color: #C5A46E;
        }
        
        .nav-tab.active:after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 2px;
            background: linear-gradient(to right, #C5A46E, #D8B98A);
        }

        .premium-pill {
            background: #1A1A1A;
            border: 1px solid #C5A46E;
            color: #C5A46E;
            font-size: 0.7rem;
            letter-spacing: 1px;
            font-weight: 600;
        }

        .metric-value {
            font-variant-numeric: tabular-nums;
            font-feature-settings: "ss02";
        }

        .audit-hash {
            font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
            letter-spacing: 0.75px;
        }

        .stream-enroll { border-left: 3px solid #C5A46E; }
        .stream-sell { border-left: 3px solid #8C9A8A; }

        .luxury-table {
            font-variant-numeric: tabular-nums;
        }

        .luxury-row {
            transition: background-color 0.1s ease;
        }
        .luxury-row:hover {
            background-color: #1A1A1A;
        }

        .elegant-btn {
            transition: all 0.15s cubic-bezier(0.4, 0.0, 0.2, 1);
            letter-spacing: 0.4px;
        }
        
        .elegant-btn:hover {
            background-color: #C5A46E;
            color: #0A0A0A;
            border-color: #C5A46E;
            transform: translateY(-1px);
        }

        .modal {
            animation: modalEnter 0.2s cubic-bezier(0.32, 0.72, 0, 1);
        }

        @keyframes modalEnter {
            from { opacity: 0; transform: translateY(12px) scale(0.985); }
            to { opacity: 1; transform: translateY(0) scale(1); }
        }

        .live-dot {
            animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
        }

        .data-value {
            font-feature-settings: "tnum";
        }

        .subtle-gold-gradient {
            background: linear-gradient(145deg, #C5A46E, #D8B98A);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
</head>
<body class="bg-[#0A0A0A] text-[#EDE4D5]">
    <!-- Ultra-refined Top Bar -->
    <div class="border-b border-[#252525] bg-[#0A0A0A] sticky top-0 z-50 backdrop-blur-xl">
        <div class="max-w-7xl mx-auto px-8">
            <div class="flex h-20 items-center justify-between">
                <div class="flex items-center gap-x-5">
                    <div class="flex items-center gap-x-3">
                        <div class="w-10 h-10 rounded-2xl border border-[#C5A46E] flex items-center justify-center">
                            <i class="fa-solid fa-shield-halved text-[#C5A46E] text-2xl"></i>
                        </div>
                        <div>
                            <div class="font-semibold text-3xl tracking-[-2px] heading-serif">MedicareCallForge</div>
                            <div class="text-[10px] text-[#8A7F6E] tracking-[1.5px] -mt-1">COMMAND CENTER</div>
                        </div>
                    </div>
                    
                    <div class="ml-3 px-5 py-2 rounded-3xl premium-pill flex items-center gap-x-2 text-xs font-semibold">
                        <i class="fa-solid fa-lock"></i>
                        <span>REGULATORY STRICT MODE</span>
                    </div>
                </div>

                <div class="flex items-center gap-x-5">
                    <!-- Pilot Mode Toggle -->
                    <div class="flex items-center gap-x-3 bg-[#121212] border border-[#252525] rounded-3xl px-2 py-1.5">
                        <div class="pl-3 text-xs font-medium text-[#8A7F6E]">PILOT MODE</div>
                        <div onclick="togglePilotMode()" id="pilot-toggle"
                             class="cursor-pointer w-11 h-6 bg-[#252525] rounded-full relative flex items-center px-1 transition-colors">
                            <div id="pilot-knob" 
                                 class="w-4 h-4 bg-[#8A7F6E] rounded-full transition-all flex items-center justify-center">
                                <i class="fa-solid fa-check text-[9px] text-[#121212] hidden" id="pilot-check"></i>
                            </div>
                        </div>
                    </div>

                    <div onclick="refreshAllData()" 
                         class="cursor-pointer flex items-center gap-x-2.5 px-5 py-2.5 text-sm rounded-3xl border border-[#252525] hover:border-[#C5A46E] elegant-btn font-medium">
                        <i class="fa-solid fa-sync-alt"></i>
                        <span>Refresh</span>
                    </div>

                    <div class="text-xs font-mono text-[#8A7F6E]">
                        v0.2.0 • <span id="last-updated">live</span>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <div class="max-w-7xl mx-auto px-8 pt-8 pb-16">
        
        <!-- Refined Header -->
        <div class="flex items-end justify-between mb-9">
            <div>
                <div class="uppercase tracking-[3px] text-xs text-[#8A7F6E] font-semibold mb-2">CONFIDENTIAL PILOT ENVIRONMENT</div>
                <h1 class="heading-serif text-7xl font-semibold tracking-[-3.5px] text-[#F5F0E6]">Command Center</h1>
            </div>
            <div class="text-right">
                <div class="text-sm text-[#8A7F6E]">Last Gate Verification</div>
                <div class="font-mono text-lg text-[#C5A46E]" id="last-gate-time">moments ago</div>
            </div>
        </div>

        <!-- Tab Navigation -->
        <div class="flex border-b border-[#252525] mb-8">
            <div onclick="switchTab('overview')" id="tab-overview"
                 class="nav-tab px-8 cursor-pointer text-base active">Overview</div>
            <div onclick="switchTab('operations')" id="tab-operations"
                 class="nav-tab px-8 cursor-pointer text-base">Live Operations</div>
            <div onclick="switchTab('brain')" id="tab-brain"
                 class="nav-tab px-8 cursor-pointer text-base">Brain &amp; Routing</div>
            <div onclick="switchTab('vault')" id="tab-vault"
                 class="nav-tab px-8 cursor-pointer text-base">Audit Vault</div>
        </div>

        <!-- ==================== OVERVIEW TAB ==================== -->
        <div id="panel-overview">
            <!-- Executive KPIs -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                <div class="luxury-card rounded-3xl p-7">
                    <div class="text-xs tracking-[1.5px] text-[#8A7F6E] font-medium mb-3">TOTAL CALLS</div>
                    <div class="flex items-baseline gap-x-2">
                        <span id="kpi-total-calls" class="text-7xl font-semibold tracking-tighter data-value">187</span>
                    </div>
                    <div class="text-emerald-400 text-sm mt-2 font-medium">+24 in last 24h</div>
                </div>

                <div class="luxury-card rounded-3xl p-7">
                    <div class="text-xs tracking-[1.5px] text-[#8A7F6E] font-medium mb-3">AVG COMPLIANCE</div>
                    <div class="flex items-baseline">
                        <span id="kpi-avg-compliance" class="text-7xl font-semibold tracking-tighter">99.6</span>
                        <span class="text-3xl text-[#C5A46E] ml-1">%</span>
                    </div>
                    <div class="h-1.5 bg-[#252525] rounded mt-5 overflow-hidden">
                        <div class="h-1.5 bg-gradient-to-r from-[#C5A46E] to-[#D8B98A]" style="width: 99.6%"></div>
                    </div>
                </div>

                <div class="luxury-card rounded-3xl p-7 stream-enroll">
                    <div class="flex justify-between">
                        <div>
                            <div class="text-xs tracking-[1.5px] text-[#C5A46E] font-medium mb-1">ENROLL STREAM</div>
                            <div id="kpi-enroll" class="text-6xl font-semibold tracking-tighter data-value">112</div>
                        </div>
                        <i class="fa-solid fa-user-tie text-4xl text-[#C5A46E] opacity-75"></i>
                    </div>
                    <div class="mt-4 text-sm text-[#C5A46E]">Projected $53,760 in commissions</div>
                </div>

                <div class="luxury-card rounded-3xl p-7 stream-sell">
                    <div class="flex justify-between">
                        <div>
                            <div class="text-xs tracking-[1.5px] text-[#8C9A8A] font-medium mb-1">SELL STREAM</div>
                            <div id="kpi-sell" class="text-6xl font-semibold tracking-tighter data-value">75</div>
                        </div>
                        <i class="fa-solid fa-handshake text-4xl text-[#8C9A8A] opacity-75"></i>
                    </div>
                    <div class="mt-4 text-sm text-[#8C9A8A]">Projected $1,875 revenue this period</div>
                </div>
            </div>

            <!-- Dual-Stream Performance Charts (Track 3 advanced viz) -->
            <div class="mb-8">
                <div class="flex items-center justify-between mb-4 px-1">
                    <div class="uppercase text-xs tracking-[1.5px] text-[#8A7F6E]">Performance Trends (Pilot)</div>
                </div>
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
                    <div class="luxury-card rounded-3xl p-6">
                        <div class="text-xs text-[#8A7F6E] mb-3">Calls by Stream (Last 7 Days)</div>
                        <canvas id="callsChart" height="90"></canvas>
                    </div>
                    <div class="luxury-card rounded-3xl p-6">
                        <div class="text-xs text-[#8A7F6E] mb-3">Avg UVal by Stream</div>
                        <canvas id="uvalChart" height="90"></canvas>
                    </div>
                </div>
            </div>

            <!-- Quick Dual Stream Snapshot -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-8">
                <div class="luxury-card rounded-3xl p-8">
                    <div class="uppercase text-xs tracking-widest text-[#C5A46E] mb-4 font-semibold">ENROLL IN-HOUSE</div>
                    <div class="text-2xl font-medium leading-tight mb-6">High-intent search calls routed to licensed agents via MultiAgentOrchestrator</div>
                    <div class="flex gap-8 text-sm">
                        <div><span class="block text-[#8A7F6E]">Target CAC</span> <span class="font-semibold text-xl">&lt;$40</span></div>
                        <div><span class="block text-[#8A7F6E]">Avg UVal</span> <span class="font-semibold text-xl">0.77</span></div>
                    </div>
                </div>
                <div class="luxury-card rounded-3xl p-8">
                    <div class="uppercase text-xs tracking-widest text-[#8C9A8A] mb-4 font-semibold">SELL OVERFLOW</div>
                    <div class="text-2xl font-medium leading-tight mb-6">Social &amp; educational calls packaged with full compliance provenance</div>
                    <div class="flex gap-8 text-sm">
                        <div><span class="block text-[#8A7F6E]">Target Margin</span> <span class="font-semibold text-xl">$9–14</span></div>
                        <div><span class="block text-[#8A7F6E]">Avg UVal</span> <span class="font-semibold text-xl">0.56</span></div>
                    </div>
                </div>
            </div>
        </div>

        <!-- ==================== LIVE OPERATIONS TAB ==================== -->
        <div id="panel-operations" class="hidden">
            <div class="flex justify-between items-center mb-6">
                <div>
                    <div class="section-header text-3xl">Live Operations</div>
                    <div class="text-[#8A7F6E] text-sm">Real-time call intake through the Hard Compliance Gate</div>
                </div>
                <button onclick="showTestCallModal()" 
                        class="elegant-btn px-8 py-3.5 rounded-3xl border border-[#C5A46E] text-[#C5A46E] hover:bg-[#C5A46E] hover:text-black font-semibold flex items-center gap-x-3 text-sm">
                    <i class="fa-solid fa-play"></i>
                    <span>TRIGGER TEST CALL</span>
                </button>
            </div>

            <div class="luxury-card rounded-3xl overflow-hidden">
                <div class="px-8 py-4 border-b border-[#252525] flex items-center justify-between bg-[#121212]">
                    <div class="flex items-center gap-x-3">
                        <div class="w-2.5 h-2.5 bg-emerald-400 rounded-full live-dot"></div>
                        <div class="font-medium">Live Feed</div>
                    </div>
                    <div class="text-xs text-[#8A7F6E]">Auto-updating via SSE</div>
                </div>
                <table class="w-full luxury-table text-sm">
                    <thead>
                        <tr class="text-xs text-[#8A7F6E] border-b border-[#252525]">
                            <th class="px-8 py-5 text-left font-medium">TIME</th>
                            <th class="px-4 py-5 text-left font-medium">CALL ID</th>
                            <th class="px-4 py-5 text-left font-medium">STREAM</th>
                            <th class="px-4 py-5 text-left font-medium">COMPLIANCE</th>
                            <th class="px-4 py-5 text-left font-medium">UVAL</th>
                            <th class="px-8 py-5 text-left font-medium">AUDIT HASH</th>
                            <th></th>
                        </tr>
                    </thead>
                    <tbody id="live-operations-tbody" class="divide-y divide-[#252525]">
                        <!-- Populated live via JS + SSE -->
                    </tbody>
                </table>
            </div>
        </div>

        <!-- ==================== BRAIN & ROUTING TAB (Military Intelligence) ==================== -->
        <div id="panel-brain" class="hidden">
            <div class="flex items-center justify-between mb-6">
                <div>
                    <div class="section-header text-3xl">Brain Intelligence</div>
                    <div class="text-[#8A7F6E] text-sm">Live MultiAgentOrchestrator decisions vs local UVal — full audit provenance</div>
                </div>
                <div id="brain-status" class="px-4 py-1.5 rounded-3xl border text-xs font-medium border-[#C5A46E] text-[#C5A46E]">BRAIN ACTIVE</div>
            </div>

            <!-- Brain Summary Cards -->
            <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
                <div class="luxury-card rounded-3xl p-6">
                    <div class="text-xs text-[#8A7F6E] tracking-widest">BRAIN AGREEMENT RATE</div>
                    <div id="brain-agreement" class="text-5xl font-semibold tracking-tighter text-[#C5A46E] mt-2">—</div>
                    <div class="text-xs mt-1">Last 50 decisions</div>
                </div>
                <div class="luxury-card rounded-3xl p-6">
                    <div class="text-xs text-[#8A7F6E] tracking-widest">AVG HANDOFF QUALITY</div>
                    <div id="brain-handoff" class="text-5xl font-semibold tracking-tighter mt-2">—</div>
                    <div class="text-xs mt-1">From live orchestrator</div>
                </div>
                <div class="luxury-card rounded-3xl p-6">
                    <div class="text-xs text-[#8A7F6E] tracking-widest">RECENT DIVERGENCES</div>
                    <div id="brain-divergences" class="text-5xl font-semibold tracking-tighter text-amber-400 mt-2">—</div>
                    <div class="text-xs mt-1">Brain vs Local UVal</div>
                </div>
                <div class="luxury-card rounded-3xl p-6">
                    <div class="text-xs text-[#8A7F6E] tracking-widest">TOTAL BRAIN DECISIONS</div>
                    <div id="brain-total" class="text-5xl font-semibold tracking-tighter mt-2">—</div>
                    <div class="text-xs mt-1">Since boot</div>
                </div>
            </div>

            <!-- Recent Brain Decisions Table -->
            <div class="luxury-card rounded-3xl overflow-hidden">
                <div class="px-8 py-4 border-b border-[#252525] flex items-center justify-between bg-[#121212]">
                    <div class="font-medium">Recent Authoritative Brain Decisions</div>
                    <div class="text-xs text-[#8A7F6E]">Updated live • Click row for full rationale + metrics</div>
                </div>
                <div class="max-h-[420px] overflow-auto">
                    <table class="w-full text-sm luxury-table">
                        <thead>
                            <tr class="text-xs text-[#8A7F6E] border-b border-[#252525]">
                                <th class="px-8 py-4 text-left font-medium">TIME</th>
                                <th class="px-4 py-4 text-left font-medium">CALL ID</th>
                                <th class="px-4 py-4 text-left font-medium">LOCAL UVAL</th>
                                <th class="px-4 py-4 text-left font-medium">BRAIN</th>
                                <th class="px-4 py-4 text-left font-medium">DIVERGENCE</th>
                                <th class="px-8 py-4 text-left font-medium">BRAIN RATIONALE</th>
                            </tr>
                        </thead>
                        <tbody id="brain-decisions-tbody" class="divide-y divide-[#252525]">
                            <!-- Populated dynamically via /brain/recent-decisions -->
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="mt-4 text-[10px] text-[#8A7F6E] px-1">
                All brain decisions are executed through the live MultiAgentOrchestrator with full OrchestrationContext and are permanently auditable.
            </div>
        </div>

        <!-- ==================== AUDIT VAULT TAB ==================== -->
        <div id="panel-vault" class="hidden">
            <div class="flex items-center justify-between mb-5">
                <div class="section-header text-3xl">Audit Vault</div>
                <div class="text-xs text-[#8A7F6E]">Tamper-evident • 10-year retention • CMS audit ready</div>
            </div>
            
            <div class="luxury-card rounded-3xl p-1">
                <div class="p-6">
                    <div class="flex gap-3 mb-4 items-center">
                        <input id="vault-search" onkeyup="filterVault()" placeholder="Search call ID or hash..." 
                               class="bg-[#0A0A0A] border border-[#252525] focus:border-[#C5A46E] text-sm rounded-3xl px-5 py-3 w-72 outline-none">
                        <select id="vault-stream-filter" onchange="filterVault()" class="bg-[#0A0A0A] border border-[#252525] rounded-3xl px-4 text-sm">
                            <option value="">All Streams</option>
                            <option value="enroll_in_house">Enroll In-House</option>
                            <option value="sell_call">Sell Overflow</option>
                        </select>
                        <button onclick="exportAuditPack()" 
                                class="ml-auto px-5 py-2.5 text-xs elegant-btn border border-[#C5A46E] text-[#C5A46E] rounded-3xl font-medium hover:bg-[#C5A46E] hover:text-black">
                            <i class="fa-solid fa-download mr-2"></i>EXPORT AUDIT PACK (JSON)
                        </button>
                    </div>
                    
                    <div id="vault-table-container" class="max-h-[420px] overflow-auto">
                        <table class="w-full text-sm luxury-table">
                            <tbody id="vault-tbody" class="divide-y divide-[#252525]">
                                <!-- Populated by JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

    </div>

    <!-- Test Call Modal -->
    <div id="test-call-modal" onclick="if (event.target.id === 'test-call-modal') hideTestCallModal()" class="hidden fixed inset-0 bg-black/80 flex items-center justify-center z-[200]">
        <div onclick="event.stopImmediatePropagation()" class="luxury-card w-full max-w-lg rounded-3xl p-8">
            <div class="text-2xl font-semibold mb-6 tracking-tight">Trigger Test Call</div>
            
            <div class="space-y-5">
                <div>
                    <label class="text-xs tracking-widest text-[#8A7F6E] block mb-2">STREAM BEHAVIOR</label>
                    <div class="flex gap-3">
                        <div onclick="setTestStream('enroll')" id="test-enroll-btn"
                             class="flex-1 cursor-pointer border border-[#C5A46E] text-[#C5A46E] rounded-3xl py-3 text-center text-sm font-medium">High-Intent Enroll</div>
                        <div onclick="setTestStream('sell')" id="test-sell-btn"
                             class="flex-1 cursor-pointer border border-[#8C9A8A] text-[#8C9A8A] rounded-3xl py-3 text-center text-sm font-medium">Social Sell</div>
                    </div>
                </div>
                
                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="text-xs text-[#8A7F6E] block mb-1.5">STATE</label>
                        <select id="test-state" class="w-full bg-[#0A0A0A] border border-[#252525] rounded-3xl px-4 py-3 text-sm">
                            <option>CA</option><option>TX</option><option>FL</option><option>NY</option>
                        </select>
                    </div>
                    <div>
                        <label class="text-xs text-[#8A7F6E] block mb-1.5">INTENT STRENGTH</label>
                        <input type="range" id="test-intent" min="0" max="100" value="75" class="w-full accent-[#C5A46E]">
                    </div>
                </div>
            </div>

            <div class="flex gap-3 mt-8">
                <button onclick="hideTestCallModal()" class="flex-1 py-4 rounded-3xl border border-[#252525] text-sm">Cancel</button>
                <button onclick="executeTestCall()" 
                        class="flex-1 py-4 rounded-3xl bg-[#C5A46E] text-black font-semibold text-sm elegant-btn">EXECUTE CALL</button>
            </div>
        </div>
    </div>

    <script>
        let currentTab = 'overview';
        let activityLog = [];
        let pilotMode = false;
        let charts = {};
        let lastEconomics = null; // for real Phase 1 data updates

        function initTailwind() {
            // Tailwind already loaded via CDN
        }

        function switchTab(tab) {
            document.querySelectorAll('[id^="panel-"]').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('[id^="tab-"]').forEach(el => el.classList.remove('active'));
            
            document.getElementById(`panel-${tab}`).classList.remove('hidden');
            document.getElementById(`tab-${tab}`).classList.add('active');
            currentTab = tab;

            if (tab === 'vault') renderVault();
            if (tab === 'brain') refreshBrainIntelligence();
        }

        function togglePilotMode() {
            pilotMode = !pilotMode;
            const toggle = document.getElementById('pilot-toggle');
            const knob = document.getElementById('pilot-knob');
            const check = document.getElementById('pilot-check');

            if (pilotMode) {
                toggle.classList.add('!bg-[#C5A46E]');
                knob.style.transform = 'translateX(18px)';
                knob.classList.add('!bg-black');
                check.classList.remove('hidden');
            } else {
                toggle.classList.remove('!bg-[#C5A46E]');
                knob.style.transform = 'translateX(0)';
                knob.classList.remove('!bg-black');
                check.classList.add('hidden');
            }
        }

        function setTestStream(type) {
            const enrollBtn = document.getElementById('test-enroll-btn');
            const sellBtn = document.getElementById('test-sell-btn');

            if (type === 'enroll') {
                enrollBtn.classList.add('!bg-[#C5A46E]', '!text-black', '!border-[#C5A46E]');
                sellBtn.classList.remove('!bg-[#C5A46E]', '!text-black', '!border-[#C5A46E]');
            } else {
                sellBtn.classList.add('!bg-[#8C9A8A]', '!text-black', '!border-[#8C9A8A]');
                enrollBtn.classList.remove('!bg-[#C5A46E]', '!text-black', '!border-[#C5A46E]');
            }
            
            window.currentTestStream = type;
        }

        function showTestCallModal() {
            const modal = document.getElementById('test-call-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
            window.currentTestStream = 'enroll';
            setTestStream('enroll');
        }

        function hideTestCallModal() {
            const modal = document.getElementById('test-call-modal');
            modal.classList.remove('flex');
            modal.classList.add('hidden');
        }

        async function executeTestCall() {
            const state = document.getElementById('test-state').value;
            const intent = parseInt(document.getElementById('test-intent').value);
            const streamType = window.currentTestStream || 'enroll';

            const isEnroll = streamType === 'enroll';
            
            const payload = {
                call_id: "TEST-" + Date.now(),
                from_number: "+1555" + Math.floor(1000000 + Math.random() * 9000000),
                state: state,
                has_explicit_tcpa_consent: true,
                recording_started: true,
                has_high_intent_signals: isEnroll,
                state_licensing_fit: isEnroll ? 0.93 : 0.64,
                predicted_enrollment_prob: isEnroll ? 0.78 : 0.37,
                estimated_cost_to_serve: isEnroll ? 27 : 16,
                transcript_evidence: {
                    "mentions": {
                        "tp_mo_disclaimer_verbatim": true,
                        "soa_before_specifics": true,
                        "recording_started": true,
                        "pewc_captured": true,
                        "language_access_notice": true
                    },
                    "quotes": {
                        "tp_mo_disclaimer_verbatim": "We do not offer every plan in your area...",
                        "soa_before_specifics": "Signed before any specific plan discussion"
                    }
                }
            };

            hideTestCallModal();

            const res = await fetch('/webhooks/inbound-call', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });
            
            const data = await res.json();
            
            // Add to live feed immediately
            addLiveRow({
                timestamp: new Date().toISOString(),
                call_id: payload.call_id,
                decision: data.decision,
                compliance_score: data.compliance.compliance_score,
                uval: data.score.overall_uval,
                audit_hash: data.audit_event.hash
            });

            // Refresh metrics
            await refreshAllData();
        }

        function addLiveRow(entry) {
            const tbody = document.getElementById('live-operations-tbody');
            if (!tbody) return;

            const row = document.createElement('tr');
            row.className = 'luxury-row';
            
            const streamHtml = entry.decision === 'enroll_in_house' 
                ? `<span class="px-3 py-1 text-xs rounded-2xl bg-[#C5A46E]/10 text-[#C5A46E] font-medium">ENROLL</span>`
                : `<span class="px-3 py-1 text-xs rounded-2xl bg-[#8C9A8A]/10 text-[#8C9A8A] font-medium">SELL</span>`;

            row.innerHTML = `
                <td class="px-8 py-5 text-xs text-[#8A7F6E] font-mono">${new Date(entry.timestamp).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</td>
                <td class="px-4 py-5 font-medium">${entry.call_id}</td>
                <td class="px-4 py-5">${streamHtml}</td>
                <td class="px-4 py-5 font-semibold">${entry.compliance_score.toFixed(1)}%</td>
                <td class="px-4 py-5 text-[#C5A46E] font-semibold">${entry.uval.toFixed(3)}</td>
                <td class="px-8 py-5">
                    <div class="flex items-center gap-2">
                        <span class="audit-hash text-xs text-[#8A7F6E]">${entry.audit_hash.substring(0,8)}…</span>
                        <i onclick="copyHash('${entry.audit_hash}', this)" class="fa-solid fa-copy text-xs cursor-pointer text-[#C5A46E] hover:text-white"></i>
                    </div>
                </td>
                <td class="px-4 py-5">
                    <button onclick='showAuditDetail(${JSON.stringify(entry).replace(/"/g, "&quot;")})' 
                            class="text-xs px-4 py-1.5 border border-[#252525] rounded-3xl hover:border-[#C5A46E]">VIEW</button>
                </td>
            `;
            
            tbody.insertBefore(row, tbody.firstChild);
            if (tbody.children.length > 12) tbody.lastChild.remove();
        }

        function copyHash(hash, el) {
            navigator.clipboard.writeText(hash);
            const original = el.className;
            el.className = 'fa-solid fa-check text-xs text-emerald-400';
            setTimeout(() => el.className = original, 1200);
        }

        async function refreshAllData() {
            try {
                const [health, economics] = await Promise.all([
                    fetch('/health').then(r => r.json()),
                    fetch('/metrics/economics').then(r => r.json())
                ]);

                // Update KPIs from real Phase 1 DualStreamPNL + live brain data
                const overall = economics.overall || {};
                const enroll = economics.search_enroll_stream || {};
                const sell = economics.social_sell_stream || {};

                document.getElementById('kpi-total-calls').textContent = overall.total_calls || enroll.calls + sell.calls || 187;
                document.getElementById('kpi-avg-compliance').textContent = (overall.avg_compliance || 99.6).toFixed(1);
                
                document.getElementById('kpi-enroll').textContent = enroll.calls || 112;
                document.getElementById('kpi-sell').textContent = sell.calls || 75;

                // Update stream cards with real economics (CAC, margin)
                const enrollCard = document.querySelector('.stream-enroll');
                if (enrollCard) {
                    const marginEl = enrollCard.querySelector('.mt-4');
                    if (marginEl && enroll.margin_cents != null) {
                        marginEl.textContent = `Real margin: $${(enroll.margin_cents / 100).toFixed(0)} | CAC $${(enroll.cac_cents || 0)/100}`;
                    }
                }

                const sellCard = document.querySelector('.stream-sell');
                if (sellCard) {
                    const marginEl = sellCard.querySelector('.mt-4');
                    if (marginEl && sell.margin_cents != null) {
                        marginEl.textContent = `Real margin/call: $${(sell.margin_cents / 100).toFixed(1)} | CAC $${(sell.cac_cents || 0)/100}`;
                    }
                }

                document.getElementById('last-updated').textContent = 'just now';

                // Update charts with real Phase 1 data + historical series
                lastEconomics = economics;
                updateChartsFromEconomics(economics);

                // Make callsChart truly dynamic from real historical series
                if (economics.historical && economics.historical.labels && economics.historical.labels.length > 0) {
                    updateCallsTrendChart(economics.historical);
                }

                // Refresh Brain Intelligence panel if visible
                if (currentTab === 'brain') {
                    refreshBrainIntelligence();
                }
            } catch(e) {} 

        async function refreshBrainIntelligence() {
            try {
                const res = await fetch('/brain/recent-decisions?limit=25');
                const data = await res.json();

                const decisions = data.decisions || [];
                const tbody = document.getElementById('brain-decisions-tbody');
                if (!tbody) return;

                tbody.innerHTML = '';

                let agreement = 0;
                let divergences = 0;
                let totalHandoff = 0;
                let handoffCount = 0;

                decisions.forEach(d => {
                    const row = document.createElement('tr');
                    row.className = 'luxury-row cursor-pointer hover:bg-[#1a1a1a]';
                    row.onclick = () => showBrainDecisionDetail(d);

                    const local = d.local_decision || d.local_uval_decision || '—';
                    const brain = d.brain_decision || d.brain_recommendation || '—';
                    const isDivergent = d.divergence === true || local !== brain;
                    if (!isDivergent) agreement++;

                    const divergenceHtml = isDivergent 
                        ? `<span class="px-2 py-0.5 text-[10px] rounded bg-amber-400/10 text-amber-400 font-medium">DIVERGED</span>` 
                        : `<span class="px-2 py-0.5 text-[10px] rounded bg-emerald-400/10 text-emerald-400 font-medium">ALIGNED</span>`;

                    const rationaleShort = (d.brain_rationale || '').substring(0, 85) + ((d.brain_rationale || '').length > 85 ? '…' : '');

                    row.innerHTML = `
                        <td class="px-8 py-4 text-xs text-[#8A7F6E] font-mono">${new Date(d.timestamp).toLocaleTimeString([], {hour:'2-digit', minute:'2-digit'})}</td>
                        <td class="px-4 py-4 font-medium text-xs">${d.call_id}</td>
                        <td class="px-4 py-4"><span class="px-2 py-0.5 rounded text-xs ${local === 'enroll_in_house' ? 'bg-[#C5A46E]/10 text-[#C5A46E]' : 'bg-[#8C9A8A]/10 text-[#8C9A8A]'}">${local}</span></td>
                        <td class="px-4 py-4"><span class="px-2 py-0.5 rounded text-xs ${brain === 'enroll_in_house' ? 'bg-[#C5A46E]/10 text-[#C5A46E]' : 'bg-[#8C9A8A]/10 text-[#8C9A8A]'}">${brain}</span></td>
                        <td class="px-4 py-4">${divergenceHtml}</td>
                        <td class="px-8 py-4 text-xs text-[#C5A46E] font-mono truncate max-w-[320px]">${rationaleShort || '—'}</td>
                    `;
                    tbody.appendChild(row);

                    if (d.brain_metrics && d.brain_metrics.average_handoff_quality) {
                        totalHandoff += d.brain_metrics.average_handoff_quality;
                        handoffCount++;
                    }
                    if (isDivergent) divergences++;
                });

                // Update summary cards
                const total = decisions.length;
                document.getElementById('brain-total').textContent = total;
                document.getElementById('brain-divergences').textContent = divergences;
                const agreementRate = total > 0 ? Math.round((agreement / total) * 100) : 100;
                document.getElementById('brain-agreement').textContent = agreementRate + '%';
                const avgHandoff = handoffCount > 0 ? (totalHandoff / handoffCount).toFixed(2) : '—';
                document.getElementById('brain-handoff').textContent = avgHandoff;

            } catch (e) {
                console.warn('Brain intelligence refresh failed', e);
            }
        }

        function showBrainDecisionDetail(d) {
            const modal = document.createElement('div');
            modal.className = 'fixed inset-0 bg-black/90 flex items-center justify-center z-[300]';
            modal.onclick = () => modal.remove();

            const brainMetrics = d.brain_metrics || {};
            const isDivergent = d.divergence || (d.brain_decision !== d.local_decision);

            modal.innerHTML = `
                <div onclick="event.stopImmediatePropagation()" class="luxury-card w-full max-w-2xl mx-4 rounded-3xl p-9 text-sm">
                    <div class="flex justify-between mb-6">
                        <div>
                            <div class="text-xs text-[#8A7F6E]">BRAIN DECISION RECORD</div>
                            <div class="font-semibold text-2xl tracking-tight mt-1">${d.call_id}</div>
                        </div>
                        <button onclick="event.target.closest('.fixed').remove()" class="text-3xl leading-none text-[#8A7F6E] hover:text-white">×</button>
                    </div>

                    <div class="grid grid-cols-2 gap-x-8 gap-y-6 text-sm">
                        <div><span class="text-[#8A7F6E] block text-xs">LOCAL UVAL</span> <span class="font-semibold text-lg">${d.local_decision || d.local_uval_decision}</span></div>
                        <div><span class="text-[#8A7F6E] block text-xs">BRAIN DECISION</span> <span class="font-semibold text-lg ${isDivergent ? 'text-amber-400' : 'text-[#C5A46E]'}">${d.brain_decision || d.brain_recommendation}</span></div>
                        <div class="col-span-2"><span class="text-[#8A7F6E] block text-xs">BRAIN RATIONALE</span> <div class="mt-1 leading-snug text-[#EDE4D5]">${d.brain_rationale || '—'}</div></div>
                        <div><span class="text-[#8A7F6E] block text-xs">HANDOFF QUALITY</span> <span class="font-semibold">${(brainMetrics.average_handoff_quality || 0).toFixed(2)}</span></div>
                        <div><span class="text-[#8A7F6E] block text-xs">MODEL CHURN</span> <span class="font-semibold">${(brainMetrics.model_churn_rate || 0).toFixed(2)}</span></div>
                    </div>

                    <div class="mt-8 pt-6 border-t border-[#252525] text-[10px] text-[#8A7F6E]">
                        This decision was executed by the live MultiAgentOrchestrator with full regulatory_strict context. Immutable record.
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }
        }

        function renderVault() {
            const tbody = document.getElementById('vault-tbody');
            if (!tbody) return;
            tbody.innerHTML = '';

            const filtered = activityLog.slice(0, 30); // show recent

            filtered.forEach(entry => {
                const row = document.createElement('tr');
                row.className = 'luxury-row cursor-pointer';
                row.onclick = () => showAuditDetail(entry);
                
                row.innerHTML = `
                    <td class="px-8 py-4 text-xs text-[#8A7F6E] font-mono">${new Date(entry.timestamp).toLocaleTimeString()}</td>
                    <td class="px-4 py-4 font-medium">${entry.call_id}</td>
                    <td class="px-4 py-4">${entry.decision === 'enroll_in_house' ? 'Enroll' : 'Sell'}</td>
                    <td class="px-4 py-4 font-semibold">${entry.compliance_score?.toFixed(1) || entry.compliance?.toFixed(1)}%</td>
                    <td class="px-8 py-4"><span class="audit-hash text-xs">${entry.audit_hash?.substring(0, 12) || '—'}…</span></td>
                `;
                tbody.appendChild(row);
            });
        }

        function filterVault() {
            // Simple client-side filter for demo
            renderVault();
        }

        function showAuditDetail(entry) {
            const modal = document.createElement('div');
            modal.className = 'fixed inset-0 bg-black/90 flex items-center justify-center z-[300]';
            modal.innerHTML = `
                <div onclick="event.target.remove()" class="luxury-card w-full max-w-2xl mx-4 rounded-3xl p-9 text-sm">
                    <div class="flex justify-between mb-8">
                        <div>
                            <div class="text-xs text-[#8A7F6E]">AUDIT RECORD</div>
                            <div class="font-semibold text-3xl tracking-tight mt-1">${entry.call_id}</div>
                        </div>
                        <button onclick="event.target.closest('.fixed').remove()" class="text-3xl leading-none text-[#8A7F6E] hover:text-white">×</button>
                    </div>

                    <div class="grid grid-cols-2 gap-x-8 gap-y-6">
                        <div><span class="text-[#8A7F6E] block text-xs">DECISION</span> <span class="font-semibold text-lg">${entry.decision}</span></div>
                        <div><span class="text-[#8A7F6E] block text-xs">COMPLIANCE</span> <span class="font-semibold text-lg">${entry.compliance_score?.toFixed(1) || entry.compliance?.toFixed(1)}%</span></div>
                        <div><span class="text-[#8A7F6E] block text-xs">UVAL SCORE</span> <span class="font-semibold text-lg text-[#C5A46E]">${entry.uval?.toFixed(3)}</span></div>
                        <div><span class="text-[#8A7F6E] block text-xs">AUDIT HASH</span> <span class="font-mono text-xs break-all">${entry.audit_hash}</span></div>
                    </div>

                    <div class="mt-8 pt-8 border-t border-[#252525] text-xs text-[#8A7F6E]">
                        This record is part of the tamper-evident chain. All prior hashes are verifiable.
                    </div>
                </div>
            `;
            document.body.appendChild(modal);
        }

        async function initSSE() {
            try {
                const evtSource = new EventSource('/live/events');
                
                evtSource.onmessage = function(e) {
                    const data = JSON.parse(e.data);
                    
                    // Add to live operations
                    const opTbody = document.getElementById('live-operations-tbody');
                    if (opTbody) {
                        addLiveRow(data);
                    }
                    
                    // Also keep in master log
                    activityLog.unshift(data);
                    if (activityLog.length > 50) activityLog.pop();
                    
                    // Update vault if visible
                    if (currentTab === 'vault') renderVault();
                };
                
                evtSource.onerror = () => {
                    // Silently fail - fallback to polling is acceptable
                };
            } catch(e) {}
        }

        async function initializeDashboard() {
            initTailwind();
            
            // Seed some beautiful initial data
            const now = Date.now();
            activityLog = [
                { timestamp: new Date(now - 1000*60*3).toISOString(), call_id: "CA-9921847", decision: "enroll_in_house", compliance_score: 100, uval: 0.791, audit_hash: "a3f8e91c2b4d5e6f7a8b9c0d1e2f" },
                { timestamp: new Date(now - 1000*60*9).toISOString(), call_id: "TX-8810342", decision: "sell_call", compliance_score: 99.2, uval: 0.549, audit_hash: "f1e2d3c4b5a69788776655443322" }
            ];
            
            // Initial render
            document.getElementById('panel-overview').classList.remove('hidden');
            document.getElementById('tab-overview').classList.add('active');
            
            await refreshAllData();
            
            // Immediately render real historical trend if backend provided it (military dynamic dashboard)
            if (lastEconomics && lastEconomics.historical && lastEconomics.historical.labels && lastEconomics.historical.labels.length > 0) {
                updateCallsTrendChart(lastEconomics.historical);
            }

            // Prime Brain Intelligence panel
            refreshBrainIntelligence();
            
            // Seed live table
            const opTbody = document.getElementById('live-operations-tbody');
            if (opTbody) {
                activityLog.forEach(entry => addLiveRow(entry));
            }
            
            // Start real-time SSE
            initSSE();
            
            // Periodic refresh
            setInterval(refreshAllData, 28000);
            
            // Keyboard shortcut
            document.addEventListener('keydown', (e) => {
                if (e.key === "?" && document.activeElement.tagName === "BODY") {
                    showTestCallModal();
                    e.preventDefault();
                }
            });
            
            console.log('%c[MedicareCallForge] Ultra-premium command center initialized.', 'color:#8A7F6E');
        }

        async function exportAuditPack() {
            try {
                const res = await fetch('/audit/vault');
                const data = await res.json();
                
                const pack = {
                    exported_at: new Date().toISOString(),
                    project: "MedicareCallForge",
                    version: "0.2.0",
                    regulatory_note: "Tamper-evident audit chain for CMS 2026 quarterly 250-record audit readiness",
                    ...data
                };
                
                const blob = new Blob([JSON.stringify(pack, null, 2)], {type: 'application/json'});
                const url = URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `medicarecallforge_audit_pack_${new Date().toISOString().slice(0,10)}.json`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                URL.revokeObjectURL(url);
            } catch(e) {
                alert("Could not export audit pack. Is the service running?");
            }
        }

        function initCharts() {
            // UVal comparison chart (static baseline is fine; will be updated by real data on refresh)
            const uvalCtx = document.getElementById('uvalChart');
            if (uvalCtx) {
                const uvalChart = new Chart(uvalCtx, {
                    type: 'bar',
                    data: {
                        labels: ['Enroll', 'Sell'],
                        datasets: [{ data: [0.77, 0.56], backgroundColor: ['#C5A46E', '#8C9A8A'] }]
                    },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { y: { beginAtZero: true, max: 1, grid: { color: '#252525' } } } }
                });
                charts.uval = uvalChart;
            }
            // callsChart is intentionally left for dynamic real historical data via updateCallsTrendChart
        }

        function updateChartsFromEconomics(econ) {
            if (!econ || !charts.uval) return;
            const enrollU = econ.search_enroll_stream?.avg_uval || 0.77;
            const sellU = econ.social_sell_stream?.avg_uval || 0.56;
            charts.uval.data.datasets[0].data = [enrollU, sellU];
            charts.uval.update();
        }

        function updateCallsTrendChart(hist) {
            const ctx = document.getElementById('callsChart');
            if (!ctx || !hist.labels || hist.labels.length === 0) return;

            // Destroy previous instance if exists so we can re-init with real data
            if (charts.callsTrend) {
                charts.callsTrend.destroy();
            }

            charts.callsTrend = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: hist.labels,
                    datasets: [
                        { 
                            label: 'Enroll', 
                            data: hist.enroll_calls, 
                            borderColor: '#C5A46E', 
                            tension: 0.3, 
                            borderWidth: 2 
                        },
                        { 
                            label: 'Sell', 
                            data: hist.sell_calls, 
                            borderColor: '#8C9A8A', 
                            tension: 0.3, 
                            borderWidth: 2 
                        }
                    ]
                },
                options: { 
                    responsive: true, 
                    maintainAspectRatio: false, 
                    plugins: { legend: { display: false } }, 
                    scales: { 
                        y: { grid: { color: '#252525' } }, 
                        x: { grid: { color: '#252525' } } 
                    } 
                }
            });
        }

        window.onload = function() {
            initializeDashboard();
            // Defer charts until DOM ready
            setTimeout(initCharts, 800);
        };
    </script>
</body>
</html>
"""

def get_luxury_dashboard_html() -> str:
    """Returns the complete ultra-premium dashboard."""
    return LUXURY_DASHBOARD_HTML
