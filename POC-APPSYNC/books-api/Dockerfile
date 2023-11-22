FROM gradle:8.0.0-jdk17-alpine AS build
COPY --chown=gradle:gradle . /home/gradle/src
WORKDIR /home/gradle/src
RUN gradle clean build

FROM eclipse-temurin:17-jdk-alpine
VOLUME /tmp

COPY --from=build  /home/gradle/src/build/libs/books-api-0.0.1-SNAPSHOT.jar /app.jar
ENTRYPOINT ["java","-jar","/app.jar"]
