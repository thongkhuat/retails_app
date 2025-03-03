-- init_retail_db.sql
-- PostgreSQL script to initialize the retail database for Supabase

-- Drop existing tables if they exist (optional, for clean initialization)
DROP TABLE IF EXISTS order_details CASCADE;
DROP TABLE IF EXISTS orders CASCADE;
DROP TABLE IF EXISTS inventories CASCADE;
DROP TABLE IF EXISTS products CASCADE;
DROP TABLE IF EXISTS customers CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR UNIQUE NOT NULL,
    password VARCHAR NOT NULL,
    role VARCHAR,
    email VARCHAR NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE
);

-- Create Customers table
CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    first_name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    dob TIMESTAMP,
    last_purchase_order_id UUID,
    last_activity_time TIMESTAMP DEFAULT NOW(),
    address VARCHAR,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL
);

-- Create Products table
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR NOT NULL,
    type VARCHAR NOT NULL,
    created_date TIMESTAMP NOT NULL,
    retail_price FLOAT NOT NULL,
    remark VARCHAR
);
CREATE INDEX idx_products_type ON products(type);

-- Create Inventories table
CREATE TABLE inventories (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    product_id UUID NOT NULL REFERENCES products(id),
    qty INTEGER NOT NULL,
    type VARCHAR NOT NULL,
    source VARCHAR,
    destination VARCHAR,
    created_time TIMESTAMP NOT NULL,
    created_by VARCHAR NOT NULL,
    remark VARCHAR
);

-- Create Orders table
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_time TIMESTAMP NOT NULL,
    customer_id UUID NOT NULL REFERENCES customers(id),
    is_delivered BOOLEAN NOT NULL,
    note VARCHAR,
    delivered_time TIMESTAMP,
    total_retail_price FLOAT,
    total_real_price FLOAT
);

-- Create Order Details table
CREATE TABLE order_details (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID NOT NULL REFERENCES orders(id),
    product_id UUID NOT NULL REFERENCES products(id),
    qty INTEGER NOT NULL,
    discount FLOAT,
    retail_price FLOAT,
    real_price FLOAT
);

-- Insert initial superuser (admin)
-- Password '12345678' hashed with bcrypt (generated using a tool or Python script)
INSERT INTO users (id, username, password, role, email, is_active, is_superuser)
VALUES (
    gen_random_uuid(),
    'admin',
    '$2b$12$EMlATbtJvqTZxsRaYXvGPeV58VK3mcq7PrkNaxazjQjo4c/w8xGWe', -- Replace with actual bcrypt hash
    'admin',
    'admin@example.com',
    TRUE,
    TRUE
);

-- Create indexes for performance (optional, based on your search requirements)
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_customers_first_name ON customers(first_name);
CREATE INDEX idx_products_name ON products(name);