import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class DatabaseManager:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
    
    def get_connection(self):
        """Create and return a database connection"""
        try:
            conn = psycopg2.connect(self.database_url)
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    def save_patient_assessment(self, patient_data, prediction_data):
        """Save a patient assessment to the database"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            insert_query = """
                INSERT INTO patients (
                    patient_name, patient_id, age, sex, cp, trestbps, chol, 
                    fbs, restecg, thalachh, exang, oldpeak, slope, ca, thal,
                    risk_probability, risk_level
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING id
            """
            
            values = (
                patient_data['patient_name'],
                patient_data['patient_id'],
                patient_data['age'],
                patient_data['sex'],
                patient_data['cp'],
                patient_data['trestbps'],
                patient_data['chol'],
                patient_data['fbs'],
                patient_data['restecg'],
                patient_data['thalachh'],
                patient_data['exang'],
                patient_data['oldpeak'],
                patient_data['slope'],
                patient_data['ca'],
                patient_data['thal'],
                prediction_data['risk_probability'] * 100,  # Convert to percentage
                prediction_data['risk_level']
            )
            
            cursor.execute(insert_query, values)
            record_id = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Patient assessment saved successfully with ID: {record_id}")
            return True
            
        except Exception as e:
            print(f"Error saving patient assessment: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False
    
    def get_all_assessments(self):
        """Retrieve all patient assessments"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    id,
                    patient_name,
                    patient_id,
                    age,
                    CASE WHEN sex = 1 THEN 'Male' ELSE 'Female' END as sex,
                    risk_probability,
                    risk_level,
                    assessment_date
                FROM patients
                ORDER BY assessment_date DESC
            """
            
            cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"Error retrieving assessments: {e}")
            if conn:
                conn.close()
            return []
    
    def get_patient_by_id(self, patient_id):
        """Get detailed information for a specific patient"""
        conn = self.get_connection()
        if not conn:
            return None
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT *
                FROM patients
                WHERE patient_id = %s
                ORDER BY assessment_date DESC
                LIMIT 1
            """
            
            cursor.execute(query, (patient_id,))
            result = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return result
            
        except Exception as e:
            print(f"Error retrieving patient: {e}")
            if conn:
                conn.close()
            return None
    
    def search_patients(self, search_term):
        """Search patients by name or ID"""
        conn = self.get_connection()
        if not conn:
            return []
        
        try:
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT 
                    id,
                    patient_name,
                    patient_id,
                    age,
                    CASE WHEN sex = 1 THEN 'Male' ELSE 'Female' END as sex,
                    risk_probability,
                    risk_level,
                    assessment_date
                FROM patients
                WHERE 
                    LOWER(patient_name) LIKE LOWER(%s) OR
                    LOWER(patient_id) LIKE LOWER(%s)
                ORDER BY assessment_date DESC
            """
            
            search_pattern = f"%{search_term}%"
            cursor.execute(query, (search_pattern, search_pattern))
            results = cursor.fetchall()
            cursor.close()
            conn.close()
            
            return results
            
        except Exception as e:
            print(f"Error searching patients: {e}")
            if conn:
                conn.close()
            return []
    
    def delete_assessment(self, assessment_id):
        """Delete a specific assessment"""
        conn = self.get_connection()
        if not conn:
            return False
        
        try:
            cursor = conn.cursor()
            
            delete_query = "DELETE FROM patients WHERE id = %s"
            cursor.execute(delete_query, (assessment_id,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            print(f"Assessment {assessment_id} deleted successfully")
            return True
            
        except Exception as e:
            print(f"Error deleting assessment: {e}")
            if conn:
                conn.rollback()
                conn.close()
            return False

# Create a singleton instance
db_manager = DatabaseManager()