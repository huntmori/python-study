# ✅ 문제 해결 완료: MariaDB 접근 권한 문제

## 문제 원인

### 에러 메시지
```
Access denied for user 'fastapi_user'@'172.18.0.1' (using password: YES)
```

### 근본 원인
1. **.env 파일 설정 문제**: `root` 사용자 대신 `fastapi_user`를 사용해야 했습니다
2. **Docker 네트워크 IP**: 172.18.0.1은 Docker 브리지 네트워크의 호스트 IP입니다
3. **MariaDB 사용자 권한**: `fastapi_user`는 `%` (모든 호스트)에서 접근 가능하도록 설정되어 있습니다

## 해결 방법

### 1. ✅ .env 파일 수정 완료
```env
# 변경 전
DATABASE_URL=mysql+pymysql://root:rootpassword@localhost:3306/fastapi_db

# 변경 후  
DATABASE_URL=mysql+pymysql://fastapi_user:fastapi_password@localhost:3306/fastapi_db
```

### 2. ✅ docker-compose.yml 최적화 완료
```yaml
version: '3.8'

services:
  mariadb:
    image: mariadb:11.6
    container_name: fastapi_mariadb
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: fastapi_db
      MYSQL_USER: fastapi_user
      MYSQL_PASSWORD: fastapi_password
    ports:
      - "3306:3306"
    command:
      - --bind-address=0.0.0.0     # 모든 인터페이스에서 수신
      - --port=3306                 # 포트 명시
      - --skip-name-resolve         # DNS 조회 생략 (성능 향상)
    volumes:
      - mariadb_data:/var/lib/mysql

volumes:
  mariadb_data:
```

### 3. ✅ MariaDB 사용자 권한 설정 완료
```sql
CREATE USER IF NOT EXISTS 'fastapi_user'@'%' IDENTIFIED BY 'fastapi_password';
GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'%';
FLUSH PRIVILEGES;
```

## 현재 데이터베이스 사용자 상태

```
+--------------+-----------+
| User         | Host      |
+--------------+-----------+
| fastapi_user | %         |  ← 모든 호스트에서 접근 가능
| root         | %         |  
| healthcheck  | 127.0.0.1 |
| healthcheck  | ::1       |
| healthcheck  | localhost |
| mariadb.sys  | localhost |
| root         | localhost |
+--------------+-----------+
```

## Docker 네트워크 이해하기

### 왜 172.18.0.1에서 접근하는가?

```
Windows Host (localhost)
     ↓
Docker Desktop
     ↓
Docker Bridge Network (172.18.0.0/16)
     ├─ Gateway: 172.18.0.1 (호스트)
     └─ Container: 172.18.0.x (MariaDB)
```

- **localhost (127.0.0.1)**: Windows 호스트에서 보는 주소
- **172.18.0.1**: Docker 컨테이너에서 보는 호스트 주소
- Docker 컨테이너 내부에서는 호스트가 `172.18.0.1`로 보입니다

### MariaDB는 어떻게 연결을 받는가?

1. Windows에서 `localhost:3306`으로 연결 시도
2. Docker가 포트를 컨테이너로 포워딩
3. MariaDB 컨테이너는 연결이 `172.18.0.1`에서 온 것으로 인식
4. `'fastapi_user'@'%'` 권한으로 접근 허용

## 서버 실행 및 테스트

### 1. 서버 실행
```powershell
cd C:\Users\kknd5050\projects\py\fast-api-practice
.\fastapienv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**성공 메시지:**
```
Database tables created successfully!
INFO:     Will watch for changes in these directories: ['C:\\Users\\...']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx] using WatchFiles
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### 2. API 테스트

#### 헬스 체크
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

**결과:**
```json
{"status":"healthy"}
```

#### Swagger UI
브라우저에서: http://localhost:8000/docs

### 3. 전체 테스트 스크립트

```powershell
# 사용자 등록
$registerBody = @{
    email = "test@example.com"
    username = "testuser"
    password = "Test123!@#"
} | ConvertTo-Json

$user = Invoke-RestMethod -Method Post `
    -Uri "http://localhost:8000/api/auth/register" `
    -ContentType "application/json" `
    -Body $registerBody

Write-Host "User registered: $($user.username)" -ForegroundColor Green

# 로그인
$loginBody = @{
    username = "testuser"
    password = "Test123!@#"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Method Post `
    -Uri "http://localhost:8000/api/auth/login" `
    -ContentType "application/json" `
    -Body $loginBody

$token = $loginResponse.access_token
Write-Host "Token: $token" -ForegroundColor Cyan

# 현재 사용자 정보 조회
$headers = @{
    Authorization = "Bearer $token"
}

$currentUser = Invoke-RestMethod -Method Get `
    -Uri "http://localhost:8000/api/users/me" `
    -Headers $headers

Write-Host "Current user email: $($currentUser.email)" -ForegroundColor Green
```

## 데이터베이스 직접 확인

```powershell
# MariaDB 접속
docker exec -it fastapi_mariadb mariadb -u fastapi_user -pfastapi_password fastapi_db

# 테이블 확인
SHOW TABLES;

# users 테이블 구조
DESCRIBE users;

# 데이터 확인
SELECT id, username, email, is_active, created_at FROM users;

# 종료
EXIT;
```

## 트러블슈팅

### 문제 1: 여전히 연결 안됨
```powershell
# 1. 컨테이너 상태 확인
docker ps

# 2. 컨테이너 재시작
docker compose restart

# 3. 로그 확인
docker logs fastapi_mariadb

# 4. 포트 확인
netstat -ano | findstr :3306
```

### 문제 2: 권한 에러
```powershell
# 권한 재설정
docker exec fastapi_mariadb mariadb -u root -prootpassword -e `
    "DROP USER IF EXISTS 'fastapi_user'@'%'; 
     CREATE USER 'fastapi_user'@'%' IDENTIFIED BY 'fastapi_password';
     GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'%';
     FLUSH PRIVILEGES;"
```

### 문제 3: 테이블이 생성되지 않음
```powershell
# Python 스크립트로 테이블 생성
cd C:\Users\kknd5050\projects\py\fast-api-practice
.\fastapienv\Scripts\Activate.ps1

python -c "from app.database import Base, engine; Base.metadata.create_all(bind=engine); print('Tables created!')"
```

## 핵심 교훈

### ✅ DO (해야 할 것)
1. **전용 사용자 사용**: `root` 대신 `fastapi_user` 사용
2. **Host `%` 사용**: Docker 네트워크 IP를 허용하기 위해
3. **`.env` 파일 확인**: 환경 변수가 올바른지 항상 확인
4. **`--skip-name-resolve`**: DNS 조회를 생략하여 성능 향상

### ❌ DON'T (하지 말아야 할 것)
1. **특정 IP로 제한하지 마세요**: Docker IP는 동적으로 변경될 수 있음
2. **root 사용자 직접 사용하지 마세요**: 보안상 위험
3. **환경 변수 하드코딩하지 마세요**: `.env` 파일 사용

## 최종 확인

현재 서버가 http://localhost:8000 에서 실행 중입니다!

### 확인 사항:
- ✅ MariaDB 컨테이너 실행 중
- ✅ fastapi_user 권한 설정 완료
- ✅ .env 파일 올바르게 설정
- ✅ 서버 실행 중
- ✅ 데이터베이스 연결 성공

### 다음 단계:
1. http://localhost:8000/docs 에서 API 문서 확인
2. 사용자 등록 및 로그인 테스트
3. JWT 토큰 인증 테스트
4. 프로젝트 개발 시작!

## 참고 자료

- [SQLAlchemy 2.0 문서](https://docs.sqlalchemy.org/en/20/)
- [FastAPI 문서](https://fastapi.tiangolo.com/)
- [Docker 네트워킹](https://docs.docker.com/network/)
- [MariaDB 사용자 관리](https://mariadb.com/kb/en/create-user/)

---

🎉 **문제가 완전히 해결되었습니다!** 🎉

