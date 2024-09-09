FROM openjdk:17-jdk-slim

# 로컬에서 빌드한 JAR 파일을 Docker 이미지로 복사
COPY build/libs/web_server-0.0.1-SNAPSHOT.jar app.jar

# 작업 디렉터리 설정
WORKDIR /app

# 포트 번호 설정
EXPOSE 8000

# 컨테이너가 시작될 때 실행할 명령 설정
ENTRYPOINT ["java", "-jar", "/app.jar", "--spring.profiles.active=docker"]