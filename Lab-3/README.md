# Lab 3 – Component Modelling & Architectural Pattern Selection

**Name:** Suhas D  **SRN:** PES1UG24AM451
**Scenario:** Self-Service Coffee Kiosk System (from the Lab 3 handout)

## Deliverables

| File | Description |
|------|-------------|
| `Component_Diagram_PES1UG24AM451.png` / `.pdf` | UML component diagram |
| `Lab3_Justification_PES1UG24AM451.docx` / `.pdf` | One-page architectural justification |

## Architecture: Layered

| Layer | Components |
|-------|------------|
| Presentation | Touch Screen UI |
| Business Logic | Order Manager *(given)*, Payment Service *(given)* |
| Data & Hardware Access | Menu & Pricing Catalog, Receipt Printer Service |
| External | Card Payment Gateway (card reader + bank processor) |

## Interfaces (provided → required)

| Interface | Provider | Required by | Technology |
|-----------|----------|-------------|------------|
| `IOrderService` | Order Manager | Touch Screen UI | API call |
| `IPayment` *(given)* | Payment Service | Order Manager | API call – payment request |
| `IPaymentStatus` | Payment Service | Touch Screen UI | API call / event |
| `IMenuData` | Menu & Pricing Catalog | Order Manager | DB query (local SQLite) |
| `IReceiptPrint` | Receipt Printer Service | Order Manager | Hardware interface (USB / ESC-POS) |
| `ICardAuthorization` | Card Payment Gateway | Payment Service | HTTPS / TLS (PCI-DSS) |

5 internal components + 1 external, 6 interfaces, drawn in ball (provided) / socket (required) notation.
