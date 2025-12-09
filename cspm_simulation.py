# =============================================================================
# CSPM (CLOUD SECURITY POSTURE MANAGEMENT) - LIVE SIMULATION
# Environment: Production (AWS us-east-1 & Azure East US)
# Standards: NIST CSF v1.1, CIS Benchmark v1.4, PCI-DSS
# Dashboard Sync: Real-time
# =============================================================================

import time
import sys
import random
from datetime import datetime


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m' # Yellow (High Risk)
    FAIL = '\033[91m'    # Red (Critical)
    ENDC = '\033[0m'
    BOLD = '\033[1m'

RESOURCES = [
    # --- CRITICAL ISSUES 
    {"id": "s3:company-invoice-bucket", "type": "S3",  "check": "Block Public Access",        "status": "FAIL", "severity": "CRITICAL", "auto_fix": False},
    {"id": "rds:payment-db-prod",      "type": "RDS", "check": "Database Public Access",     "status": "FAIL", "severity": "CRITICAL", "auto_fix": False},
    {"id": "iam:root_account",          "type": "IAM", "check": "MFA Enabled for Root",       "status": "FAIL", "severity": "CRITICAL", "auto_fix": False},

    # --- HIGH RISKS (Some will be auto-fixed to show capability) ---
    {"id": "ec2:prod-bastion-host",     "type": "EC2", "check": "SSH Port 22 Closed (0.0.0.0)","status": "FAIL", "severity": "HIGH",     "auto_fix": True},
    {"id": "s3:customer-pii-raw",       "type": "S3",  "check": "Server-Side Encryption",     "status": "FAIL", "severity": "HIGH",     "auto_fix": True},
    {"id": "s3:legacy-app-data",        "type": "S3",  "check": "Bucket Versioning Enabled",  "status": "FAIL", "severity": "HIGH",     "auto_fix": False},

    # --- COMPLIANT ASSETS (Passing) ---
    {"id": "s3:app-logs-archive",       "type": "S3",  "check": "Encryption (SSE-S3)",        "status": "PASS", "severity": "INFO",     "auto_fix": False},
    {"id": "s3:static-frontend",        "type": "S3",  "check": "Read-Only Public Policy",    "status": "PASS", "severity": "INFO",     "auto_fix": False},
    {"id": "vpc:primary-prod",          "type": "VPC", "check": "Flow Logs Enabled",          "status": "PASS", "severity": "INFO",     "auto_fix": False},
    {"id": "iam:user:admin_01",         "type": "IAM", "check": "Access Key Rotation",        "status": "PASS", "severity": "INFO",     "auto_fix": False},
    {"id": "az:vm:frontend-01",         "type": "VM",  "check": "Network Watcher Enabled",    "status": "PASS", "severity": "INFO",     "auto_fix": False},
    {"id": "k8s:cluster-main",          "type": "EKS", "check": "Control Plane Logging",      "status": "PASS", "severity": "INFO",     "auto_fix": False},
]

# --- 2. HELPER FUNCTIONS ---

def print_slow(str):
    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.01)
    print()

def progress_bar(label):
    sys.stdout.write(f"{label:<30}")
    sys.stdout.flush()
    for i in range(20):
        time.sleep(random.uniform(0.02, 0.08))
        sys.stdout.write("█")
        sys.stdout.flush()
    sys.stdout.write(" 100%\n")

def scan_engine():
    # HEADER
    print(f"\n{Colors.HEADER}{Colors.BOLD}=== ENTERPRISE CSPM SCANNER v4.2 ==={Colors.ENDC}")
    print(f"Target: AWS (12 accounts) & Azure (4 subscriptions)")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)

    # CONNECTING PHASE
    print_slow(f"{Colors.CYAN}[INIT] Authenticating with Cloud Providers...{Colors.ENDC}")
    time.sleep(0.5)
    progress_bar("Fetching Asset Inventory")
    progress_bar("Syncing Compliance Policies")
    print(f"{Colors.GREEN}[READY] Inventory Loaded: 1,248 Total Assets found.{Colors.ENDC}")
    print("-" * 60)
    time.sleep(1)

    # SCANNING PHASE
    print(f"{'ASSET ID':<25} | {'SERVICE':<5} | {'CHECK':<30} | {'STATUS'}")
    print("-" * 75)

    fixed_count = 40 
    critical_open = 0

    for res in RESOURCES:
        time.sleep(0.2)
        
        status_txt = f"{Colors.GREEN}SECURE{Colors.ENDC}"
        if res['status'] == "FAIL":
            status_txt = f"{Colors.FAIL}FAIL ({res['severity']}){Colors.ENDC}"
        
        print(f"{res['id']:<25} | {res['type']:<5} | {res['check']:<30} | {status_txt}")

    
        if res['status'] == "FAIL":
            if res['auto_fix']:
                # Automation 
                time.sleep(0.3)
                print(f"   └── {Colors.WARNING}Risk Detected. Triggering Lambda Remediation...{Colors.ENDC}")
                time.sleep(0.8)
                print(f"   └── {Colors.GREEN}✅ FIXED: Configuration updated successfully.{Colors.ENDC}")
                fixed_count += 1
            else:
    
                time.sleep(0.2)
                print(f"   └── {Colors.FAIL}⛔ AUTO-REMEDIATION BLOCKED (Requires Manual Approval){Colors.ENDC}")
                print(f"   └── {Colors.CYAN}ℹ️  Ticket created: JIRA-{random.randint(4000,5000)}{Colors.ENDC}")
                if res['severity'] == "CRITICAL":
                    critical_open += 1

    # HIDDEN SCAN SIMULATION 
    print("...")
    time.sleep(0.5)
    print(f"{Colors.CYAN}[INFO] Scanning remaining 1,236 assets in background...{Colors.ENDC}")
    time.sleep(1.5)
    print("...")

    print("\n" + "=" * 60)
    print(f"{Colors.BOLD}   🛡️  SECURITY POSTURE DASHBOARD REPORT   🛡️{Colors.ENDC}")
    print("=" * 60)
    
    print(f"Total Assets Scanned:       {Colors.BOLD}1,248{Colors.ENDC}")
    print(f"Critical Vulnerabilities:   {Colors.FAIL}{critical_open} Open{Colors.ENDC} (Requires Action)")
    print(f"Auto-Remediated (7d):       {Colors.GREEN}{fixed_count} Fixed{Colors.ENDC}")
    print("-" * 60)
    
 
    print(f"COMPLIANCE SCORE:           {Colors.WARNING}{Colors.BOLD}78% (Needs Action){Colors.ENDC}")
    print("=" * 60)
    print(f"Data synced to Central Dashboard at {datetime.now().strftime('%H:%M')}")

if __name__ == "__main__":
    try:
        scan_engine()
    except KeyboardInterrupt:
        print("\nScan Aborted.")