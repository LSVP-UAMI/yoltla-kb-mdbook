FROM peaceiris/mdbook:v0.4.40
RUN apk add --no-cache curl build-base
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"
RUN cargo install mdbook-extended-markdown-table