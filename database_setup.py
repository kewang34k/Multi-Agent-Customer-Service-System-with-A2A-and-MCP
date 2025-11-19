"""
Database Setup Script for Multi-Agent Customer Service System
Creates SQLite database with customers and tickets tables
Inserts test data for demonstrations
"""

import sqlite3
from datetime import datetime
import os

def create_database(db_path="customer_service.db"):
    """
    Create database with customers and tickets tables
    """
    # Remove existing database if present
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"✓ Removed existing database: {db_path}")

    # Create connection
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create customers table
    cursor.execute("""
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT,
            phone TEXT,
            status TEXT DEFAULT 'active' CHECK(status IN ('active', 'disabled')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("✓ Created customers table")

    # Create tickets table
    cursor.execute("""
        CREATE TABLE tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            issue TEXT NOT NULL,
            status TEXT DEFAULT 'open' CHECK(status IN ('open', 'in_progress', 'resolved')),
            priority TEXT DEFAULT 'medium' CHECK(priority IN ('low', 'medium', 'high')),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)
    print("✓ Created tickets table")

    # Insert test customers
    test_customers = [
        ("Alice Johnson", "alice.johnson@email.com", "+1-555-0101", "active"),
        ("Bob Martinez", "bob.martinez@company.com", "+1-555-0202", "active"),
        ("Carol White", "carol.white@mail.com", "+1-555-0303", "active"),
        ("David Brown", "david.b@enterprise.com", "+1-555-0404", "active"),
        ("Emma Davis", "emma.davis@startup.io", "+1-555-0505", "active"),
        ("Frank Wilson", "frank.w@inactive.com", "+1-555-0606", "disabled"),
        ("Grace Lee", "grace.lee@premium.com", "+1-555-0707", "active"),
        ("Henry Chen", "henry.chen@tech.com", "+1-555-0808", "active"),
        ("Iris Rodriguez", "iris.r@finance.com", "+1-555-0909", "active"),
        ("Jack Taylor", "jack.taylor@small.biz", "+1-555-1010", "active")
    ]

    cursor.executemany(
        "INSERT INTO customers (name, email, phone, status) VALUES (?, ?, ?, ?)",
        test_customers
    )
    print(f"✓ Inserted {len(test_customers)} test customers")

    # Insert test tickets
    test_tickets = [
        # Customer 1 (Alice) - Premium customer with multiple tickets
        (1, "Product not working as expected", "open", "high"),
        (1, "Need help with account settings", "in_progress", "medium"),
        (1, "Billing question about last invoice", "resolved", "low"),

        # Customer 2 (Bob) - Enterprise customer
        (2, "System integration issues", "open", "high"),
        (2, "API rate limit concerns", "in_progress", "high"),

        # Customer 3 (Carol) - Basic customer
        (3, "How do I reset my password?", "resolved", "low"),

        # Customer 4 (David) - Multiple open tickets
        (4, "Data export not working", "open", "high"),
        (4, "Feature request: bulk operations", "open", "medium"),
        (4, "Documentation unclear", "in_progress", "low"),

        # Customer 5 (Emma) - Recent user
        (5, "Getting started questions", "resolved", "low"),

        # Customer 7 (Grace) - Premium with urgent issue
        (7, "Critical: Service outage affecting business", "open", "high"),
        (7, "Need compensation for downtime", "open", "high"),

        # Customer 8 (Henry) - Technical issues
        (8, "Performance degradation", "in_progress", "medium"),

        # Customer 9 (Iris) - Billing concerns
        (9, "Double charged on subscription", "open", "high"),
        (9, "Need refund urgently", "open", "high"),

        # Customer 10 (Jack) - General support
        (10, "Product inquiry", "resolved", "low")
    ]

    cursor.executemany(
        "INSERT INTO tickets (customer_id, issue, status, priority) VALUES (?, ?, ?, ?)",
        test_tickets
    )
    print(f"✓ Inserted {len(test_tickets)} test tickets")

    # Commit and close
    conn.commit()
    conn.close()

    print(f"\n✓ Database created successfully: {db_path}")
    print_database_stats(db_path)

    return db_path

def print_database_stats(db_path="customer_service.db"):
    """
    Print database statistics
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Count customers by status
    cursor.execute("SELECT status, COUNT(*) FROM customers GROUP BY status")
    customer_stats = cursor.fetchall()

    # Count tickets by status
    cursor.execute("SELECT status, COUNT(*) FROM tickets GROUP BY status")
    ticket_stats = cursor.fetchall()

    # Count tickets by priority
    cursor.execute("SELECT priority, COUNT(*) FROM tickets GROUP BY priority")
    priority_stats = cursor.fetchall()

    print("\n" + "="*60)
    print("DATABASE STATISTICS")
    print("="*60)

    print("\nCustomers by Status:")
    for status, count in customer_stats:
        print(f"  {status}: {count}")

    print("\nTickets by Status:")
    for status, count in ticket_stats:
        print(f"  {status}: {count}")

    print("\nTickets by Priority:")
    for priority, count in priority_stats:
        print(f"  {priority}: {count}")

    conn.close()

def reset_database(db_path="customer_service.db"):
    """
    Reset database to initial state
    """
    print("\n🔄 Resetting database...")
    return create_database(db_path)

if __name__ == "__main__":
    # Create database with test data
    db_path = create_database()

    print("\n" + "="*60)
    print("Setup complete! Database ready for MCP server.")
    print("="*60)
