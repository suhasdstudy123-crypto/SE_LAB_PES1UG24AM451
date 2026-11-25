# Lab 3 – Component Modelling & Architectural Pattern Selection

**Name:** Suhas D  **SRN:** PES1UG24AM451  **Section:** H
**Scenario:** Problem Statement #43 – Feature Flag & Dynamic Config Manager (same scenario as Lab 1 and Lab 2)

## Deliverables

| File | Description |
|------|-------------|
| `Component_Diagram_PES1UG24AM451.png` / `.pdf` | UML component diagram |
| `Lab3_Justification_PES1UG24AM451.docx` / `.pdf` | One-page architectural justification |

## Architecture: Microservices

| Group | Components |
|-------|------------|
| Presentation | Admin Dashboard (used by Software Engineer / Release Manager) |
| Control Plane | Auth & RBAC Service, Flag Management Service |
| Data Plane | Flag Evaluation Service, Real-time Sync Service |
| Data & Messaging | Config Store, Audit Log Service, Event Bus |
| External | Client SDK (embedded in client applications) |

## Interfaces (provided → required)

| Interface | Provider | Required by | Technology |
|-----------|----------|-------------|------------|
| `IAuthenticate` | Auth & RBAC Service | Admin Dashboard | OAuth2 / OIDC login (HTTPS) |
| `IFlagAdminAPI` | Flag Management | Admin Dashboard | REST API (HTTPS / JSON) |
| `IAuthorize` | Auth & RBAC Service | Flag Management | JWT role check |
| `IFlagRepository` | Config Store | Flag Management | DB queries (SQL) |
| `IAuditLog` | Audit Log Service | Flag Management | async API call |
| `IPublishChange` | Event Bus | Flag Management | publish event (pub/sub) |
| `IChangeStream` | Event Bus | Real-time Sync, Flag Evaluation | subscribe (pub/sub) |
| `IFlagEvaluation` | Flag Evaluation | Client SDK | REST / gRPC API call |
| `IFlagStream` | Real-time Sync Service | Client SDK | SSE / WebSocket push |

## Mapping to Lab 1 requirements

| Requirement | Component |
|-------------|-----------|
| FR-001 Evaluate targeting rules | Flag Evaluation |
| FR-002 Create feature flag | Flag Management |
| FR-003 Percentage rollout | Flag Management, Flag Evaluation |
| FR-004 Environment overrides | Flag Management, Config Store |
| FR-005 Sync to client SDKs within 5 s | Event Bus, Real-time Sync Service |
| NFR-001 Evaluation under 15 ms | Flag Evaluation (in-memory rule cache) |
| NFR-002 Only Release Manager changes rollouts | Auth & RBAC Service |

8 internal components + 1 external, 9 interface connections, drawn in ball (provided) / socket (required) notation.
