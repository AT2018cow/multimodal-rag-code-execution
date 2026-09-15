# Service Inventory — configuration & verified daily costs

> All identifiers use placeholders (`<UNIQUE_SUFFIX>` = Bicep `uniqueString(resourceGroup().id)`).
> Unit prices verified via the Azure Retail Prices API (East US). Costs marked "MfS Floor"
> count toward the 5 workloads needed for Microsoft for Startups Milestone 3 (≥$1/day each).

## Application hosting

| Service | Configuration | Daily cost | MfS Floor |
|---|---|---|---|
| App Service Plan `B3` (Linux) | 1 instance, 4 vCPU / 7 GB RAM | **$1.61** ($0.067/hr) | ✅ |
| — hosts: chat UI (Chainlit) | `dev-app-chat-<UNIQUE_SUFFIX>.azurewebsites.net` | ↑ shared | — |
| — hosts: API (FastAPI) | `dev-app-api-<UNIQUE_SUFFIX>.azurewebsites.net` | ↑ shared | — |
| Container App (Streamlit) | 0.5 vCPU / 1 GiB, minReplicas 1 | ~$0.40 | (not MfS-tracked) |
| Container Apps Environment | consumption profile, no base charge | $0 | — |

## Data & retrieval

| Service | Configuration | Daily cost | MfS Floor |
|---|---|---|---|
| Azure AI Search | `basic` tier, 1 replica × 1 partition, semantic ranker enabled | **$2.42** ($0.101/hr) | ✅ |
| Azure Cosmos DB | provisioned **800 RU/s** shared throughput, EastUS2, `disableLocalAuth=true` | **$1.54** ($0.008/hr per 100 RU/s) | ✅ |
| Storage (file share) | Premium LRS, **quota 250 GB** (bicep default is 1024 GB — reduce after every re-provision) | **$1.33** ($0.16/GB/month) | ✅ |
| Storage (AML artifacts) | Standard LRS, `allowSharedKeyAccess=true` (AML v1 SDK requirement) | ~$0.05 | — |

## AI services

| Service | Configuration | Daily cost | MfS Floor |
|---|---|---|---|
| Azure AI Foundry (Foundry account) | kind `AIServices`, **EastUS2**, deployments: `gpt-5.6-luna` (capacity 4998, GlobalStandard) + `text-embedding-3-large` | **$0 idle** (per-token: $0.20/1M in, $1.20/1M out) | — |
| Document Intelligence | S0, West Europe, `disableLocalAuth=true`, api-version `2024-11-30` | $0 idle (~$0.002/page) | — |
| Vision (ComputerVision) | S1, `publicNetworkAccess=Enabled`, `networkAcls.defaultAction=Deny` | $0 idle (per-call) | — |

## Networking & security

| Service | Configuration | Daily cost | MfS Floor |
|---|---|---|---|
| Private Link (5 endpoints) | pe-search, pe-cosmos, pe-storage, pe-di, pe-vision | **$1.15-1.20** ($0.01/hr x 5) | MfS: Virtual Network |
| Private DNS zones (4) | privatelink.{search, documents, file, cognitiveservices} | ~$0.07 | — |
| VNet + 3 subnets | 10.20.0.0/16; snet-endpoints, snet-appservice, snet-aml (no delegation on snet-aml!) | $0 | — |

## Platform & support

| Service | Configuration | Daily cost | MfS Floor |
|---|---|---|---|
| Container Registry | `Basic` tier, admin user **disabled**, identity-based pulls | $0.17 | — |
| Key Vault | Standard, access-policy model, firewall: Deny + plan outbound IPs + team IP | ~$0.01 | — |
| Log Analytics | 30-day retention, **1 GB/day ingestion cap** | ~$0.10 | — |
| App Insights | connected to Log Analytics workspace | ~$0.05 | — |
| AML Workspace | with attached ACR, uami identity on compute cluster | $0 | — |
| AML Compute Cluster | `STANDARD_D2S_V3`, min 0 / max 3, **idle scale-down 10 min** | $0 (0 nodes idle) / $0.096/hr when running | — |
| Managed Identity (uami) | used for: KV references, ACR pulls, Entra data-plane auth, AML compute | $0 | — |

## Cost summary

| | Amount |
|---|---|
| **Fixed daily total** | **≈ $10.3** |
| **Fixed monthly total** | **≈ $310** |
| Variable (OpenAI tokens + DI pages + AML compute) | $1–3/day typical |
| **Typical daily total** | **$11–13** |
| MfS credits budget | $5,000 (consumed ~6–7%/month) |

## MfS Milestone 3 - 5 confirmed workloads (>= $1/day, verified in MfS portal)

| # | MfS Portal Category | Azure Service | Daily cost | Headroom |
|---|---|---|---|---|
| 1 | Azure Cognitive Search | AI Search basic | $2.42 | +142% |
| 2 | Azure App Service | B3 plan | $1.61 | +61% |
| 3 | Azure Cosmos DB | 800 RU/s | $1.54 | +54% |
| 4 | Storage | Premium file share 250GB | $1.33 | +33% |
| 5 | **Virtual Network** | **Private Link 5 endpoints** | **$1.15** | **+15%** |

> Verified in MfS portal (2026-09-15): Private Link endpoints are tracked as "Virtual
> Network" and show $1.15/day. Container Apps is NOT tracked by the MfS portal.
> These 5 workloads are the definitive milestone floors.
