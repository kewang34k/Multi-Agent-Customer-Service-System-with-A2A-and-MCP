"""
MCP (Model Context Protocol) Server for Customer Service System

Implements 5 required tools:
1. get_customer(customer_id)
2. list_customers(status, limit)
3. update_customer(customer_id, data)
4. create_ticket(customer_id, issue, priority)
5. get_customer_history(customer_id)
"""

import sqlite3
from typing import Optional, List, Dict, Any
from datetime import datetime
import json

class MCPServer:
    """
    MCP Server for Customer Service Database Access
    Provides standardized tools for customer and ticket management
    """

    def __init__(self, db_path: str = "customer_service.db"):
        """
        Initialize MCP server with database connection

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._validate_database()
        print(f"✓ MCP Server initialized with database: {db_path}")

    def _validate_database(self):
        """Validate database exists and has required tables"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check for customers table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
            if not cursor.fetchone():
                raise Exception("customers table not found")

            # Check for tickets table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tickets'")
            if not cursor.fetchone():
                raise Exception("tickets table not found")

            conn.close()
        except Exception as e:
            raise Exception(f"Database validation failed: {e}")

    def _get_connection(self):
        """Get database connection"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        return conn

    def get_customer(self, customer_id: int) -> Optional[Dict[str, Any]]:
        """
        Tool 1: Get customer by ID

        Args:
            customer_id: Customer ID to retrieve

        Returns:
            Customer dict or None if not found
        """
        print(f"\n🔧 MCP Tool: get_customer(customer_id={customer_id})")

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT id, name, email, phone, status, created_at, updated_at
                FROM customers
                WHERE id = ?
            """, (customer_id,))

            row = cursor.fetchone()
            conn.close()

            if not row:
                print(f"   ❌ Customer {customer_id} not found")
                return None

            customer = dict(row)
            print(f"   ✓ Found: {customer['name']} ({customer['email']})")
            return customer

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

    def list_customers(self, status: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Tool 2: List customers with optional status filter

        Args:
            status: Filter by status ('active' or 'disabled'), None for all
            limit: Maximum number of results

        Returns:
            List of customer dicts
        """
        print(f"\n🔧 MCP Tool: list_customers(status={status}, limit={limit})")

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            if status:
                cursor.execute("""
                    SELECT id, name, email, phone, status, created_at, updated_at
                    FROM customers
                    WHERE status = ?
                    ORDER BY id
                    LIMIT ?
                """, (status, limit))
            else:
                cursor.execute("""
                    SELECT id, name, email, phone, status, created_at, updated_at
                    FROM customers
                    ORDER BY id
                    LIMIT ?
                """, (limit,))

            rows = cursor.fetchall()
            conn.close()

            customers = [dict(row) for row in rows]
            print(f"   ✓ Found {len(customers)} customers")

            return customers

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return []

    def update_customer(self, customer_id: int, data: Dict[str, Any]) -> bool:
        """
        Tool 3: Update customer information

        Args:
            customer_id: Customer ID to update
            data: Dict with fields to update (name, email, phone, status)

        Returns:
            True if successful, False otherwise
        """
        print(f"\n🔧 MCP Tool: update_customer(customer_id={customer_id}, data={data})")

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Build dynamic UPDATE query
            allowed_fields = ['name', 'email', 'phone', 'status']
            update_fields = []
            values = []

            for field, value in data.items():
                if field in allowed_fields:
                    update_fields.append(f"{field} = ?")
                    values.append(value)

            if not update_fields:
                print("   ⚠️  No valid fields to update")
                conn.close()
                return False

            # Add updated_at timestamp
            update_fields.append("updated_at = ?")
            values.append(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

            # Add customer_id for WHERE clause
            values.append(customer_id)

            query = f"""
                UPDATE customers
                SET {', '.join(update_fields)}
                WHERE id = ?
            """

            cursor.execute(query, values)
            conn.commit()

            if cursor.rowcount == 0:
                print(f"   ❌ Customer {customer_id} not found")
                conn.close()
                return False

            print(f"   ✓ Updated customer {customer_id}")
            conn.close()
            return True

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return False

    def create_ticket(self, customer_id: int, issue: str, priority: str = "medium") -> Optional[int]:
        """
        Tool 4: Create support ticket

        Args:
            customer_id: Customer ID
            issue: Issue description
            priority: Priority level ('low', 'medium', 'high')

        Returns:
            Ticket ID if successful, None otherwise
        """
        print(f"\n🔧 MCP Tool: create_ticket(customer_id={customer_id}, priority={priority})")
        print(f"   Issue: {issue[:50]}...")

        try:
            # Validate priority
            if priority not in ['low', 'medium', 'high']:
                print(f"   ❌ Invalid priority: {priority}")
                return None

            conn = self._get_connection()
            cursor = conn.cursor()

            # Check if customer exists
            cursor.execute("SELECT id FROM customers WHERE id = ?", (customer_id,))
            if not cursor.fetchone():
                print(f"   ❌ Customer {customer_id} not found")
                conn.close()
                return None

            # Create ticket
            cursor.execute("""
                INSERT INTO tickets (customer_id, issue, status, priority)
                VALUES (?, ?, 'open', ?)
            """, (customer_id, issue, priority))

            conn.commit()
            ticket_id = cursor.lastrowid

            print(f"   ✓ Created ticket #{ticket_id}")
            conn.close()
            return ticket_id

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

    def get_customer_history(self, customer_id: int) -> Dict[str, Any]:
        """
        Tool 5: Get customer history (profile + all tickets)

        Args:
            customer_id: Customer ID

        Returns:
            Dict with customer info and ticket history
        """
        print(f"\n🔧 MCP Tool: get_customer_history(customer_id={customer_id})")

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Get customer info
            cursor.execute("""
                SELECT id, name, email, phone, status, created_at, updated_at
                FROM customers
                WHERE id = ?
            """, (customer_id,))

            customer_row = cursor.fetchone()

            if not customer_row:
                print(f"   ❌ Customer {customer_id} not found")
                conn.close()
                return None

            customer = dict(customer_row)

            # Get all tickets for this customer
            cursor.execute("""
                SELECT id, issue, status, priority, created_at
                FROM tickets
                WHERE customer_id = ?
                ORDER BY created_at DESC
            """, (customer_id,))

            ticket_rows = cursor.fetchall()
            tickets = [dict(row) for row in ticket_rows]

            # Build history
            history = {
                "customer": customer,
                "tickets": tickets,
                "ticket_count": len(tickets),
                "open_tickets": len([t for t in tickets if t['status'] == 'open']),
                "high_priority_tickets": len([t for t in tickets if t['priority'] == 'high'])
            }

            print(f"   ✓ Found customer: {customer['name']}")
            print(f"   ✓ Total tickets: {len(tickets)}")
            print(f"   ✓ Open tickets: {history['open_tickets']}")

            conn.close()
            return history

        except Exception as e:
            print(f"   ❌ Error: {e}")
            return None

    # Additional helper methods

    def get_tickets_by_criteria(self, status: Optional[str] = None,
                                 priority: Optional[str] = None,
                                 customer_ids: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """
        Get tickets by various criteria (helper for complex queries)
        """
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            query = "SELECT * FROM tickets WHERE 1=1"
            params = []

            if status:
                query += " AND status = ?"
                params.append(status)

            if priority:
                query += " AND priority = ?"
                params.append(priority)

            if customer_ids:
                placeholders = ','.join(['?'] * len(customer_ids))
                query += f" AND customer_id IN ({placeholders})"
                params.extend(customer_ids)

            query += " ORDER BY created_at DESC"

            cursor.execute(query, params)
            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]

        except Exception as e:
            print(f"Error getting tickets: {e}")
            return []

    def get_server_stats(self) -> Dict[str, Any]:
        """Get server statistics"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            # Customer stats
            cursor.execute("SELECT COUNT(*) as total FROM customers WHERE status='active'")
            active_customers = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM customers WHERE status='disabled'")
            disabled_customers = cursor.fetchone()['total']

            # Ticket stats
            cursor.execute("SELECT COUNT(*) as total FROM tickets WHERE status='open'")
            open_tickets = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM tickets WHERE status='in_progress'")
            in_progress_tickets = cursor.fetchone()['total']

            cursor.execute("SELECT COUNT(*) as total FROM tickets WHERE priority='high'")
            high_priority_tickets = cursor.fetchone()['total']

            conn.close()

            return {
                "active_customers": active_customers,
                "disabled_customers": disabled_customers,
                "open_tickets": open_tickets,
                "in_progress_tickets": in_progress_tickets,
                "high_priority_tickets": high_priority_tickets
            }

        except Exception as e:
            print(f"Error getting stats: {e}")
            return {}


# Test the MCP Server
if __name__ == "__main__":
    print("="*60)
    print("MCP SERVER TEST")
    print("="*60)

    # Initialize server
    mcp = MCPServer()

    # Test Tool 1: get_customer
    print("\n" + "="*60)
    print("TEST 1: get_customer()")
    print("="*60)
    customer = mcp.get_customer(1)
    if customer:
        print(json.dumps(customer, indent=2))

    # Test Tool 2: list_customers
    print("\n" + "="*60)
    print("TEST 2: list_customers()")
    print("="*60)
    customers = mcp.list_customers(status="active", limit=3)
    for c in customers:
        print(f"  - {c['name']} ({c['email']})")

    # Test Tool 3: update_customer
    print("\n" + "="*60)
    print("TEST 3: update_customer()")
    print("="*60)
    success = mcp.update_customer(1, {"email": "alice.updated@email.com"})
    print(f"Update result: {success}")

    # Test Tool 4: create_ticket
    print("\n" + "="*60)
    print("TEST 4: create_ticket()")
    print("="*60)
    ticket_id = mcp.create_ticket(1, "Test ticket from MCP server", "low")
    print(f"Created ticket ID: {ticket_id}")

    # Test Tool 5: get_customer_history
    print("\n" + "="*60)
    print("TEST 5: get_customer_history()")
    print("="*60)
    history = mcp.get_customer_history(1)
    if history:
        print(f"Customer: {history['customer']['name']}")
        print(f"Total tickets: {history['ticket_count']}")
        print(f"Open tickets: {history['open_tickets']}")

    # Server stats
    print("\n" + "="*60)
    print("SERVER STATISTICS")
    print("="*60)
    stats = mcp.get_server_stats()
    print(json.dumps(stats, indent=2))
