FROM gleif/keri:0.7.1

SHELL ["/bin/bash", "-c"]
EXPOSE 5621

RUN mkdir -p /usr/local/var/keri
RUN mkdir -p /ward/keri/cf

COPY ./prod-witness-prod-schema.json /ward/keri/cf/prod-witness-prod-schema.json

ENTRYPOINT ["kli", "agent", "start", "--config-dir", "/ward",  "--config-file", "prod-witness-prod-schema", "--admin-http-port", "5621", "--insecure"]


