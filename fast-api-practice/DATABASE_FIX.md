# ✅ 데이터베이스 연결 문제 해결 완료!

## 문제
```
Warning: Could not create database tables: (pymysql.err.OperationalError) (1045, "Access denied for user 'root'@'172.18.0.1' (using password: YES)")
```

## 해결 방법

### 1. ✅ MariaDB 사용자 권한 설정 완료
다음 명령으로 `fastapi_user` 사용자를 생성하고 권한을 부여했습니다:

```powershell
docker exec fastapi_mariadb mariadb -u root -prootpassword -e "CREATE USER IF NOT EXISTS 'fastapi_user'@'%' IDENTIFIED BY 'fastapi_password'; GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'%'; FLUSH PRIVILEGES;"
```

### 2. ✅ .env 파일 수정 완료
`.env` 파일에서 데이터베이스 사용자를 `fastapi_user`로 변경했습니다.

## 서버 실행 확인

### 방법 1: 새 터미널에서 실행 (권장)
```powershell
cd C:\Users\kknd5050\projects\py\fast-api-practice
.\fastapienv\Scripts\Activate.ps1
python main.py
```

다음과 같은 메시지가 표시되어야 합니다:
```
Database tables created successfully!
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 방법 2: 백그라운드에서 실행
```powershell
cd C:\Users\kknd5050\projects\py\fast-api-practice
.\fastapienv\Scripts\Activate.ps1
Start-Process python -ArgumentList "main.py" -WindowStyle Hidden
```

### 방법 3: Uvicorn으로 실행 (로그 출력 보장)
```powershell
cd C:\Users\kknd5050\projects\py\fast-api-practice
.\fastapienv\Scripts\Activate.ps1
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## API 테스트

### 1. 헬스 체크
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get
```

**예상 결과:**
```json
{"status":"healthy"}
```

### 2. 루트 엔드포인트
```powershell
Invoke-RestMethod -Uri "http://localhost:8000/" -Method Get
```

**예상 결과:**
```json
{
  "message": "Welcome to FastAPI JWT Authentication API",
  "docs": "/docs",
  "redoc": "/redoc"
}
```

### 3. 브라우저에서 확인
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 완전한 API 테스트 시나리오

### Step 1: 사용자 등록
```powershell
$registerBody = @{
    email = "test@example.com"
    username = "testuser"
    password = "Test123!@#"
} | ConvertTo-Json

$registerResponse = Invoke-RestMethod -Method Post `
    -Uri "http://localhost:8000/api/auth/register" `
    -ContentType "application/json" `
    -Body $registerBody

Write-Host "사용자 등록 완료!" -ForegroundColor Green
$registerResponse
```

### Step 2: 로그인 (JWT 토큰 받기)
```powershell
$loginBody = @{
    username = "testuser"
    password = "Test123!@#"
} | ConvertTo-Json

$loginResponse = Invoke-RestMethod -Method Post `
    -Uri "http://localhost:8000/api/auth/login" `
    -ContentType "application/json" `
    -Body $loginBody

$token = $loginResponse.access_token
Write-Host "로그인 성공! 토큰: $token" -ForegroundColor Green
```

### Step 3: 인증된 요청 (현재 사용자 정보)
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

$userInfo = Invoke-RestMethod -Method Get `
    -Uri "http://localhost:8000/api/users/me" `
    -Headers $headers

Write-Host "현재 사용자 정보:" -ForegroundColor Green
$userInfo
```

### Step 4: 사용자 정보 수정
```powershell
$updateBody = @{
    email = "newemail@example.com"
} | ConvertTo-Json

$updatedUser = Invoke-RestMethod -Method Put `
    -Uri "http://localhost:8000/api/users/me" `
    -Headers $headers `
    -ContentType "application/json" `
    -Body $updateBody

Write-Host "사용자 정보 수정 완료!" -ForegroundColor Green
$updatedUser
```

## 데이터베이스 직접 확인

```powershell
# MariaDB 컨테이너 접속
docker exec -it fastapi_mariadb mariadb -u fastapi_user -pfastapi_password fastapi_db

# SQL 명령 실행
SELECT * FROM users;
DESCRIBE users;
EXIT;
```

## 문제 해결

### 포트가 이미 사용 중인 경우
```powershell
# 포트 사용 중인 프로세스 확인
Get-NetTCPConnection -LocalPort 8000 | Select-Object -Property OwningProcess | ForEach-Object {Get-Process -Id $_.OwningProcess}

# 프로세스 종료
Stop-Process -Id <PROCESS_ID> -Force

# 또는 다른 포트로 실행
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 데이터베이스 초기화
```powershell
# 테이블 삭제 및 재생성
docker exec fastapi_mariadb mariadb -u fastapi_user -pfastapi_password -e "DROP DATABASE IF EXISTS fastapi_db; CREATE DATABASE fastapi_db;"

# 서버 재시작 (테이블 자동 생성됨)
```

### MariaDB 컨테이너 재시작
```powershell
docker compose restart

# 또는 완전히 재생성
docker compose down
docker compose up -d
```

## 현재 상태

✅ **완료된 작업:**
1. MariaDB 사용자 `fastapi_user` 생성 및 권한 부여
2. `.env` 파일에서 데이터베이스 사용자 설정
3. 서버 재시작 준비 완료

🔄 **다음 단계:**
1. 위의 방법으로 서버를 실행하세요
2. http://localhost:8000/docs 에서 API 문서 확인
3. API 테스트 시나리오를 따라 기능 테스트

## 추가 도움말

모든 단계를 한 번에 실행하는 스크립트:

```powershell
# 전체 테스트 스크립트
cd C:\Users\kknd5050\projects\py\fast-api-practice

# 서버가 실행 중인지 확인
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -ErrorAction Stop
    Write-Host "✅ 서버가 이미 실행 중입니다!" -ForegroundColor Green
    Write-Host "응답: $($response | ConvertTo-Json)" -ForegroundColor Cyan
} catch {
    Write-Host "❌ 서버가 실행되지 않았습니다. 서버를 시작하세요:" -ForegroundColor Yellow
    Write-Host "  .\fastapienv\Scripts\Activate.ps1" -ForegroundColor Cyan
    Write-Host "  python main.py" -ForegroundColor Cyan
}
```

이 파일을 저장한 후 실행하세요!

