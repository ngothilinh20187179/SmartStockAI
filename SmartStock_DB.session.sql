-- Extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- ENUM
CREATE TYPE user_status AS ENUM ('active', 'inactive', 'suspended');
CREATE TYPE user_role AS ENUM ('manager', 'staff');
CREATE TYPE supplier_status AS ENUM ('active', 'inactive');
CREATE TYPE invoice_status AS ENUM ('pending', 'processing', 'completed', 'error');
CREATE TYPE payment_status AS ENUM ('unpaid', 'partially_paid', 'paid', 'refunded');
CREATE TYPE product_status AS ENUM ('in_stock', 'out_of_stock', 'low_stock', 'discontinued');
CREATE TYPE transaction_type AS ENUM ('import', 'export', 'inventory_check', 'adjustment');

-- TABLES
CREATE TABLE Users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_name VARCHAR(100) NOT NULL,
    hash_password TEXT NOT NULL,
    role user_role DEFAULT 'staff',
    email VARCHAR(255) UNIQUE,
    status user_status DEFAULT 'active'
);

CREATE TABLE Suppliers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    supplier_name VARCHAR(255) NOT NULL,
    tax_code VARCHAR(50), -- ABN (Australian Business Number)
    supplier_code VARCHAR(50) UNIQUE,
    phone VARCHAR(20),
    email VARCHAR(100),
    website VARCHAR(255),
    address TEXT,
    bank_account_number VARCHAR(50),
    bank_name VARCHAR(100),
    logo TEXT,
    status supplier_status DEFAULT 'active'
);

CREATE TABLE Invoices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    supplier_id UUID REFERENCES Suppliers(id),
    user_id UUID REFERENCES Users(id),
    file_name TEXT,
    file_size INTEGER,
    file_type VARCHAR(50),
    ocr_raw_text TEXT,
    invoice_url TEXT,
    invoice_code VARCHAR(100),
    invoice_date DATE,
    currency VARCHAR(10) DEFAULT 'AUD',
    sub_total NUMERIC(15, 2), -- Total before tax
    total_tax NUMERIC(15, 2), -- GST in Australia
    total_amount NUMERIC(15, 2), -- Total after tax
    payment_status payment_status DEFAULT 'unpaid',
    invoice_status invoice_status DEFAULT 'pending',
    error_message TEXT
);

CREATE TABLE Categories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    parent_id UUID REFERENCES Categories(id),
    category_name VARCHAR(255) NOT NULL,
    description TEXT
);

CREATE TABLE Units (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    unit_name VARCHAR(50) NOT NULL,
    unit_symbol VARCHAR(10)
);

CREATE TABLE Products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    category_id UUID REFERENCES Categories(id),
    base_unit_id UUID REFERENCES Units(id),
    sku_code VARCHAR(50) UNIQUE,
    barcode VARCHAR(100) UNIQUE,
    product_code VARCHAR(50) UNIQUE,
    product_name TEXT NOT NULL,
    image_url TEXT,
    description TEXT,
    brand VARCHAR(100),
    stock_quantity DECIMAL(15, 2) DEFAULT 0,
    sales_volume DECIMAL(15, 2) DEFAULT 0,
    reorder_level DECIMAL(15, 2),
    selling_price NUMERIC(15, 2),
    last_unit_price NUMERIC(15, 2),
    currency VARCHAR(10) DEFAULT 'AUD',
    status product_status DEFAULT 'in_stock',
    warehouse_location TEXT,
    is_batch_tracked BOOLEAN DEFAULT FALSE,
    batch_number VARCHAR(50),
    expiry_date DATE
);

CREATE TABLE Product_Unit_Conversions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES Products(id),
    unit_id UUID REFERENCES Units(id),
    factor DECIMAL(15, 4) NOT NULL
);

CREATE TABLE Invoice_Items (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    invoice_id UUID REFERENCES Invoices(id),
    product_id UUID REFERENCES Products(id),
    raw_product_name TEXT,
    quantity DECIMAL(15, 2),
    unit VARCHAR(50),
    unit_price NUMERIC(15, 2),
    line_total NUMERIC(15, 2),
    confidence_score DECIMAL(5, 2),
    has_gst BOOLEAN DEFAULT TRUE
);

CREATE TABLE Stock_Log (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES Products(id),
    invoice_id UUID REFERENCES Invoices(id),
    user_id UUID REFERENCES Users(id),
    transaction_type transaction_type NOT NULL,
    quantity_change DECIMAL(15, 2),
    balance_after DECIMAL(15, 2),
    timestamp TIMESTAMP DEFAULT NOW()
);