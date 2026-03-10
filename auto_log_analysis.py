#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===============================================================================
🚀 ENTERPRISE LOG ANOMALY DETECTION PIPELINE v4.0
===============================================================================
Eine deutsch-koreanische Gemeinschaftsproduktion

🇩🇪 German Engineering:   Robuste Pipeline, ISO-konform, dokumentiert
🇰🇷 Korean Innovation:    Echtzeit-Analyse, KI-gestützt, zukunftsweisend

Features:
▶ Automatisierte Log-Generierung & Rotation
▶ PyCaret Anomalie-Erkennung mit 5+ Algorithmen
▶ Echtzeit-Monitoring mit Alarming
▶ MLflow Integration für Modell-Tracking
▶ Export-Funktionen für Reports
▶ Multi-Format Support (CSV, JSON, Parquet)
▶ Dashboard-Integration
===============================================================================
"""

import os
import sys
import json
import hashlib
import logging
import warnings
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, List, Tuple, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import confusion_matrix, classification_report

# PyCaret Imports
from pycaret.anomaly import *
from pycaret.internal.pycaret_experiment import TimeSeriesExperiment

# MLflow für Modell-Tracking
import mlflow
import mlflow.sklearn

# Weitere Utilities
import joblib
import yaml
from tqdm import tqdm
import schedule
import time

warnings.filterwarnings('ignore')

# =============================================================================
# KONFIGURATION – Deutsche Präzision
# =============================================================================

class Config:
    """Zentrale Konfigurationsklasse – Einmal definiert, perfekt für immer"""
    
    # Verzeichnisstruktur
    BASE_DIR = Path(os.path.expanduser("~"))
    LOG_DIR = BASE_DIR / "logs"
    LOG_FILE = LOG_DIR / "enterprise_test.log"
    CSV_FILE = Path("enterprise_log_data.csv")
    MODEL_DIR = Path("models")
    REPORT_DIR = Path("reports")
    MLFLOW_DIR = Path("mlruns")
    
    # Logging-Konfiguration
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
    
    # PyCaret Konfiguration
    ANOMALY_ALGORITHMS = {
        'iforest': 'Isolation Forest',
        'knn': 'K-Nearest Neighbors',
        'cluster': 'Clustering Based',
        'pca': 'Principal Component Analysis',
        'mcd': 'Minimum Covariance Determinant',
        'svm': 'One-Class SVM',
        'abod': 'Angle-Based Outlier Detection',
        'cbod': 'Cluster-Based Outlier Detection',
        'feature_bagging': 'Feature Bagging',
        'histogram': 'Histogram-Based Outlier Detection',
        'lof': 'Local Outlier Factor',
        'cof': 'Connectivity-Based Outlier Factor'
    }
    
    DEFAULT_ALGORITHM = 'iforest'
    RANDOM_SEED = 42
    ANOMALY_THRESHOLD = 0.1  # 10% Anomalie-Erwartung
    
    # Alert-Konfiguration
    ALERT_THRESHOLDS = {
        'low': 0.05,      # 5% Anomalien
        'medium': 0.10,    # 10% Anomalien
        'high': 0.20,      # 20% Anomalien
        'critical': 0.30   # 30%+ Anomalien
    }
    
    # Feature Engineering
    TIME_FEATURES = ['hour', 'day_of_week', 'day_of_month', 'month', 'is_weekend', 'is_business_hours']
    TEXT_FEATURES = ['word_count', 'char_count', 'has_ip', 'has_email', 'has_path']

# =============================================================================
# LOGGING SYSTEM – Industrielles Monitoring
# =============================================================================

def setup_logging(name: str = "AnomalyDetection") -> logging.Logger:
    """Initialisiert das Logging-System nach ISO 9001 Standards"""
    
    logger = logging.getLogger(name)
    logger.setLevel(Config.LOG_LEVEL)
    
    # Konsolen-Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(Config.LOG_LEVEL)
    console_formatter = logging.Formatter(Config.LOG_FORMAT, Config.LOG_DATE_FORMAT)
    console_handler.setFormatter(console_formatter)
    
    # Datei-Handler
    log_file = Config.LOG_DIR / f"anomaly_detection_{datetime.now():%Y%m%d}.log"
    Config.LOG_DIR.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(Config.LOG_LEVEL)
    file_formatter = logging.Formatter(Config.LOG_FORMAT, Config.LOG_DATE_FORMAT)
    file_handler.setFormatter(file_formatter)
    
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    return logger

logger = setup_logging()

# =============================================================================
# ENHANCED LOG GENERATOR – Mit deutscher Gründlichkeit
# =============================================================================

class EnterpriseLogGenerator:
    """
    Erweiterter Log-Generator für Enterprise-Umgebungen
    Generiert realistische Logs mit verschiedenen Mustern
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Log-Templates für verschiedene Szenarien
        self.normal_patterns = [
            "User {user} login success from {ip}",
            "File {file} opened by user {user}",
            "Email sent from {user} to {recipient}",
            "Process {process} started with PID {pid}",
            "Database query executed by {user}",
            "API call {api} returned {status}",
            "Backup completed: {size}MB in {duration}s",
            "System health check: OK",
            "Network connection established to {server}:{port}",
            "Print job {job_id} completed for user {user}"
        ]
        
        self.anomaly_patterns = [
            "CRITICAL: Multiple failed logins for user {user} from {ip}",
            "WARNING: Data transfer exceeded threshold: {size}GB",
            "ALERT: Mass file deletion detected: {count} files",
            "SECURITY: Unauthorized access attempt to {file}",
            "ERROR: Buffer overflow detected in process {process}",
            "Suspicious: External data transfer user={user} size={size}GB to {country}",
            "WARNING: Anomalous process behavior: {process} CPU={cpu}%",
            "CRITICAL: Database connection pool exhausted",
            "ALERT: Privilege escalation detected for user {user}",
            "SECURITY: Malware signature detected in {file}"
        ]
        
        # Daten für realistische Logs
        self.users = ['ahyeon', 'admin', 'developer', 'analyst', 'manager', 
                      'system', 'guest', 'service', 'backup', 'audit']
        self.files = ['report.docx', 'data.xlsx', 'config.json', 'backup.zip',
                     'database.db', 'credentials.txt', 'passwords.xlsx']
        self.ips = ['192.168.1.{}'.format(i) for i in range(1, 255)]
        self.countries = ['DE', 'KR', 'US', 'JP', 'CN', 'GB', 'FR']
        
    def generate_timestamp(self, base_date: datetime, hours_back: int = 24) -> str:
        """Generiert realistische Zeitstempel"""
        random_hour = np.random.randint(0, 24)
        random_minute = np.random.randint(0, 60)
        random_second = np.random.randint(0, 60)
        
        timestamp = base_date - timedelta(hours=random_hour, 
                                         minutes=random_minute,
                                         seconds=random_second)
        return timestamp.strftime("%Y-%m-%d %H:%M:%S")
    
    def generate_log_line(self, is_anomaly: bool = False) -> str:
        """Generiert eine einzelne Log-Zeile"""
        
        timestamp = self.generate_timestamp(datetime.now())
        
        if is_anomaly:
            pattern = np.random.choice(self.anomaly_patterns)
        else:
            pattern = np.random.choice(self.normal_patterns)
        
        # Fülle Platzhalter mit realistischen Werten
        log_line = pattern.format(
            user=np.random.choice(self.users),
            ip=np.random.choice(self.ips),
            file=np.random.choice(self.files),
            recipient=f"{np.random.choice(self.users)}@company.com",
            process=np.random.choice(['chrome.exe', 'python.exe', 'sqlservr.exe']),
            pid=np.random.randint(1000, 9999),
            api=np.random.choice(['/api/data', '/api/auth', '/api/report']),
            status=np.random.choice(['200', '404', '500'], p=[0.9, 0.05, 0.05]),
            size=np.random.randint(1, 100),
            duration=np.random.randint(1, 300),
            server=f"server{np.random.randint(1,10)}",
            port=np.random.choice([80, 443, 3306, 5432]),
            job_id=np.random.randint(10000, 99999),
            count=np.random.randint(100, 1000),
            country=np.random.choice(self.countries),
            cpu=np.random.randint(50, 100)
        )
        
        return f"{timestamp} {log_line}"
    
    def generate_logs(self, num_lines: int = 1000, anomaly_rate: float = 0.05) -> List[str]:
        """
        Generiert einen realistischen Log-Dump
        
        Args:
            num_lines: Anzahl der Log-Zeilen
            anomaly_rate: Anteil der Anomalien (0-1)
        """
        self.logger.info(f"📝 Generiere {num_lines} Log-Zeilen mit {anomaly_rate*100:.1f}% Anomalien")
        
        logs = []
        num_anomalies = int(num_lines * anomaly_rate)
        
        for i in range(num_lines):
            is_anomaly = i < num_anomalies
            logs.append(self.generate_log_line(is_anomaly))
        
        # Mische die Logs
        np.random.shuffle(logs)
        
        self.logger.info(f"✅ {len(logs)} Log-Zeilen generiert")
        return logs

# =============================================================================
# FEATURE ENGINEERING – Intelligente Merkmalsextraktion
# =============================================================================

class FeatureEngineer:
    """
    Erweiterte Feature-Extraktion für Log-Analyse
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def extract_time_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extrahiert zeitbasierte Features"""
        
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['day_of_month'] = df['timestamp'].dt.day
        df['month'] = df['timestamp'].dt.month
        df['is_weekend'] = df['day_of_week'].isin([5, 6]).astype(int)
        df['is_business_hours'] = ((df['hour'] >= 9) & (df['hour'] <= 17) & 
                                   (df['is_weekend'] == 0)).astype(int)
        
        return df
    
    def extract_text_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extrahiert textbasierte Features"""
        
        df['word_count'] = df['message'].str.split().str.len()
        df['char_count'] = df['message'].str.len()
        df['has_ip'] = df['message'].str.contains(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}').astype(int)
        df['has_email'] = df['message'].str.contains(r'[\w\.-]+@[\w\.-]+\.\w+').astype(int)
        df['has_path'] = df['message'].str.contains(r'[a-zA-Z]:\\|/').astype(int)
        df['has_error'] = df['message'].str.contains('ERROR|CRITICAL|ALERT').astype(int)
        df['has_user'] = df['message'].str.contains('user=').astype(int)
        
        return df
    
    def extract_security_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Extrahiert sicherheitsrelevante Features"""
        
        # Benutzer-Aktivitätszähler
        user_activity = df['message'].str.extract(r'user[= ](\w+)')[0]
        df['user_activity_count'] = user_activity.map(user_activity.value_counts())
        
        # Dateizugriffs-Muster
        file_access = df['message'].str.contains('file|open|access').astype(int)
        df['is_file_access'] = file_access
        
        # Datentransfer-Erkennung
        data_transfer = df['message'].str.contains('transfer|size|GB|MB').astype(int)
        df['is_data_transfer'] = data_transfer
        
        # Zeit seit letztem Log
        df = df.sort_values('timestamp')
        df['time_to_next'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
        df['time_from_last'] = df['timestamp'].diff().dt.total_seconds().fillna(0)
        
        return df
    
    def engineer_all(self, df: pd.DataFrame) -> pd.DataFrame:
        """Führt alle Feature-Engineering-Schritte aus"""
        
        self.logger.info("🔧 Starte Feature-Engineering...")
        
        df = self.extract_time_features(df)
        df = self.extract_text_features(df)
        df = self.extract_security_features(df)
        
        self.logger.info(f"✅ {len(df.columns)} Features generiert")
        return df

# =============================================================================
# PYCARET ANOMALY DETECTION – Das Herzstück
# =============================================================================

class PyCaretAnomalyDetector:
    """
    Erweiterte Anomalie-Erkennung mit PyCaret
    """
    
    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(__name__)
        self.model = None
        self.experiment = None
        self.results = None
        
    def prepare_data(self, df: pd.DataFrame, target_col: str = None) -> pd.DataFrame:
        """
        Bereitet Daten für PyCaret vor
        """
        
        # Feature-Engineering
        engineer = FeatureEngineer()
        df = engineer.engineer_all(df)
        
        # Entferne nicht-numerische Spalten für PyCaret
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # Füge Zielspalte hinzu falls vorhanden
        if target_col and target_col in df.columns:
            numeric_cols.append(target_col)
        
        return df[numeric_cols]
    
    def train(self, df: pd.DataFrame, algorithm: str = Config.DEFAULT_ALGORITHM):
        """
        Trainiert das Anomalie-Erkennungsmodell
        """
        
        self.logger.info(f"🚀 Starte Training mit {algorithm}...")
        
        # MLflow Tracking
        mlflow.set_experiment(f"Anomaly_Detection_{algorithm}")
        
        with mlflow.start_run():
            # Log parameters
            mlflow.log_param("algorithm", algorithm)
            mlflow.log_param("data_shape", df.shape)
            mlflow.log_param("random_seed", Config.RANDOM_SEED)
            
            # PyCaret Setup
            self.experiment = setup(
                data=df,
                session_id=Config.RANDOM_SEED,
                silent=True,
                verbose=False,
                log_experiment=True,
                experiment_name=f"Anomaly_Detection_{algorithm}"
            )
            
            # Modell erstellen
            self.model = create_model(algorithm, fraction=Config.ANOMALY_THRESHOLD)
            
            # Ergebnisse zuweisen
            self.results = assign_model(self.model)
            
            # Log metrics
            anomaly_count = (self.results['Anomaly'] == 1).sum()
            anomaly_rate = anomaly_count / len(self.results)
            
            mlflow.log_metric("anomaly_count", anomaly_count)
            mlflow.log_metric("anomaly_rate", anomaly_rate)
            mlflow.log_metric("total_samples", len(self.results))
            
            # Feature Importance (falls verfügbar)
            if hasattr(self.model, 'feature_importances_'):
                for i, imp in enumerate(self.model.feature_importances_):
                    mlflow.log_metric(f"feature_{i}_importance", imp)
            
            self.logger.info(f"✅ Training abgeschlossen. Anomalie-Rate: {anomaly_rate:.2%}")
        
        return self.results
    
    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Sagt Anomalien für neue Daten vorher
        """
        
        if self.model is None:
            raise ValueError("❌ Modell wurde nicht trainiert!")
        
        self.logger.info("🔮 Starte Vorhersage...")
        
        predictions = predict_model(self.model, data=df)
        
        self.logger.info(f"✅ Vorhersage abgeschlossen")
        return predictions
    
    def save_model(self, path: Path = Config.MODEL_DIR / "pycaret_model"):
        """Speichert das trainierte Modell"""
        
        path.parent.mkdir(parents=True, exist_ok=True)
        save_model(self.model, str(path))
        self.logger.info(f"💾 Modell gespeichert: {path}")
    
    def load_model(self, path: Path):
        """Lädt ein trainiertes Modell"""
        
        self.model = load_model(str(path))
        self.logger.info(f"📂 Modell geladen: {path}")

# =============================================================================
# ENSEMBLE DETECTOR – Mehrere Algorithmen kombinieren
# =============================================================================

class EnsembleAnomalyDetector:
    """
    Ensemble-Methode für robustere Anomalie-Erkennung
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.detectors = {}
        self.weights = {}
        
    def add_detector(self, name: str, detector: PyCaretAnomalyDetector, weight: float = 1.0):
        """Fügt einen Detektor zum Ensemble hinzu"""
        
        self.detectors[name] = detector
        self.weights[name] = weight
        self.logger.info(f"➕ Detektor hinzugefügt: {name} (Gewicht: {weight})")
    
    def train_all(self, df: pd.DataFrame):
        """Trainiert alle Detektoren im Ensemble"""
        
        for name, detector in self.detectors.items():
            self.logger.info(f"🎯 Trainiere {name}...")
            detector.train(df)
    
    def predict_ensemble(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Ensemble-Vorhersage mit Weighted Voting
        """
        
        predictions = pd.DataFrame()
        predictions['timestamp'] = df['timestamp']
        predictions['message'] = df['message']
        
        # Sammle alle Vorhersagen
        for name, detector in self.detectors.items():
            pred = detector.predict(df)
            predictions[f'{name}_anomaly'] = pred['Anomaly']
            predictions[f'{name}_score'] = pred['Anomaly_Score']
        
        # Weighted Voting
        anomaly_cols = [f'{name}_anomaly' for name in self.detectors.keys()]
        score_cols = [f'{name}_score' for name in self.detectors.keys()]
        
        # Gewichtete Anomalie-Entscheidung
        weighted_sum = sum(predictions[col] * self.weights[name] 
                          for name, col in zip(self.detectors.keys(), anomaly_cols))
        total_weight = sum(self.weights.values())
        
        predictions['Ensemble_Anomaly'] = (weighted_sum / total_weight >= 0.5).astype(int)
        predictions['Ensemble_Score'] = sum(predictions[col] * self.weights[name] 
                                           for name, col in zip(self.detectors.keys(), score_cols)) / total_weight
        
        self.logger.info(f"🎯 Ensemble-Vorhersage abgeschlossen")
        return predictions

# =============================================================================
# VISUALIZATION ENGINE – Koreanische Ästhetik
# =============================================================================

class VisualizationEngine:
    """
    Erweiterte Visualisierungen für Anomalie-Analyse
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
        # Koreanisches Farbschema
        self.colors = {
            'normal': '#2ecc71',      # Smaragdgrün
            'anomaly': '#e74c3c',      # Signalrot
            'background': '#f8f9fa',   # Hellgrau
            'grid': '#dee2e6',          # Mittelgrau
            'text': '#212529'           # Dunkelgrau
        }
    
    def plot_anomaly_timeline(self, df: pd.DataFrame, save_path: Optional[Path] = None):
        """Erstellt eine Zeitachsen-Visualisierung"""
        
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        
        # Plot 1: Anomalie-Score über Zeit
        ax1 = axes[0]
        normal = df[df['Anomaly'] == 0]
        anomaly = df[df['Anomaly'] == 1]
        
        ax1.scatter(normal['timestamp'], normal['Anomaly_Score'], 
                   c=self.colors['normal'], alpha=0.5, label='Normal', s=20)
        ax1.scatter(anomaly['timestamp'], anomaly['Anomaly_Score'], 
                   c=self.colors['anomaly'], alpha=0.8, label='Anomalie', s=50, marker='X')
        ax1.set_xlabel('Zeit', fontsize=12)
        ax1.set_ylabel('Anomalie-Score', fontsize=12)
        ax1.set_title('Anomalie-Score über Zeit', fontsize=14, fontweight='bold')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Verteilung der Scores
        ax2 = axes[1]
        ax2.hist([normal['Anomaly_Score'], anomaly['Anomaly_Score']], 
                bins=30, label=['Normal', 'Anomalie'], 
                color=[self.colors['normal'], self.colors['anomaly']], 
                alpha=0.7, stacked=True)
        ax2.set_xlabel('Anomalie-Score', fontsize=12)
        ax2.set_ylabel('Häufigkeit', fontsize=12)
        ax2.set_title('Verteilung der Anomalie-Scores', fontsize=14, fontweight='bold')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Heatmap nach Stunde
        ax3 = axes[2]
        pivot = df.pivot_table(
            values='Anomaly_Score',
            index='hour',
            columns='day_of_week',
            aggfunc='mean'
        )
        im = ax3.imshow(pivot, cmap='YlOrRd', aspect='auto')
        ax3.set_xticks(range(len(pivot.columns)))
        ax3.set_xticklabels(['Mo', 'Di', 'Mi', 'Do', 'Fr', 'Sa', 'So'])
        ax3.set_yticks(range(len(pivot.index)))
        ax3.set_yticklabels([f'{h:02d}:00' for h in pivot.index])
        ax3.set_xlabel('Wochentag', fontsize=12)
        ax3.set_ylabel('Stunde', fontsize=12)
        ax3.set_title('Anomalie-Heatmap (Zeit vs. Wochentag)', fontsize=14, fontweight='bold')
        plt.colorbar(im, ax=ax3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"📊 Visualisierung gespeichert: {save_path}")
        
        plt.show()
    
    def plot_risk_dashboard(self, df: pd.DataFrame, save_path: Optional[Path] = None):
        """Erstellt ein Risk-Dashboard"""
        
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        
        # Risk Gauge
        ax1 = axes[0, 0]
        current_risk = df['Anomaly_Score'].mean()
        ax1.pie([current_risk, 100-current_risk], 
                colors=[self.colors['anomaly'], self.colors['normal']],
                labels=[f'Risk {current_risk:.1f}%', f'Safe {100-current_risk:.1f}%'],
                autopct='%1.1f%%',
                startangle=90)
        ax1.set_title('Aktuelles Risiko', fontsize=14, fontweight='bold')
        
        # Top Anomalies
        ax2 = axes[0, 1]
        top_anomalies = df[df['Anomaly'] == 1].nlargest(10, 'Anomaly_Score')
        ax2.barh(range(len(top_anomalies)), top_anomalies['Anomaly_Score'], 
                color=self.colors['anomaly'])
        ax2.set_yticks(range(len(top_anomalies)))
        ax2.set_yticklabels(top_anomalies['message'].str[:30])
        ax2.set_xlabel('Anomalie-Score')
        ax2.set_title('Top 10 Anomalien', fontsize=14, fontweight='bold')
        
        # Hourly Distribution
        ax3 = axes[1, 0]
        hourly_anomalies = df[df['Anomaly'] == 1].groupby('hour').size()
        hourly_normal = df[df['Anomaly'] == 0].groupby('hour').size()
        
        ax3.bar(hourly_normal.index, hourly_normal.values, 
               label='Normal', color=self.colors['normal'], alpha=0.7)
        ax3.bar(hourly_anomalies.index, hourly_anomalies.values, 
               label='Anomalie', color=self.colors['anomaly'], alpha=0.7, bottom=hourly_normal)
        ax3.set_xlabel('Stunde')
        ax3.set_ylabel('Anzahl')
        ax3.set_title('Stündliche Verteilung', fontsize=14, fontweight='bold')
        ax3.legend()
        
        # Feature Importance
        ax4 = axes[1, 1]
        feature_cols = [col for col in df.columns if col not in ['timestamp', 'message', 'Anomaly']]
        correlations = df[feature_cols + ['Anomaly']].corr()['Anomaly'].drop('Anomaly').sort_values()
        
        top_features = correlations.tail(10)
        ax4.barh(range(len(top_features)), top_features.values, color='#3498db')
        ax4.set_yticks(range(len(top_features)))
        ax4.set_yticklabels(top_features.index)
        ax4.set_xlabel('Korrelation mit Anomalie')
        ax4.set_title('Top Feature-Korrelationen', fontsize=14, fontweight='bold')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            self.logger.info(f"📊 Dashboard gespeichert: {save_path}")
        
        plt.show()

# =============================================================================
# ALERTING SYSTEM – Echtzeit-Benachrichtigungen
# =============================================================================

class AlertSystem:
    """
    Erweitertes Alerting-System für kritische Anomalien
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.alert_history = []
        
    def check_alerts(self, df: pd.DataFrame) -> List[Dict]:
        """
        Überprüft auf kritische Anomalien und generiert Alerts
        """
        
        alerts = []
        
        # Gesamt-Anomalie-Rate
        anomaly_rate = (df['Anomaly'] == 1).mean()
        
        for level, threshold in Config.ALERT_THRESHOLDS.items():
            if anomaly_rate >= threshold:
                alert = {
                    'timestamp': datetime.now().isoformat(),
                    'level': level.upper(),
                    'message': f"Anomalie-Rate {anomaly_rate:.1%} überschreitet {level}-Threshold ({threshold:.1%})",
                    'anomaly_rate': anomaly_rate,
                    'threshold': threshold
                }
                alerts.append(alert)
                
                # Log Alert
                self.logger.warning(f"🚨 ALERT [{level.upper()}]: {alert['message']}")
        
        # Kritische Einzel-Anomalien
        critical_anomalies = df[df['Anomaly_Score'] > 90]
        for _, row in critical_anomalies.iterrows():
            alert = {
                'timestamp': row['timestamp'],
                'level': 'CRITICAL',
                'message': f"Kritische Anomalie: {row['message'][:100]}",
                'score': row['Anomaly_Score']
            }
            alerts.append(alert)
            self.logger.critical(f"💥 CRITICAL: {alert['message']} (Score: {row['Anomaly_Score']:.1f})")
        
        self.alert_history.extend(alerts)
        return alerts
    
    def generate_report(self, df: pd.DataFrame, alerts: List[Dict]) -> str:
        """
        Generiert einen detaillierten Report
        """
        
        report = []
        report.append("=" * 80)
        report.append("🚨 ANOMALIE-DETEKTIONSREPORT")
        report.append("=" * 80)
        report.append(f"Erstellt am: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Statistiken
        report.append("📊 STATISTIKEN")
        report.append("-" * 40)
        report.append(f"Gesamt Logs: {len(df)}")
        report.append(f"Anomalien: {(df['Anomaly'] == 1).sum()}")
        report.append(f"Anomalie-Rate: {(df['Anomaly'] == 1).mean():.2%}")
        report.append(f"Durchschnitts-Score: {df['Anomaly_Score'].mean():.2f}")
        report.append(f"Max Score: {df['Anomaly_Score'].max():.2f}")
        report.append("")
        
        # Alerts
        if alerts:
            report.append("🚨 ALERTS")
            report.append("-" * 40)
            for alert in alerts:
                report.append(f"[{alert['level']}] {alert['timestamp']}: {alert['message']}")
        else:
            report.append("✅ Keine Alerts ausgelöst")
        report.append("")
        
        # Top Anomalien
        report.append("🔥 TOP 10 ANOMALIEN")
        report.append("-" * 40)
        top_anomalies = df[df['Anomaly'] == 1].nlargest(10, 'Anomaly_Score')
        for i, (_, row) in enumerate(top_anomalies.iterrows(), 1):
            report.append(f"{i:2d}. Score {row['Anomaly_Score']:.1f}: {row['message'][:80]}")
        
        report.append("")
        report.append("=" * 80)
        
        return "\n".join(report)

# =============================================================================
# MAIN PIPELINE – Die Orchestrierung
# =============================================================================

class AnomalyDetectionPipeline:
    """
    Hauptpipeline für die gesamte Anomalie-Erkennung
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.generator = EnterpriseLogGenerator()
        self.detector = PyCaretAnomalyDetector()
        self.ensemble = EnsembleAnomalyDetector()
        self.viz = VisualizationEngine()
        self.alerter = AlertSystem()
        
        # Erstelle Verzeichnisse
        Config.MODEL_DIR.mkdir(parents=True, exist_ok=True)
        Config.REPORT_DIR.mkdir(parents=True, exist_ok=True)
        
    def run_full_pipeline(self, 
                          num_logs: int = 10000,
                          anomaly_rate: float = 0.05,
                          algorithm: str = Config.DEFAULT_ALGORITHM):
        """
        Führt die komplette Pipeline aus
        """
        
        self.logger.info("=" * 80)
        self.logger.info("🚀 STARTE ENTERPRISE ANOMALIE-DETEKTIONS-PIPELINE")
        self.logger.info("=" * 80)
        
        # Step 1: Logs generieren
        self.logger.info("\n📝 STEP 1: Log-Generierung")
        logs = self.generator.generate_logs(num_logs, anomaly_rate)
        
        # Step 2: Logs speichern
        with open(Config.LOG_FILE, 'w') as f:
            f.write('\n'.join(logs))
        self.logger.info(f"💾 Logs gespeichert: {Config.LOG_FILE}")
        
        # Step 3: CSV konvertieren
        self.logger.info("\n🔄 STEP 2: CSV-Konvertierung")
        df = pd.DataFrame({
            "timestamp": [log[:19] for log in logs],
            "message": [log[20:] for log in logs]
        })
        df.to_csv(Config.CSV_FILE, index=False)
        self.logger.info(f"💾 CSV gespeichert: {Config.CSV_FILE}")
        
        # Step 4: Feature Engineering
        self.logger.info("\n🔧 STEP 3: Feature Engineering")
        engineer = FeatureEngineer()
        df_features = engineer.engineer_all(df)
        
        # Step 5: PyCaret Setup
        self.logger.info("\n🚀 STEP 4: PyCaret Anomalie-Erkennung")
        prepared_df = self.detector.prepare_data(df_features)
        results = self.detector.train(prepared_df, algorithm)
        
        # Step 6: Ensemble Training (optional)
        self.logger.info("\n🤝 STEP 5: Ensemble-Training")
        for alg in ['iforest', 'knn', 'pca'][:3]:  # Nur 3 für Performance
            det = PyCaretAnomalyDetector()
            det.train(prepared_df, alg)
            self.ensemble.add_detector(alg, det, weight=1.0)
        
        # Step 7: Ergebnisse kombinieren
        df_with_results = df_features.copy()
        df_with_results['Anomaly'] = results['Anomaly']
        df_with_results['Anomaly_Score'] = results['Anomaly_Score']
        
        # Step 8: Alert-Check
        self.logger.info("\n🚨 STEP 6: Alert-Überprüfung")
        alerts = self.alerter.check_alerts(df_with_results)
        
        # Step 9: Report generieren
        self.logger.info("\n📊 STEP 7: Report-G