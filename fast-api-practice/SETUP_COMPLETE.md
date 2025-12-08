# FastAPI JWT Authentication Project 설정 완료!

## 🎉 프로젝트가 성공적으로 구성되었습니다!

### 설치된 구성 요소

#### 1. FastAPI 애플리케이션
- ✅ FastAPI 0.122.0
- ✅ Uvicorn ASGI 서버
- ✅ Pydantic v2 데이터 검증
- ✅ CORS 미들웨어

#### 2. JWT 인증 시스템
- ✅ python-jose (JWT 생성/검증)
- ✅ passlib + bcrypt (비밀번호 해싱)
- ✅ OAuth2 호환 인증 스킴

#### 3. 데이터베이스
- ✅ MariaDB 11.6 (Docker 컨테이너)
- ✅ SQLAlchemy 2.0.36 ORM
- ✅ PyMySQL 드라이버

### 프로젝트 구조

```
fast-api-practice/
├── app/
│   ├── __init__.py
│   ├── database.py          # 데이터베이스 연결
│   ├── models.py            # User 모델
│   ├── schemas.py           # Pydantic 스키마
│   ├── auth.py              # JWT 인증 로직
│   ├── dependencies.py      # FastAPI 의존성
│   └── routers/
│       ├── __init__.py
│       ├── auth.py          # 인증 API
│       └── users.py         # 사용자 API
├── main.py                  # 앱 진입점
├── requirements.txt
├── docker-compose.yml       # MariaDB 설정
├── .env                     # 환경 변수
└── README.md
```

### 서버 실행 방법

#### 방법 1: 직접 실행
```powershell
# 가상환경 활성화
.\fastapienv\Scripts\Activate.ps1

# 서버 실행
python main.py
```

#### 방법 2: uvicorn으로 실행
```powershell
.\fastapienv\Scripts\Activate.ps1
uvicorn main:app --reload
```

### API 엔드포인트

#### 인증 (Authentication)
- `POST /api/auth/register` - 사용자 등록
- `POST /api/auth/login` - 로그인 (JWT 발급)
- `POST /api/auth/token` - OAuth2 토큰 (Swagger UI용)

#### 사용자 (Users) - 인증 필요
- `GET /api/users/me` - 현재 사용자 정보
- `PUT /api/users/me` - 사용자 정보 수정
- `DELETE /api/users/me` - 계정 삭제
- `GET /api/users/` - 모든 사용자 목록
- `GET /api/users/{user_id}` - 특정 사용자 조회

#### 기본 엔드포인트
- `GET /` - 루트
- `GET /health` - 헬스 체크

### API 문서 확인

서버 실행 후 브라우저에서 접속:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 사용 예시

#### 1. 사용자 등록
```bash
curl -X POST http://localhost:8000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "username": "testuser",
    "password": "password123"
  }'
```

또는 PowerShell:
```powershell
$body = @{
    email = "user@example.com"
    username = "testuser"
    password = "password123"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/auth/register" `
    -ContentType "application/json" -Body $body
```

#### 2. 로그인 (JWT 토큰 받기)
```powershell
$loginBody = @{
    username = "testuser"
    password = "password123"
} | ConvertTo-Json

$response = Invoke-RestMethod -Method Post -Uri "http://localhost:8000/api/auth/login" `
    -ContentType "application/json" -Body $loginBody

$token = $response.access_token
```

#### 3. 인증된 요청 (현재 사용자 정보)
```powershell
$headers = @{
    Authorization = "Bearer $token"
}

Invoke-RestMethod -Method Get -Uri "http://localhost:8000/api/users/me" -Headers $headers
```

### Docker 명령어

#### MariaDB 컨테이너 관리
```powershell
# 컨테이너 시작
docker compose up -d

# 컨테이너 중지
docker compose stop

# 컨테이너 제거
docker compose down

# 로그 확인
docker logs fastapi_mariadb

# 데이터베이스 접속
docker exec -it fastapi_mariadb mysql -u root -prootpassword
```

#### 데이터베이스 연결 정보
- Host: localhost
- Port: 3306
- Database: fastapi_db
- User: fastapi_user
- Password: fastapi_password
- Root Password: rootpassword

### 환경 변수 (.env)

```env
DATABASE_URL=mysql+pymysql://fastapi_user:fastapi_password@localhost:3306/fastapi_db
SECRET_KEY=your-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 데이터베이스 스키마

**users 테이블**:
- `id` - INT (Primary Key)
- `email` - VARCHAR(255) (Unique)
- `username` - VARCHAR(255) (Unique)
- `hashed_password` - VARCHAR(255)
- `is_active` - BOOLEAN
- `is_superuser` - BOOLEAN
- `created_at` - DATETIME
- `updated_at` - DATETIME

### 보안 고려사항

⚠️ **프로덕션 배포 전 필수 작업**:

1. `.env` 파일의 `SECRET_KEY` 변경
   ```python
   # Python에서 안전한 키 생성
   import secrets
   print(secrets.token_urlsafe(32))
   ```

2. CORS 설정 제한
   ```python
   # main.py에서 수정
   allow_origins=["https://yourdomain.com"]  # 특정 도메인만 허용
   ```

3. 데이터베이스 비밀번호 변경

4. HTTPS 사용 설정

### 문제 해결

#### 데이터베이스 연결 오류
```powershell
# MariaDB 컨테이너 재시작
docker compose restart

# 사용자 권한 재설정
docker exec fastapi_mariadb mysql -u root -prootpassword -e `
    "GRANT ALL PRIVILEGES ON fastapi_db.* TO 'fastapi_user'@'%' IDENTIFIED BY 'fastapi_password'; FLUSH PRIVILEGES;"
```

#### 포트 충돌
```powershell
# 다른 포트로 실행
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

### 다음 단계

1. ✅ 서버가 정상 작동하는지 확인: http://localhost:8000/docs
2. ✅ 사용자 등록 테스트
3. ✅ 로그인 및 JWT 토큰 발급 테스트
4. ✅ 인증이 필요한 엔드포인트 테스트
5. 필요에 따라 추가 기능 구현

### 추가 기능 아이디어

- 이메일 인증
- 비밀번호 재설정
- 사용자 프로필 이미지
- 사용자 역할/권한 시스템
- API 레이트 리미팅
- 로깅 시스템
- 테스트 코드 작성

## 🚀 프로젝트를 즐기세요!

질문이나 문제가 있으면 README.md를 참조하세요.

