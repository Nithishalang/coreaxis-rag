from src.database.mysql_connection import MySQLConnection
class ConversationRepository:
    def __init__(self):
        self.db = MySQLConnection()
    def create_conversation(
        self,
        user_id,
        title="New Conversation"
    ):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO conversations
        (user_id, title)
        VALUES (%s, %s)
        """
        cursor.execute(
            query,
            (user_id, title)
        )
        connection.commit()
        conversation_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return conversation_id
    
    def get_user_conversations(
        self,
        user_id
    ):
        connection = self.db.get_connection()
        cursor = connection.cursor(
            dictionary=True
        )
        query = """
        SELECT
            id,
            title,
            created_at,
            updated_at
        FROM conversations
        WHERE user_id = %s
        ORDER BY updated_at DESC
        """
        cursor.execute(
            query,
            (user_id,)
        )
        conversations = cursor.fetchall()
        cursor.close()
        connection.close()
        return conversations

    def get_conversation(
        self,
        conversation_id,
        user_id
    ):
        connection = self.db.get_connection()
        cursor = connection.cursor(
            dictionary=True
        )
        query = """
        SELECT
            id,
            user_id,
            title,
            created_at,
            updated_at
        FROM conversations
        WHERE id = %s
        AND user_id = %s
        """
        cursor.execute(
            query,
            (
                conversation_id,
                user_id
            )
        )
        conversation = cursor.fetchone()
        cursor.close()
        connection.close()
        return conversation
    
    def update_conversation_title(
        self,
        conversation_id,
        user_id,
        title
    ):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        query = """
        UPDATE conversations
        SET title = %s
        WHERE id = %s
        AND user_id = %s
        """
        cursor.execute(
            query,
            (
                title,
                conversation_id,
                user_id
            )
        )
        connection.commit()
        cursor.close()
        connection.close()

    def save_message(
        self,
        conversation_id,
        role,
        content,
        source=None
    ):
        connection = self.db.get_connection()
        cursor = connection.cursor()
        query = """
        INSERT INTO messages
        (
            conversation_id,
            role,
            content,
            source
        )
        VALUES
        (
            %s,
            %s,
            %s,
            %s
        )
        """
        cursor.execute(
            query,
            (
                conversation_id,
                role,
                content,
                source
            )
        )
        connection.commit()
        message_id = cursor.lastrowid
        cursor.close()
        connection.close()
        return message_id

    def get_messages(
        self,
        conversation_id
    ):
        connection = self.db.get_connection()
        cursor = connection.cursor(
            dictionary=True
        )
        query = """
        SELECT
            id,
            conversation_id,
            role,
            content,
            source,
            created_at
        FROM messages
        WHERE conversation_id = %s
        ORDER BY created_at ASC
        """
        cursor.execute(
            query,
            (conversation_id,)
        )
        messages = cursor.fetchall()
        cursor.close()
        connection.close()
        return messages