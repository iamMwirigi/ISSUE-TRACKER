-- Create 'users' table
CREATE TABLE users (
    id CHAR(36) PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    phone_number VARCHAR(20) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create 'offices' table
CREATE TABLE offices (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    location VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create 'services' table (renamed from projects)
CREATE TABLE services (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT,
    created_by CHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    office_id CHAR(36) REFERENCES offices(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create 'issues' table (updated schema)
CREATE TABLE issues (
    id CHAR(36) PRIMARY KEY,
    type VARCHAR(150) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'unsolved',
    priority VARCHAR(50) DEFAULT 'medium',
    reporter_id CHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    service_id CHAR(36) REFERENCES services(id) ON DELETE CASCADE,
    office_id CHAR(36) REFERENCES offices(id) ON DELETE SET NULL,
    assigned_to_id CHAR(36) REFERENCES users(id) ON DELETE SET NULL,
    attachments VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
