# CHAPTER 1: Business Requirements Document (BRD)

## 1.1 Problem Statement
In the era of digital transformation, the retail and logistics industries are under immense pressure to increase speed and accuracy. However, a persistent "data entry bottleneck" continues to hinder operational efficiency: **Manual Invoice Processing**.

* **Operational Inefficiency:** Warehouse staff spend hours daily manually transcribing information from paper or PDF invoices into Management Information Systems (MIS).
* **High Error Rates:** Manual entry typically results in an error rate of 3% to 5%, leading to severe consequences such as inventory discrepancies, incorrect Cost of Goods Sold (COGS), and financial loss.
* **Naming Inconsistencies:** Product names on supplier invoices rarely match the internal Stock Keeping Unit (SKU) names, making reconciliation and database synchronization a complex manual task.

Consequently, there is an urgent need for a system capable of "reading" invoices and automating the inbound inventory workflow using Artificial Intelligence.

## 1.2 Project Objectives
* **Automated Extraction:** Develop an AI-powered OCR pipeline to extract structured data from invoices with over 95% accuracy.
* **Data Standardization:** Build an Intelligent Matching Engine to automatically map supplier product descriptions to internal inventory catalogs.
* **Operational Optimization:** Reduce manual data entry time by up to 95% and eliminate human-induced data errors.
* **Real-time Management:** Provide a centralized dashboard for tracking stock levels and purchase price fluctuations in real-time.

## 1.3 Project Scope
* **Document Types:** Focus on Value Added Tax (VAT) invoices and delivery notes within the retail and Fast-Moving Consumer Goods (FMCG) sectors.
* **Core Technology:** A modern full-stack ecosystem including Next.js (Frontend), FastAPI (Backend), PostgreSQL (Database), and Gemini 1.5 Flash/ Google Cloud Document AI.
* **Constraints:** The system focuses on Inbound Logistics (Receiving); it does not currently cover outbound shipping or direct banking payment integration.

## 1.4 Proposed Solution
The project implements a comprehensive End-to-End Pipeline that bridges Artificial Intelligence with robust data processing logic:

1.  **Cloud Ingestion Layer:** Utilize AWS S3/ Supabase for secure storage of raw invoice images, ensuring high availability for AI processing services.
2.  **AI Extraction Layer:** Leverage Google Cloud Document AI to transform unstructured data (Images/PDFs) into structured formats (Line-items, Tax, Totals).
3.  **Intelligent Matching Engine:**
    * Employ the **RapidFuzz** library for advanced string similarity (Fuzzy Matching).
    * Apply a **Weighted Keyword Scoring** algorithm to handle abbreviations and naming variations.
4.  **Human-in-the-loop Interface:** Provide a Validation UI that allows users to review and calibrate AI outputs before final database entry, ensuring 100% data integrity.

## 1.5 Market Research & Competitive Analysis

### Market Overview
The market for invoice digitization and inventory management is divided into three main segments. While powerful, each has specific barriers for small to medium enterprises.

| Competitor Type | Examples | Pros | Cons |
| :--- | :--- | :--- | :--- |
| **Enterprise ERP** | SAP, Oracle, MS Dynamics | Robust, all-in-one integration, high security. | Extremely high cost, complex implementation, rigid workflows. |
| **Traditional OCR Tools** | Abbyy FineReader, Adobe Acrobat | High text reliability, established technology. | Lack of business logic; cannot match products or update stock automatically. |
| **SaaS Invoice Solutions** | Rossum.ai, Bill.com | Advanced AI, modern UI, cloud-based. | Expensive monthly subscriptions; focused on accounting rather than warehouse operations. |

### SmartStock AI Competitive Edge
SmartStock AI bridges the "automation gap" by focusing specifically on the relationship between invoice data and physical inventory:

* **Contextual Intelligence:** Unlike traditional OCR that only "sees" characters, our system uses Gemini 1.5 Flash/ Google Cloud Document AI to "understand" product descriptions, units, and categories.
* **End-to-End Workflow:** It provides a seamless transition from Scan → Extract → Match SKU → Update Stock in a single unified pipeline.
* **Intelligent Reconciliation:** Specifically handles the discrepancy between supplier naming conventions and internal SKU records through advanced fuzzy logic.
* **Cost Efficiency:** By utilizing a "Pay-as-you-go" API model, the system eliminates the heavy upfront licensing fees associated with enterprise software.
* **Operational Speed:** The split-view verification and automated suggestions reduce manual data entry time by up to 70%, minimizing human error.
* **Agile Adaptability:** Through prompt engineering, the system can adapt to new invoice layouts instantly without needing to retrain complex machine learning models.