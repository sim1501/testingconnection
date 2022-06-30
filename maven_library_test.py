# Databricks notebook source
# MAGIC %python
# MAGIC  
# MAGIC import requests
# MAGIC import json
# MAGIC import time
# MAGIC from pyspark.sql.types import (StructField, StringType, StructType, IntegerType)
# MAGIC   
# MAGIC target_cluster_api_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
# MAGIC target_token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
# MAGIC  
# MAGIC target_cluster_id = "0112-155314-glee262"
# MAGIC 
# MAGIC libraries = [{'maven': {'coordinates': 'com.moodysalem:LatLongToTimezoneMaven:1.2'}}, {'maven': {'coordinates': 'com.comcast:ip4s_2.11:1.0.2'}}, {'maven': {'coordinates': 'org.zeroturnaround:zt-zip:1.14'}}, {'maven': {'coordinates': 'com.uber:h3:3.6.4'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:2.11.3'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.module:jackson-module-scala:2.1.2'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.13.1'}}, {'maven': {'coordinates': 'io.circe:circe-generic_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_2.12:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.12.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark2:0.10.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark-runtime:0.10.0'}}, {'maven': {'coordinates': 'io.spray:spray-json_2.10:1.3.2'}}, {'maven': {'coordinates': 'commons-validator:commons-validator:1.6'}}, {'maven': {'coordinates': 'com.github.databricks:spark-redshift_2.11:master-SNAPSHOT', 'repo': 'https://jitpack.io'}}, {'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}}, {'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, {'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}] 
# MAGIC print(target_cluster_api_url)
# MAGIC target_lib_install_payload = json.dumps({'cluster_id': target_cluster_id, 'libraries': libraries})
# MAGIC  
# MAGIC response = requests.post(target_cluster_api_url+"/api/2.0/libraries/install", headers={'Authorization': "Bearer " + target_token}, data = target_lib_install_payload)
# MAGIC  
# MAGIC print(target_lib_install_payload)
# MAGIC print(response.status_code)

# COMMAND ----------

libraries = [{'maven': {'coordinates': 'com.moodysalem:LatLongToTimezoneMaven:1.2'}}, {'maven': {'coordinates': 'com.comcast:ip4s_2.11:1.0.2'}}, {'maven': {'coordinates': 'org.zeroturnaround:zt-zip:1.14'}}, {'maven': {'coordinates': 'com.uber:h3:3.6.4'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:2.11.3'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.module:jackson-module-scala:2.1.2'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.13.1'}}, {'maven': {'coordinates': 'io.circe:circe-generic_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_2.12:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.12.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark2:0.10.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark-runtime:0.10.0'}}, {'maven': {'coordinates': 'io.spray:spray-json_2.10:1.3.2'}}, {'maven': {'coordinates': 'commons-validator:commons-validator:1.6'}}, {'maven': {'coordinates': 'com.github.databricks:spark-redshift_2.11:master-SNAPSHOT', 'repo': 'https://jitpack.io'}}, {'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}}, {'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, {'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}]

# COMMAND ----------

import os
import json
import traceback



def debug(msg):
  if ( DEBUG ):
    print(msg)
  
def get_dependency(coordinate):
  coordinate_array = coordinate.split(":")
  return dep_template.format(groupId=coordinate_array[0], artifactId=coordinate_array[1], version=coordinate_array[2])



# constants
pom_template = '''<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>group-id</groupId>
  <artifactId>artifact-id</artifactId>
  <version>1.0</version>
  <packaging>jar</packaging>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    {dependencies}
  </dependencies>
</project>'''

dep_template = '''
    <dependency>
      <groupId>{groupId}</groupId>
      <artifactId>{artifactId}</artifactId>
      <version>{version}</version>
    </dependency>'''


DEBUG = False
dependencies = []

libraries = [{'maven': {'coordinates': 'com.moodysalem:LatLongToTimezoneMaven:1.2'}}, {'maven': {'coordinates': 'com.comcast:ip4s_2.11:1.0.2'}}, {'maven': {'coordinates': 'org.zeroturnaround:zt-zip:1.14'}}, {'maven': {'coordinates': 'com.uber:h3:3.6.4'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:2.11.3'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.module:jackson-module-scala:2.1.2'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.13.1'}}, {'maven': {'coordinates': 'io.circe:circe-generic_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_2.12:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.12.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark2:0.10.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark-runtime:0.10.0'}}, {'maven': {'coordinates': 'io.spray:spray-json_2.10:1.3.2'}}, {'maven': {'coordinates': 'commons-validator:commons-validator:1.6'}},  {'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}}, {'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, {'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}]
             
for library in libraries:
  debug('checking for {0}...'.format(library))
  if 'maven' in library:
    print(library)
    print(library['maven']['coordinates'])
    coordinates = library['maven']['coordinates']
    dep = get_dependency(coordinates)
    if ( dep ):
      dependencies.append(dep)
      debug('success')
  else:
    print('Skpping non maven library %s' % library)
output_file = "pom.xml"
f = open(output_file, 'w')
f.write(pom_template.format(dependencies='\n'.join(dependencies)))
f.close()

# COMMAND ----------

# MAGIC %sh cat pom.xml

# COMMAND ----------

# MAGIC %sh apt-get -y install maven

# COMMAND ----------

# MAGIC %sh mvn --version

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC mkdir -p /tmp/pom_test;
# MAGIC cp pom.xml /tmp/pom_test

# COMMAND ----------

# MAGIC %sh cd /tmp/pom_test;
# MAGIC mvn dependency:tree

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp;
# MAGIC mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:get -Dartifact=io:circe:circe-yaml_2.13:0.13.1 &>/tmp/circe-yaml_2.13.txt
# MAGIC cat /tmp/circe-yaml_2.13.txt

# COMMAND ----------

# MAGIC %sh
# MAGIC cd /tmp;
# MAGIC mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:get -Dartifact=org.tpolecat:doobie-core_2.11:0.4.4 &>/tmp/tpolecat.txt
# MAGIC cat /tmp/tpolecat.txt

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:get -Dartifact=io.circe:circe-parse_2.11:0.2.1 &>/tmp/circe.txt
# MAGIC cat /tmp/circe.txt

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:get -Dartifact=io.circe:circe-yaml_2.13:0.12.0 &>/tmp/doobie.txt
# MAGIC cat /tmp/doobie.txt

# COMMAND ----------

# MAGIC %sh 
# MAGIC 
# MAGIC cat /tmp/doobie.txt | grep -i jar

# COMMAND ----------

# MAGIC %sh cp /tmp/circe.txt /dbfs/FileStore/

# COMMAND ----------

# MAGIC %sh cd /tmp/pom_test;
# MAGIC mvn dependency:tree -Dverbose

# COMMAND ----------

INFO] --- maven-dependency-plugin:2.8:tree (default-cli) @ artifact-id ---
[INFO] group-id:artifact-id:jar:1.0
[INFO] +- com.moodysalem:LatLongToTimezoneMaven:jar:1.2:compile
[INFO] +- com.comcast:ip4s_2.11:jar:1.0.2:compile
[INFO] |  +- org.scala-lang:scala-library:jar:2.11.12:compile
[INFO] |  \- org.typelevel:cats-effect_2.11:jar:0.10:compile
[INFO] |     +- (org.scala-lang:scala-library:jar:2.11.12:compile - omitted for duplicate)
[INFO] |     \- org.typelevel:cats-core_2.11:jar:1.0.1:compile
[INFO] |        +- (org.scala-lang:scala-library:jar:2.11.12:compile - omitted for duplicate)
[INFO] |        +- org.typelevel:cats-macros_2.11:jar:1.0.1:compile
[INFO] |        |  +- (org.scala-lang:scala-library:jar:2.11.12:compile - omitted for duplicate)
[INFO] |        |  \- (org.typelevel:machinist_2.11:jar:0.6.2:compile - omitted for duplicate)
[INFO] |        +- org.typelevel:cats-kernel_2.11:jar:1.0.1:compile
[INFO] |        |  \- (org.scala-lang:scala-library:jar:2.11.12:compile - omitted for duplicate)
[INFO] |        \- org.typelevel:machinist_2.11:jar:0.6.2:compile
[INFO] |           +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |           \- (org.scala-lang:scala-reflect:jar:2.11.8:compile - omitted for duplicate)
[INFO] +- org.zeroturnaround:zt-zip:jar:1.14:compile
[INFO] |  \- org.slf4j:slf4j-api:jar:1.6.6:compile
[INFO] +- com.uber:h3:jar:3.6.4:compile
[INFO] +- com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:jar:2.11.3:compile
[INFO] |  +- com.fasterxml.jackson.core:jackson-databind:jar:2.11.3:compile
[INFO] |  |  +- (com.fasterxml.jackson.core:jackson-annotations:jar:2.11.3:compile - omitted for conflict with 2.1.0)
[INFO] |  |  \- (com.fasterxml.jackson.core:jackson-core:jar:2.11.3:compile - omitted for duplicate)
[INFO] |  +- org.yaml:snakeyaml:jar:1.26:compile
[INFO] |  \- com.fasterxml.jackson.core:jackson-core:jar:2.11.3:compile
[INFO] +- com.fasterxml.jackson.module:jackson-module-scala:jar:2.1.2:compile
[INFO] |  +- (com.fasterxml.jackson.core:jackson-core:jar:2.1.0:compile - omitted for conflict with 2.11.3)
[INFO] |  +- com.fasterxml.jackson.core:jackson-annotations:jar:2.1.0:compile
[INFO] |  +- (com.fasterxml.jackson.core:jackson-databind:jar:2.1.0:compile - omitted for conflict with 2.11.3)
[INFO] |  +- (org.scala-lang:scala-library:jar:2.9.1:compile - omitted for conflict with 2.11.12)
[INFO] |  \- org.scalastuff:scalabeans:jar:0.3:compile
[INFO] |     +- com.thoughtworks.paranamer:paranamer:jar:2.3:compile
[INFO] |     \- com.google.guava:guava:jar:r09:compile
[INFO] +- io.circe:circe-yaml_2.13:jar:0.12.0:compile
[INFO] |  +- (org.scala-lang:scala-library:jar:2.13.0:compile - omitted for conflict with 2.11.12)
[INFO] |  +- io.circe:circe-core_2.13:jar:0.12.3:compile
[INFO] |  |  +- (org.scala-lang:scala-library:jar:2.13.0:compile - omitted for conflict with 2.11.12)
[INFO] |  |  +- io.circe:circe-numbers_2.13:jar:0.12.3:compile
[INFO] |  |  |  \- (org.scala-lang:scala-library:jar:2.13.0:compile - omitted for conflict with 2.11.12)
[INFO] |  |  \- (org.typelevel:cats-core_2.13:jar:2.0.0:compile - omitted for conflict with 2.1.1)
[INFO] |  \- (org.yaml:snakeyaml:jar:1.25:compile - omitted for conflict with 1.26)
[INFO] +- io.circe:circe-generic_0.26:jar:0.14.0-M1:compile
[INFO] |  +- (io.circe:circe-core_0.26:jar:0.14.0-M1:compile - omitted for duplicate)
[INFO] |  \- ch.epfl.lamp:dotty-library_0.26:jar:0.26.0-RC1:compile
[INFO] |     \- (org.scala-lang:scala-library:jar:2.13.3:compile - omitted for conflict with 2.11.12)
[INFO] +- io.circe:circe-core_0.26:jar:0.14.0-M1:compile
[INFO] |  +- io.circe:circe-numbers_0.26:jar:0.14.0-M1:compile
[INFO] |  |  \- (ch.epfl.lamp:dotty-library_0.26:jar:0.26.0-RC1:compile - omitted for duplicate)
[INFO] |  +- (ch.epfl.lamp:dotty-library_0.26:jar:0.26.0-RC1:compile - omitted for duplicate)
[INFO] |  \- org.typelevel:cats-core_2.13:jar:2.1.1:compile
[INFO] |     +- (org.scala-lang:scala-library:jar:2.13.1:compile - omitted for conflict with 2.11.12)
[INFO] |     +- org.typelevel:cats-macros_2.13:jar:2.1.1:compile
[INFO] |     |  \- (org.scala-lang:scala-library:jar:2.13.1:compile - omitted for conflict with 2.11.12)
[INFO] |     \- org.typelevel:cats-kernel_2.13:jar:2.1.1:compile
[INFO] |        \- (org.scala-lang:scala-library:jar:2.13.1:compile - omitted for conflict with 2.11.12)
[INFO] +- io.circe:circe-core_2.12:jar:0.14.0-M1:compile
[INFO] |  +- (org.scala-lang:scala-library:jar:2.12.11:compile - omitted for conflict with 2.11.12)
[INFO] |  +- io.circe:circe-numbers_2.12:jar:0.14.0-M1:compile
[INFO] |  |  \- (org.scala-lang:scala-library:jar:2.12.11:compile - omitted for conflict with 2.11.12)
[INFO] |  \- org.typelevel:cats-core_2.12:jar:2.1.1:compile
[INFO] |     +- (org.scala-lang:scala-library:jar:2.12.10:compile - omitted for conflict with 2.11.12)
[INFO] |     +- org.typelevel:cats-macros_2.12:jar:2.1.1:compile
[INFO] |     |  \- (org.scala-lang:scala-library:jar:2.12.10:compile - omitted for conflict with 2.11.12)
[INFO] |     \- org.typelevel:cats-kernel_2.12:jar:2.1.1:compile
[INFO] |        \- (org.scala-lang:scala-library:jar:2.12.10:compile - omitted for conflict with 2.11.12)
[INFO] +- org.apache.iceberg:iceberg-spark2:jar:0.10.0:compile
[INFO] |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  +- com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile
[INFO] |  +- org.apache.iceberg:iceberg-api:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  \- org.apache.iceberg:iceberg-bundled-guava:jar:0.10.0:compile
[INFO] |  +- org.apache.iceberg:iceberg-common:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  \- (org.apache.iceberg:iceberg-bundled-guava:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  +- org.apache.iceberg:iceberg-core:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-api:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-common:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  +- org.apache.avro:avro:jar:1.9.2:compile
[INFO] |  |  |  +- (com.fasterxml.jackson.core:jackson-core:jar:2.10.2:compile - omitted for conflict with 2.11.3)
[INFO] |  |  |  +- (com.fasterxml.jackson.core:jackson-databind:jar:2.10.2:compile - omitted for conflict with 2.11.3)
[INFO] |  |  |  +- org.apache.commons:commons-compress:jar:1.19:compile
[INFO] |  |  |  \- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.fasterxml.jackson.core:jackson-databind:jar:2.10.2:compile - omitted for conflict with 2.11.3)
[INFO] |  |  +- (com.fasterxml.jackson.core:jackson-core:jar:2.10.2:compile - omitted for conflict with 2.11.3)
[INFO] |  |  \- com.github.ben-manes.caffeine:caffeine:jar:2.7.0:compile
[INFO] |  |     +- org.checkerframework:checker-qual:jar:2.6.0:compile
[INFO] |  |     \- com.google.errorprone:error_prone_annotations:jar:2.3.3:compile
[INFO] |  +- org.apache.iceberg:iceberg-data:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-api:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  \- (org.apache.iceberg:iceberg-core:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  +- org.apache.iceberg:iceberg-orc:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-api:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-core:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  \- org.apache.orc:orc-core:jar:nohive:1.6.5:compile
[INFO] |  |     +- org.apache.orc:orc-shims:jar:1.6.5:compile
[INFO] |  |     |  \- (org.slf4j:slf4j-api:jar:1.7.5:compile - omitted for conflict with 1.6.6)
[INFO] |  |     +- commons-lang:commons-lang:jar:2.6:compile
[INFO] |  |     +- io.airlift:aircompressor:jar:0.16:compile
[INFO] |  |     +- javax.xml.bind:jaxb-api:jar:2.2.11:compile
[INFO] |  |     +- org.jetbrains:annotations:jar:17.0.0:compile
[INFO] |  |     +- (org.slf4j:slf4j-api:jar:1.7.5:compile - omitted for conflict with 1.6.6)
[INFO] |  |     \- org.threeten:threeten-extra:jar:1.5.0:compile
[INFO] |  +- org.apache.iceberg:iceberg-parquet:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-api:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-core:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  \- org.apache.parquet:parquet-avro:jar:1.11.1:compile
[INFO] |  |     +- org.apache.parquet:parquet-column:jar:1.11.1:compile
[INFO] |  |     |  +- org.apache.parquet:parquet-common:jar:1.11.1:compile
[INFO] |  |     |  |  +- (org.apache.parquet:parquet-format-structures:jar:1.11.1:compile - omitted for duplicate)
[INFO] |  |     |  |  +- (org.slf4j:slf4j-api:jar:1.7.22:compile - omitted for conflict with 1.6.6)
[INFO] |  |     |  |  \- org.apache.yetus:audience-annotations:jar:0.11.0:compile
[INFO] |  |     |  \- org.apache.parquet:parquet-encoding:jar:1.11.1:compile
[INFO] |  |     |     \- (org.apache.parquet:parquet-common:jar:1.11.1:compile - omitted for duplicate)
[INFO] |  |     +- org.apache.parquet:parquet-hadoop:jar:1.11.1:compile
[INFO] |  |     |  +- (org.apache.parquet:parquet-column:jar:1.11.1:compile - omitted for duplicate)
[INFO] |  |     |  +- (org.apache.parquet:parquet-format-structures:jar:1.11.1:compile - omitted for duplicate)
[INFO] |  |     |  +- org.apache.parquet:parquet-jackson:jar:1.11.1:compile
[INFO] |  |     |  +- org.xerial.snappy:snappy-java:jar:1.1.7.3:compile
[INFO] |  |     |  \- commons-pool:commons-pool:jar:1.6:compile
[INFO] |  |     \- org.apache.parquet:parquet-format-structures:jar:1.11.1:compile
[INFO] |  |        +- (org.slf4j:slf4j-api:jar:1.7.22:compile - omitted for conflict with 1.6.6)
[INFO] |  |        \- javax.annotation:javax.annotation-api:jar:1.3.2:compile
[INFO] |  +- org.apache.iceberg:iceberg-arrow:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-api:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.iceberg:iceberg-parquet:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  |  +- org.apache.arrow:arrow-vector:jar:1.0.0:compile
[INFO] |  |  |  +- org.apache.arrow:arrow-format:jar:1.0.0:compile
[INFO] |  |  |  |  \- (com.google.flatbuffers:flatbuffers-java:jar:1.9.0:compile - omitted for duplicate)
[INFO] |  |  |  +- org.apache.arrow:arrow-memory-core:jar:1.0.0:compile
[INFO] |  |  |  |  \- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  |  +- (com.fasterxml.jackson.core:jackson-core:jar:2.9.8:compile - omitted for conflict with 2.11.3)
[INFO] |  |  |  +- (com.fasterxml.jackson.core:jackson-annotations:jar:2.9.8:compile - omitted for conflict with 2.1.0)
[INFO] |  |  |  +- (com.fasterxml.jackson.core:jackson-databind:jar:2.9.8:compile - omitted for conflict with 2.11.3)
[INFO] |  |  |  +- (commons-codec:commons-codec:jar:1.10:compile - omitted for conflict with 1.9)
[INFO] |  |  |  +- com.google.flatbuffers:flatbuffers-java:jar:1.9.0:compile
[INFO] |  |  |  \- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  \- org.apache.arrow:arrow-memory-netty:jar:1.0.0:compile
[INFO] |  |     +- (org.apache.arrow:arrow-memory-core:jar:1.0.0:compile - omitted for duplicate)
[INFO] |  |     +- io.netty:netty-buffer:jar:4.1.48.Final:compile
[INFO] |  |     \- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  +- org.apache.iceberg:iceberg-hive-metastore:jar:0.10.0:compile
[INFO] |  |  +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |  |  +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |  |  \- (org.apache.iceberg:iceberg-core:jar:0.10.0:compile - omitted for duplicate)
[INFO] |  \- org.apache.iceberg:iceberg-spark:jar:0.10.0:compile
[INFO] |     +- (org.slf4j:slf4j-api:jar:1.7.25:compile - omitted for conflict with 1.6.6)
[INFO] |     +- (com.github.stephenc.findbugs:findbugs-annotations:jar:1.3.9-1:compile - omitted for duplicate)
[INFO] |     +- (org.apache.iceberg:iceberg-api:jar:0.10.0:compile - omitted for duplicate)
[INFO] |     +- (org.apache.iceberg:iceberg-common:jar:0.10.0:compile - omitted for duplicate)
[INFO] |     +- (org.apache.iceberg:iceberg-core:jar:0.10.0:compile - omitted for duplicate)
[INFO] |     +- (org.apache.iceberg:iceberg-data:jar:0.10.0:compile - omitted for duplicate)
[INFO] |     +- (org.apache.iceberg:iceberg-orc:jar:0.10.0:compile - omitted for duplicate)
[INFO] |     +- (org.apache.iceberg:iceberg-parquet:jar:0.10.0:compile - omitted for duplicate)
[INFO] |     +- (org.apache.iceberg:iceberg-arrow:jar:0.10.0:compile - omitted for duplicate)
[INFO] |     \- (org.apache.iceberg:iceberg-hive-metastore:jar:0.10.0:compile - omitted for duplicate)
[INFO] +- org.apache.iceberg:iceberg-spark-runtime:jar:0.10.0:compile
[INFO] +- io.spray:spray-json_2.10:jar:1.3.2:compile
[INFO] |  \- (org.scala-lang:scala-library:jar:2.10.5:compile - omitted for conflict with 2.11.12)
[INFO] +- commons-validator:commons-validator:jar:1.6:compile
[INFO] |  +- commons-beanutils:commons-beanutils:jar:1.9.2:compile
[INFO] |  |  +- (commons-logging:commons-logging:jar:1.1.1:compile - omitted for conflict with 1.2)
[INFO] |  |  \- (commons-collections:commons-collections:jar:3.2.1:compile - omitted for conflict with 3.2.2)
[INFO] |  +- commons-digester:commons-digester:jar:1.8.1:compile
[INFO] |  +- commons-logging:commons-logging:jar:1.2:compile
[INFO] |  \- commons-collections:commons-collections:jar:3.2.2:compile
[INFO] +- org.tpolecat:doobie-core_2.11:jar:0.3.1-M2:compile
[INFO] |  +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |  +- org.scala-lang:scala-reflect:jar:2.11.8:compile
[INFO] |  |  \- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |  +- com.chuusai:shapeless_2.11:jar:2.3.2:compile
[INFO] |  |  +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |  |  \- org.typelevel:macro-compat_2.11:jar:1.1.1:compile
[INFO] |  |     \- (org.scala-lang:scala-library:jar:2.11.7:compile - omitted for conflict with 2.11.12)
[INFO] |  +- org.scalaz:scalaz-core_2.11:jar:7.2.7:compile
[INFO] |  |  \- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |  +- org.scalaz:scalaz-effect_2.11:jar:7.2.7:compile
[INFO] |  |  +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |  |  \- (org.scalaz:scalaz-core_2.11:jar:7.2.7:compile - omitted for duplicate)
[INFO] |  \- org.scalaz.stream:scalaz-stream_2.11:jar:0.8.6a:compile
[INFO] |     +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |     +- (org.scalaz:scalaz-core_2.11:jar:7.2.7:compile - omitted for duplicate)
[INFO] |     +- org.scalaz:scalaz-concurrent_2.11:jar:7.2.7:compile
[INFO] |     |  +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |     |  +- (org.scalaz:scalaz-core_2.11:jar:7.2.7:compile - omitted for duplicate)
[INFO] |     |  \- (org.scalaz:scalaz-effect_2.11:jar:7.2.7:compile - omitted for duplicate)
[INFO] |     \- org.scodec:scodec-bits_2.11:jar:1.1.2:compile
[INFO] |        \- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] +- com.mashape.unirest:unirest-java:jar:1.4.9:compile
[INFO] |  +- org.apache.httpcomponents:httpclient:jar:4.5.2:compile
[INFO] |  |  +- org.apache.httpcomponents:httpcore:jar:4.4.4:compile
[INFO] |  |  +- (commons-logging:commons-logging:jar:1.2:compile - omitted for duplicate)
[INFO] |  |  \- commons-codec:commons-codec:jar:1.9:compile
[INFO] |  +- org.apache.httpcomponents:httpasyncclient:jar:4.1.1:compile
[INFO] |  |  +- (org.apache.httpcomponents:httpcore:jar:4.4.4:compile - omitted for duplicate)
[INFO] |  |  +- org.apache.httpcomponents:httpcore-nio:jar:4.4.4:compile
[INFO] |  |  |  \- (org.apache.httpcomponents:httpcore:jar:4.4.4:compile - omitted for duplicate)
[INFO] |  |  +- (org.apache.httpcomponents:httpclient:jar:4.5.1:compile - omitted for conflict with 4.5.2)
[INFO] |  |  \- (commons-logging:commons-logging:jar:1.2:compile - omitted for duplicate)
[INFO] |  +- org.apache.httpcomponents:httpmime:jar:4.5.2:compile
[INFO] |  |  \- (org.apache.httpcomponents:httpclient:jar:4.5.2:compile - omitted for duplicate)
[INFO] |  \- org.json:json:jar:20160212:compile
[INFO] +- org.json4s:json4s-native_2.11:jar:3.5.0:compile
[INFO] |  +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |  \- org.json4s:json4s-core_2.11:jar:3.5.0:compile
[INFO] |     +- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |     +- org.json4s:json4s-ast_2.11:jar:3.5.0:compile
[INFO] |     |  \- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |     +- org.json4s:json4s-scalap_2.11:jar:3.5.0:compile
[INFO] |     |  \- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] |     +- (com.thoughtworks.paranamer:paranamer:jar:2.8:compile - omitted for conflict with 2.3)
[INFO] |     \- org.scala-lang.modules:scala-xml_2.11:jar:1.0.6:compile
[INFO] |        \- (org.scala-lang:scala-library:jar:2.11.8:compile - omitted for conflict with 2.11.12)
[INFO] +- net.gpedro.integrations.slack:slack-webhook:jar:1.2.1:compile
[INFO] |  \- com.google.code.gson:gson:jar:2.3.1:compile
[INFO] \- joda-time:joda-time:jar:2.9.4:compile

# COMMAND ----------

import os
import json
import traceback



def debug(msg):
  if ( DEBUG ):
    print(msg)
  
def get_dependency(coordinate):
  coordinate_array = coordinate.split(":")
  return dep_template.format(groupId=coordinate_array[0], artifactId=coordinate_array[1], version=coordinate_array[2])



# constants
pom_template = '''<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>group-id</groupId>
  <artifactId>artifact-id</artifactId>
  <version>1.0</version>
  <packaging>jar</packaging>

  <properties>
    <project.build.sourceEncoding>UTF-8</project.build.sourceEncoding>
  </properties>

  <dependencies>
    {dependencies}
  </dependencies>
</project>'''

dep_template = '''<dependency org="{groupId}" name="{artifactId}" rev="{version}"/>'''


DEBUG = False
dependencies = []

libraries = [{'maven': {'coordinates': 'com.moodysalem:LatLongToTimezoneMaven:1.2'}}, {'maven': {'coordinates': 'com.comcast:ip4s_2.11:1.0.2'}}, {'maven': {'coordinates': 'org.zeroturnaround:zt-zip:1.14'}}, {'maven': {'coordinates': 'com.uber:h3:3.6.4'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:2.11.3'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.module:jackson-module-scala:2.1.2'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.13.1'}}, {'maven': {'coordinates': 'io.circe:circe-generic_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_2.12:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.12.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark2:0.10.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark-runtime:0.10.0'}}, {'maven': {'coordinates': 'io.spray:spray-json_2.10:1.3.2'}}, {'maven': {'coordinates': 'commons-validator:commons-validator:1.6'}},  {'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}}, {'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, {'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}]
             
for library in libraries:
  debug('checking for {0}...'.format(library))
  if 'maven' in library:
    print(library)
    print(library['maven']['coordinates'])
    coordinates = library['maven']['coordinates']
    dep = get_dependency(coordinates)
    if ( dep ):
      dependencies.append(dep)
      debug('success')
  else:
    print('Skpping non maven library %s' % library)
output_file = "ivy.yml"
f = open(output_file, 'w')
f.write(pom_template.format(dependencies='\n'.join(dependencies)))
f.close()

# COMMAND ----------

# MAGIC %sh cat ivy.yml

# COMMAND ----------

//pending

{'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark2:0.10.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark-runtime:0.10.0'}}, {'maven': {'coordinates': 'io.spray:spray-json_2.10:1.3.2'}}, {'maven': {'coordinates': 'commons-validator:commons-validator:1.6'}},  {'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}}, {'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, {'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}


// pending

{'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}}, {'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, {'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}


//
{'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}},


{'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, 

{'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}


# COMMAND ----------

# MAGIC %python
# MAGIC  
# MAGIC import requests
# MAGIC import json
# MAGIC import time
# MAGIC from pyspark.sql.types import (StructField, StringType, StructType, IntegerType)
# MAGIC   
# MAGIC target_cluster_api_url = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
# MAGIC target_token = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
# MAGIC  
# MAGIC target_cluster_id = "0114-211609-lobs9"
# MAGIC 
# MAGIC libraries = [{'maven': {'coordinates': 'com.moodysalem:LatLongToTimezoneMaven:1.2'}}, {'maven': {'coordinates': 'com.comcast:ip4s_2.11:1.0.2'}}, {'maven': {'coordinates': 'org.zeroturnaround:zt-zip:1.14'}}, {'maven': {'coordinates': 'com.uber:h3:3.6.4'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.dataformat:jackson-dataformat-yaml:2.11.3'}}, {'maven': {'coordinates': 'com.fasterxml.jackson.module:jackson-module-scala:2.1.2'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.13.1'}}, {'maven': {'coordinates': 'io.circe:circe-generic_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_0.26:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-core_2.12:0.14.0-M1'}}, {'maven': {'coordinates': 'io.circe:circe-yaml_2.13:0.12.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark2:0.10.0'}}, {'maven': {'coordinates': 'org.apache.iceberg:iceberg-spark-runtime:0.10.0'}}, {'maven': {'coordinates': 'io.spray:spray-json_2.10:1.3.2'}}, {'maven': {'coordinates': 'commons-validator:commons-validator:1.6'}}, {'maven': {'coordinates': 'com.github.databricks:spark-redshift_2.11:master-SNAPSHOT', 'repo': 'https://jitpack.io'}}, {'maven': {'coordinates': 'org.tpolecat:doobie-core_2.11:0.3.1-M2'}}, {'maven': {'coordinates': 'com.mashape.unirest:unirest-java:1.4.9'}}, {'maven': {'coordinates': 'org.json4s:json4s-native_2.11:3.5.0'}}, {'maven': {'coordinates': 'net.gpedro.integrations.slack:slack-webhook:1.2.1'}}, {'maven': {'coordinates': 'joda-time:joda-time:2.9.4'}}]
# MAGIC 
# MAGIC print(target_cluster_api_url)
# MAGIC target_lib_install_payload = json.dumps({'cluster_id': target_cluster_id, 'libraries': libraries})
# MAGIC  
# MAGIC response = requests.post(target_cluster_api_url+"/api/2.0/libraries/install", headers={'Authorization': "Bearer " + target_token}, data = target_lib_install_payload)
# MAGIC  
# MAGIC print(target_lib_install_payload)
# MAGIC print(response.status_code)

# COMMAND ----------

# MAGIC %python
# MAGIC  
# MAGIC import requests
# MAGIC import json
# MAGIC import time
# MAGIC from pyspark.sql.types import (StructField, StringType, StructType, IntegerType)
# MAGIC   
# MAGIC API_URL = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
# MAGIC TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
# MAGIC source_cluster_api_url = API_URL +"/api/2.0"
# MAGIC token = TOKEN
# MAGIC source_cluster = "0114-211609-lobs9"
# MAGIC  
# MAGIC url = source_cluster_api_url+"/libraries/cluster-status?cluster_id=" + source_cluster
# MAGIC response = requests.get(url,
# MAGIC headers={'Authorization': "Bearer " + token})
# MAGIC #print(response.json())
# MAGIC    
# MAGIC libraries = []
# MAGIC for library_info in  response.json()['library_statuses']:
# MAGIC   lib_type = library_info['library']
# MAGIC   status = library_info['status']
# MAGIC   if "dbfs:" in str(lib_type) or "s3:" in str(lib_type) or "pypi" in str(lib_type):
# MAGIC     print("Skipping dbfs/s3 library:" + str(lib_type)+"\n")
# MAGIC   else:
# MAGIC     libraries.append(lib_type)
# MAGIC print(libraries)

# COMMAND ----------

# MAGIC %python
# MAGIC  
# MAGIC import requests
# MAGIC import json
# MAGIC import time
# MAGIC from pyspark.sql.types import (StructField, StringType, StructType, IntegerType)
# MAGIC   
# MAGIC API_URL = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiUrl().getOrElse(None)
# MAGIC TOKEN = dbutils.notebook.entry_point.getDbutils().notebook().getContext().apiToken().getOrElse(None)
# MAGIC source_cluster_api_url = API_URL +"/api/2.0"
# MAGIC token = TOKEN
# MAGIC source_cluster = "0114-211609-lobs9"
# MAGIC  
# MAGIC url = source_cluster_api_url+"/libraries/cluster-status?cluster_id=" + source_cluster
# MAGIC response = requests.get(url,
# MAGIC headers={'Authorization': "Bearer " + token})
# MAGIC #print(response.json())
# MAGIC    
# MAGIC libraries = []
# MAGIC for library_info in  response.json()['library_statuses']:
# MAGIC   lib_type = library_info['library']
# MAGIC   status = library_info['status']
# MAGIC   if "dbfs:" in str(lib_type) or "s3:" in str(lib_type) or "pypi" in str(lib_type):
# MAGIC     print("Skipping dbfs/s3 library:" + str(lib_type)+"\n")
# MAGIC   else:
# MAGIC     libraries.append(lib_type)
# MAGIC print(libraries)

# COMMAND ----------

# MAGIC %sh
# MAGIC 
# MAGIC mvn org.apache.maven.plugins:maven-dependency-plugin:2.8:get -Dartifact=io.circe:circe-parse_2.11:0.2.1 &>/tmp/circe.txt
# MAGIC cat /tmp/circe.txt

# COMMAND ----------

# MAGIC %r
# MAGIC version

# COMMAND ----------

# MAGIC %r
# MAGIC ap <- available.packages()
# MAGIC View(ap)
# MAGIC "h2o" %in% rownames(ap)

# COMMAND ----------

# MAGIC %r
# MAGIC library(h2o)
# MAGIC  h2o.init()

# COMMAND ----------

