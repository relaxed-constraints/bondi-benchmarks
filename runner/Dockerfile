FROM maven:3.9-eclipse-temurin-8 AS build
WORKDIR /src
ADD https://codeload.github.com/brianfrankcooper/YCSB/tar.gz/ae02b31fa7784b3892f121c06638aa0cd972fa06 /tmp/ycsb.tgz
RUN echo '717c991f20aab76ad8ede371e7ff8bdc2b7ee05a1d6eda4818dc91102ca9651a  /tmp/ycsb.tgz' | sha256sum -c - && tar xzf /tmp/ycsb.tgz --strip-components=1
COPY *.patch /tmp/
RUN git apply /tmp/*.patch && rm mongodb/src/main/java/site/ycsb/db/AsyncMongoDbClient.java && mvn -B -pl binding-parent/datastore-specific-descriptor,mongodb,couchbase2 -am -Dmaven.test.skip=true -Dcheckstyle.skip -Dcouchbase2.version=2.7.23 package
RUN mkdir /out && for binding in mongodb couchbase2; do mkdir /out/$binding; tar xzf $binding/target/ycsb-$binding-binding-0.18.0-SNAPSHOT*.tar.gz --strip-components=1 -C /out/$binding; done

FROM eclipse-temurin:8-jre
COPY --from=build /out /opt/ycsb
COPY run.sh /opt/run.sh
ENTRYPOINT ["sh", "/opt/run.sh"]
