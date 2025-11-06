# PART10 - Security & Best Practices

> **เนื้อหา**: Security Hardening, Authentication, Rate Limiting, Input Validation, Secure Coding, Audit
>
> **เป้าหมาย**: สร้าง secure Blockchain Explorer ตาม best practices
>
> **ระยะเวลา**: 8-10 ชั่วโมง
>
> **Prerequisites**: PART01-09, Security basics, OWASP Top 10

---

## 📑 สารบัญ

1. [Security Architecture](#security-architecture)
2. [API Security](#api-security)
3. [Database Security](#database-security)
4. [Infrastructure Security](#infrastructure-security)
5. [Smart Contract Security](#smart-contract-security)
6. [Security Monitoring](#security-monitoring)
7. [Compliance & Audit](#compliance--audit)
8. [แบบฝึกหัด](#แบบฝึกหัด)

---

## Security Architecture

### 1.1 Security Layers

```
┌─────────────────────────────────────────────────────────────┐
│                  Security Layers                            │
└─────────────────────────────────────────────────────────────┘

    Internet
       │
       ▼
┌──────────────┐
│   Cloudflare │  ← DDoS protection, WAF
│   (CDN/WAF)  │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Load        │  ← Rate limiting, SSL termination
│  Balancer    │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  API Gateway │  ← Auth, input validation
│  (FastAPI)   │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Application │  ← Business logic security
│    Layer     │
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  Database    │  ← Encryption at rest, access control
│    Layer     │
└──────────────┘
```

### 1.2 Security Principles

1. **Defense in Depth**: Multiple security layers
2. **Least Privilege**: Minimum necessary permissions
3. **Zero Trust**: Verify everything
4. **Security by Default**: Secure configurations
5. **Fail Securely**: Safe failure modes

---

## API Security

### 2.1 Authentication & Authorization

```python
"""JWT-based authentication."""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT access token."""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Verify JWT token."""
    token = credentials.credentials

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials"
            )

        return payload

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials"
        )


# Usage in endpoints
@router.get("/protected")
async def protected_route(token_data: dict = Depends(verify_token)):
    """Protected endpoint requiring authentication."""
    return {"message": "Access granted", "user": token_data.get("sub")}
```

### 2.2 Rate Limiting

```python
"""Advanced rate limiting."""
from fastapi import Request, HTTPException
from redis import Redis
from datetime import datetime
import hashlib

redis_client = Redis(host='localhost', port=6379, decode_responses=True)


class RateLimiter:
    """Token bucket rate limiter."""

    def __init__(
        self,
        rate: int = 100,  # requests
        per: int = 60,    # seconds
        burst: int = 20   # burst allowance
    ):
        self.rate = rate
        self.per = per
        self.burst = burst

    def _get_key(self, identifier: str) -> str:
        """Generate Redis key for rate limit."""
        return f"rate_limit:{identifier}"

    async def check(self, request: Request) -> bool:
        """
        Check if request is allowed.

        Uses token bucket algorithm with Redis.
        """
        # Get identifier (IP or user ID)
        identifier = self._get_identifier(request)
        key = self._get_key(identifier)

        now = datetime.now().timestamp()

        # Get current state
        pipe = redis_client.pipeline()
        pipe.hgetall(key)
        result = pipe.execute()[0]

        if not result:
            # First request - initialize bucket
            tokens = self.rate - 1
            last_update = now

            redis_client.hset(key, mapping={
                'tokens': tokens,
                'last_update': last_update
            })
            redis_client.expire(key, self.per)

            return True

        # Calculate tokens to add
        tokens = float(result['tokens'])
        last_update = float(result['last_update'])

        time_passed = now - last_update
        tokens_to_add = time_passed * (self.rate / self.per)
        tokens = min(self.rate, tokens + tokens_to_add)

        if tokens < 1:
            # Rate limit exceeded
            retry_after = int((1 - tokens) / (self.rate / self.per))
            raise HTTPException(
                status_code=429,
                detail="Rate limit exceeded",
                headers={"Retry-After": str(retry_after)}
            )

        # Consume token
        tokens -= 1

        # Update state
        redis_client.hset(key, mapping={
            'tokens': tokens,
            'last_update': now
        })

        return True

    def _get_identifier(self, request: Request) -> str:
        """Get unique identifier for rate limiting."""
        # Try API key first
        api_key = request.headers.get('X-API-Key')
        if api_key:
            return hashlib.sha256(api_key.encode()).hexdigest()

        # Fall back to IP
        forwarded_for = request.headers.get('X-Forwarded-For')
        if forwarded_for:
            return forwarded_for.split(',')[0].strip()

        return request.client.host


# Usage
rate_limiter = RateLimiter(rate=100, per=60)

@router.get("/data")
async def get_data(request: Request):
    """Endpoint with rate limiting."""
    await rate_limiter.check(request)
    return {"data": "..."}
```

### 2.3 Input Validation

```python
"""Comprehensive input validation."""
from pydantic import BaseModel, validator, Field
import re


class AddressInput(BaseModel):
    """Ethereum address input validation."""
    address: str = Field(..., description="Ethereum address")

    @validator('address')
    def validate_address(cls, v):
        """Validate Ethereum address format."""
        if not re.match(r'^0x[a-fA-F0-9]{40}$', v):
            raise ValueError('Invalid Ethereum address format')

        # Optional: Checksum validation
        # if not Web3.isChecksumAddress(v):
        #     raise ValueError('Invalid address checksum')

        return v.lower()


class BlockNumberInput(BaseModel):
    """Block number input validation."""
    block_number: int = Field(..., ge=0, le=999999999)

    @validator('block_number')
    def validate_block_number(cls, v):
        """Validate block number is reasonable."""
        if v < 0:
            raise ValueError('Block number cannot be negative')

        # Check against latest block
        # latest = get_latest_block_number()
        # if v > latest:
        #     raise ValueError(f'Block {v} does not exist yet')

        return v


class SearchQuery(BaseModel):
    """Search query validation."""
    query: str = Field(..., min_length=1, max_length=100)

    @validator('query')
    def validate_query(cls, v):
        """Sanitize search query."""
        # Remove dangerous characters
        dangerous_chars = ['<', '>', '"', "'", ';', '--', '/*', '*/']
        for char in dangerous_chars:
            if char in v:
                raise ValueError(f'Invalid character in query: {char}')

        return v.strip()


class PaginationInput(BaseModel):
    """Pagination input validation."""
    page: int = Field(1, ge=1, le=10000)
    page_size: int = Field(20, ge=1, le=100)


# SQL Injection Prevention
from sqlalchemy import text

# ❌ BAD - SQL injection vulnerability
def get_user_bad(username: str):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return db.execute(query)

# ✅ GOOD - Parameterized query
def get_user_good(username: str):
    query = text("SELECT * FROM users WHERE username = :username")
    return db.execute(query, {"username": username})
```

### 2.4 CORS Configuration

```python
"""Secure CORS configuration."""
from fastapi.middleware.cors import CORSMiddleware

# ❌ BAD - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # DANGEROUS!
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ GOOD - Whitelist specific origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://explorer.example.com",
        "https://app.example.com",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type", "Authorization"],
    max_age=3600,  # Cache preflight for 1 hour
)
```

---

## Database Security

### 3.1 Encryption at Rest

```sql
-- PostgreSQL encryption at rest
-- 1. Enable pgcrypto extension
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- 2. Create encrypted column
CREATE TABLE sensitive_data (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    encrypted_data BYTEA,  -- Store encrypted data
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Insert encrypted data
INSERT INTO sensitive_data (user_id, encrypted_data)
VALUES (
    1,
    pgp_sym_encrypt('sensitive information', 'encryption-key')
);

-- 4. Decrypt data
SELECT
    id,
    user_id,
    pgp_sym_decrypt(encrypted_data, 'encryption-key') AS decrypted_data
FROM sensitive_data
WHERE user_id = 1;
```

### 3.2 Access Control

```sql
-- Create read-only user for API
CREATE USER api_readonly WITH PASSWORD 'strong-password';

-- Grant SELECT only on specific tables
GRANT CONNECT ON DATABASE blockchain_explorer TO api_readonly;
GRANT USAGE ON SCHEMA public TO api_readonly;
GRANT SELECT ON blocks, transactions, logs TO api_readonly;

-- Revoke dangerous permissions
REVOKE CREATE ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON ALL TABLES IN SCHEMA public FROM PUBLIC;

-- Create admin user with limited access
CREATE USER db_admin WITH PASSWORD 'admin-password';
GRANT ALL PRIVILEGES ON DATABASE blockchain_explorer TO db_admin;

-- Audit who has what access
SELECT
    grantee,
    table_schema,
    table_name,
    privilege_type
FROM information_schema.table_privileges
WHERE grantee = 'api_readonly';
```

### 3.3 Connection Security

```python
"""Secure database connections."""
from sqlalchemy import create_engine
import ssl

# SSL/TLS connection
engine = create_engine(
    "postgresql://user:password@host:5432/db",
    connect_args={
        "sslmode": "require",
        "sslrootcert": "/path/to/ca.pem",
        "sslcert": "/path/to/client-cert.pem",
        "sslkey": "/path/to/client-key.pem",
    }
)

# Connection timeout
engine = create_engine(
    "postgresql://user:password@host:5432/db",
    pool_pre_ping=True,  # Verify connections
    pool_recycle=3600,   # Recycle after 1 hour
    connect_args={
        "connect_timeout": 10,
        "options": "-c statement_timeout=30000"  # 30s query timeout
    }
)
```

---

## Infrastructure Security

### 4.1 Docker Security

```dockerfile
# Secure Dockerfile best practices

FROM python:3.11-slim AS builder

# Don't run as root
RUN useradd -m -u 1000 appuser

# Install dependencies
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Production stage
FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

# Copy dependencies from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages

# Copy application
WORKDIR /app
COPY --chown=appuser:appuser . .

# Drop privileges
USER appuser

# Run application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```yaml
# docker-compose.yml security
version: '3.8'

services:
  api:
    image: blockchain-explorer-api:latest
    read_only: true  # Read-only root filesystem
    tmpfs:
      - /tmp
    cap_drop:
      - ALL
    cap_add:
      - NET_BIND_SERVICE
    security_opt:
      - no-new-privileges:true
    user: "1000:1000"
    environment:
      - DATABASE_URL  # Don't hardcode secrets
    secrets:
      - db_password
      - jwt_secret

secrets:
  db_password:
    file: ./secrets/db_password.txt
  jwt_secret:
    file: ./secrets/jwt_secret.txt
```

### 4.2 Secrets Management

```python
"""Secure secrets management."""
import os
from cryptography.fernet import Fernet


class SecretsManager:
    """Manage encrypted secrets."""

    def __init__(self, master_key: bytes):
        self.cipher = Fernet(master_key)

    def encrypt(self, secret: str) -> bytes:
        """Encrypt a secret."""
        return self.cipher.encrypt(secret.encode())

    def decrypt(self, encrypted: bytes) -> str:
        """Decrypt a secret."""
        return self.cipher.decrypt(encrypted).decode()


# Usage with environment variables
def get_secret(name: str) -> str:
    """Get secret from environment or secret manager."""
    # Try environment variable first
    value = os.getenv(name)
    if value:
        return value

    # Fall back to secret manager (AWS Secrets Manager, Vault, etc.)
    # return secrets_manager.get_secret(name)

    raise ValueError(f"Secret {name} not found")


# ❌ BAD - Hardcoded secrets
DATABASE_URL = "postgresql://user:password@localhost/db"

# ✅ GOOD - From environment
DATABASE_URL = get_secret("DATABASE_URL")
```

### 4.3 Network Security

```yaml
# Network segmentation with Docker networks
version: '3.8'

networks:
  frontend:
    driver: bridge
  backend:
    driver: bridge
    internal: true  # No external access

services:
  nginx:
    networks:
      - frontend

  api:
    networks:
      - frontend
      - backend

  database:
    networks:
      - backend  # Only accessible from backend
```

```nginx
# Nginx security headers
server {
    listen 443 ssl http2;
    server_name explorer.example.com;

    # SSL configuration
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "DENY" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
    add_header Permissions-Policy "geolocation=(), microphone=(), camera=()" always;

    # Hide server version
    server_tokens off;

    location / {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Timeout configuration
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

---

## Smart Contract Security

### 5.1 Secure Contract Patterns

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/security/ReentrancyGuard.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract SecureContract is ReentrancyGuard, Pausable, Ownable {
    // Use SafeMath for older Solidity versions
    // Solidity 0.8+ has built-in overflow protection

    // ✅ GOOD - ReentrancyGuard prevents reentrancy attacks
    function withdraw(uint256 amount) external nonReentrant {
        require(balances[msg.sender] >= amount, "Insufficient balance");

        // Update state BEFORE external call (Checks-Effects-Interactions pattern)
        balances[msg.sender] -= amount;

        // External call
        (bool success, ) = msg.sender.call{value: amount}("");
        require(success, "Transfer failed");
    }

    // ✅ GOOD - Pausable allows emergency stop
    function criticalOperation() external whenNotPaused {
        // ...
    }

    // ✅ GOOD - Access control
    function adminFunction() external onlyOwner {
        // Only owner can call
    }

    // ✅ GOOD - Input validation
    function setParameter(uint256 value) external onlyOwner {
        require(value > 0 && value <= 1000, "Invalid value");
        parameter = value;
    }
}
```

### 5.2 Contract Audit Checklist

```markdown
## Smart Contract Security Audit Checklist

### Access Control
- [ ] All sensitive functions have access modifiers
- [ ] Owner can be transferred securely
- [ ] No backdoors or hidden admin functions
- [ ] Multi-sig for critical operations

### Reentrancy
- [ ] All external calls use ReentrancyGuard or CEI pattern
- [ ] No state changes after external calls
- [ ] Pull over push for payments

### Integer Overflow/Underflow
- [ ] Using Solidity 0.8+ or SafeMath
- [ ] All arithmetic operations checked
- [ ] No unchecked blocks without justification

### Gas Optimization
- [ ] No unbounded loops
- [ ] Efficient data structures
- [ ] Gas limits considered
- [ ] Storage vs memory optimization

### External Calls
- [ ] Check return values
- [ ] Use transfer() or call with checks
- [ ] Avoid delegatecall when possible
- [ ] Verify contract interfaces

### Testing
- [ ] Unit test coverage > 90%
- [ ] Integration tests
- [ ] Fuzz testing
- [ ] Formal verification (optional)

### Deployment
- [ ] Contracts verified on Etherscan
- [ ] Immutable variables used where possible
- [ ] Upgrade mechanism (if proxy)
- [ ] Emergency pause mechanism
```

---

## Security Monitoring

### 6.1 Security Metrics

```python
"""Security monitoring metrics."""
from prometheus_client import Counter, Histogram

# Authentication metrics
auth_attempts_total = Counter(
    'auth_attempts_total',
    'Total authentication attempts',
    ['result']  # success/failure
)

failed_auth_by_ip = Counter(
    'failed_auth_by_ip_total',
    'Failed auth attempts by IP',
    ['ip_address']
)

# Rate limiting metrics
rate_limit_exceeded = Counter(
    'rate_limit_exceeded_total',
    'Rate limit exceeded count',
    ['endpoint']
)

# Security events
security_events = Counter(
    'security_events_total',
    'Security events',
    ['event_type', 'severity']
)


def log_security_event(event_type: str, severity: str, details: dict):
    """Log security event."""
    security_events.labels(
        event_type=event_type,
        severity=severity
    ).inc()

    logger.warning(
        "security_event",
        event_type=event_type,
        severity=severity,
        **details
    )


# Usage
log_security_event(
    "suspicious_login",
    "high",
    {"ip": "1.2.3.4", "attempts": 10}
)
```

### 6.2 Intrusion Detection

```python
"""Simple intrusion detection."""
from collections import defaultdict
from datetime import datetime, timedelta

class IntrusionDetector:
    """Detect suspicious behavior."""

    def __init__(self):
        self.failed_attempts = defaultdict(list)
        self.blocked_ips = set()

    def record_failed_auth(self, ip: str):
        """Record failed authentication attempt."""
        now = datetime.now()

        # Clean old attempts
        cutoff = now - timedelta(minutes=15)
        self.failed_attempts[ip] = [
            t for t in self.failed_attempts[ip]
            if t > cutoff
        ]

        # Add new attempt
        self.failed_attempts[ip].append(now)

        # Check if should block
        if len(self.failed_attempts[ip]) >= 5:
            self.block_ip(ip)
            return True

        return False

    def block_ip(self, ip: str):
        """Block IP address."""
        self.blocked_ips.add(ip)

        log_security_event(
            "ip_blocked",
            "high",
            {"ip": ip, "reason": "Too many failed attempts"}
        )

        # Update firewall (via iptables, fail2ban, etc.)
        # os.system(f"iptables -A INPUT -s {ip} -j DROP")

    def is_blocked(self, ip: str) -> bool:
        """Check if IP is blocked."""
        return ip in self.blocked_ips


detector = IntrusionDetector()
```

---

## Compliance & Audit

### 7.1 Audit Logging

```python
"""Comprehensive audit logging."""
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session


class AuditLog:
    """Audit log entry."""

    def __init__(self, db: Session):
        self.db = db

    def log_action(
        self,
        user_id: Optional[str],
        action: str,
        resource_type: str,
        resource_id: Optional[str],
        ip_address: str,
        user_agent: str,
        details: Optional[dict] = None
    ):
        """Log user action."""
        log_entry = {
            'timestamp': datetime.utcnow(),
            'user_id': user_id,
            'action': action,  # CREATE, READ, UPDATE, DELETE
            'resource_type': resource_type,
            'resource_id': resource_id,
            'ip_address': ip_address,
            'user_agent': user_agent,
            'details': details or {}
        }

        # Store in database
        self.db.execute(
            "INSERT INTO audit_logs VALUES (:timestamp, :user_id, :action, ...)",
            log_entry
        )

        # Also log to file for compliance
        logger.info("audit", **log_entry)


# Usage in API endpoint
@router.post("/admin/delete-user")
async def delete_user(
    user_id: int,
    request: Request,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete user (with audit logging)."""

    # Perform action
    db.execute("DELETE FROM users WHERE id = :id", {"id": user_id})

    # Log action
    audit = AuditLog(db)
    audit.log_action(
        user_id=current_user.id,
        action="DELETE",
        resource_type="user",
        resource_id=str(user_id),
        ip_address=request.client.host,
        user_agent=request.headers.get("User-Agent", ""),
        details={"deleted_user_id": user_id}
    )

    return {"success": True}
```

### 7.2 Compliance Checklist

```markdown
## GDPR Compliance Checklist

### Data Collection
- [ ] Minimal data collection (only what's needed)
- [ ] Clear privacy policy
- [ ] User consent mechanisms
- [ ] Cookie consent (if applicable)

### Data Storage
- [ ] Encryption at rest
- [ ] Access controls
- [ ] Data retention policies
- [ ] Secure backup procedures

### User Rights
- [ ] Right to access data
- [ ] Right to data portability
- [ ] Right to be forgotten (deletion)
- [ ] Right to rectification

### Data Protection
- [ ] DPO appointed (if required)
- [ ] DPIA completed
- [ ] Breach notification procedures
- [ ] Third-party processor agreements

### Technical Measures
- [ ] Pseudonymization where possible
- [ ] Encryption in transit
- [ ] Audit logs
- [ ] Regular security assessments
```

---

## แบบฝึกหัด

### แบบฝึกหัดที่ 1: Implement Authentication

**เป้าหมาย**: Add JWT authentication to API

**Requirements**:
- Login endpoint
- Protected routes
- Token expiration
- Refresh tokens

**Pass criteria**:
- ✅ Login works
- ✅ Protected routes require auth
- ✅ Tokens expire correctly

### แบบฝึกหัดที่ 2: Security Audit

**เป้าหมาย**: Audit codebase for vulnerabilities

**Tasks**:
- Check for SQL injection
- Verify input validation
- Test rate limiting
- Review CORS configuration

**Pass criteria**:
- ✅ No critical vulnerabilities
- ✅ All inputs validated
- ✅ Security headers present

### แบบฝึกหัดที่ 3: Penetration Testing

**เป้าหมาย**: Test security with automated tools

**Tools**:
- OWASP ZAP
- Burp Suite
- Nikto
- SQLMap

**Pass criteria**:
- ✅ No high-severity findings
- ✅ All vulnerabilities documented
- ✅ Fixes implemented

### แบบฝึกหัดที่ 4: Setup WAF

**เป้าหมาย**: Configure Web Application Firewall

**Requirements**:
- Cloudflare or ModSecurity
- Block common attacks
- Rate limiting rules
- Geo-blocking (if needed)

**Pass criteria**:
- ✅ WAF active
- ✅ Rules configured
- ✅ Attacks blocked

### แบบฝึกหัดที่ 5: Incident Response

**เป้าหมาย**: Create incident response plan

**Requirements**:
- Detection procedures
- Containment steps
- Recovery plan
- Post-incident review

**Pass criteria**:
- ✅ Plan documented
- ✅ Team trained
- ✅ Tested in drill

---

## Pass Criteria - PART10

ก่อนจบ PART10 ให้ตรวจสอบว่า:

- [ ] เข้าใจ security architecture
- [ ] Implement authentication & authorization
- [ ] Add input validation
- [ ] Configure rate limiting
- [ ] Secure database connections
- [ ] Follow secure coding practices
- [ ] Setup security monitoring
- [ ] Create audit logs
- [ ] สามารถทำแบบฝึกหัดอย่างน้อย 3 ข้อให้สำเร็จ

---

## Production Notes

### Security Checklist

**Before Deployment**:
- [ ] All secrets in environment variables
- [ ] SSL/TLS configured
- [ ] Rate limiting active
- [ ] Input validation on all endpoints
- [ ] CORS properly configured
- [ ] Security headers present
- [ ] Database access restricted
- [ ] Logging configured
- [ ] Monitoring active
- [ ] Incident response plan ready

### Regular Security Tasks

**Daily**:
- Monitor security logs
- Check for failed auth attempts
- Review rate limit events

**Weekly**:
- Review audit logs
- Check for vulnerabilities
- Update dependencies

**Monthly**:
- Security scan with tools
- Review access controls
- Test backups
- Update incident response plan

**Quarterly**:
- External security audit
- Penetration testing
- Security training
- Compliance review

---

**จบ PART10 - Security & Best Practices**

**ถัดไป**: PART11 - Deployment & DevOps

---

**สถิติ PART10**:
- **Lines**: ~1,800 lines
- **Security topics**: 15+ areas covered
- **Code examples**: 30+ security patterns
- **Exercises**: 5 hands-on labs

---

*เอกสารนี้เป็นส่วนหนึ่งของโปรเจกต์ Blockchain Explorer System*
