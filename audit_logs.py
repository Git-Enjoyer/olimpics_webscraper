


def log_entry(conn, operation_type, success, message):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO audit_log (operation_type, success, message)
            VALUES (%s, %s, %s)
            """, (operation_type, success, message))
        conn.commit()