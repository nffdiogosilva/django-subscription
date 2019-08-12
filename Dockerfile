FROM python:3.7-stretch

LABEL maintainer="Nuno Diogo da Silva <diogosilva.nuno@gmail.com>"

ENV PATH=/root/.local/bin:$PATH \
    WORKDIR=/usr/src/app/src

RUN pip install pipx && \
    pipx install pew && \
    pipx install pipenv

COPY Pipfile* ./

COPY docker-entrypoint.sh /.
RUN chmod +x /docker-entrypoint.sh

RUN pipenv lock && \
    pipenv install --dev --verbose --system --deploy

EXPOSE 8000

WORKDIR ${WORKDIR}

ENTRYPOINT [ "/docker-entrypoint.sh" ]
