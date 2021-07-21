FROM docker.elastic.co/elasticsearch/elasticsearch-oss:6.3.1
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-icu
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install analysis-stempel
RUN /usr/share/elasticsearch/bin/elasticsearch-plugin install org.wikimedia.search:extra:6.3.1.2
