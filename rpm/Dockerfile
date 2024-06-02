FROM rockylinux:9

WORKDIR /app
COPY . /app

RUN dnf install -y cargo openssl-devel lm_sensors-devel
RUN cargo install cargo-generate-rpm
RUN cargo build --release --all-features
RUN cargo clean -p minmon
RUN strip -s target/release/minmon
RUN cargo generate-rpm

RUN dnf install -y createrepo
RUN mkdir -p /srv/repository
RUN cp /app/target/generate-rpm/minmon-0.9.0-1.x86_64.rpm /srv/repository
RUN createrepo --update /srv/repository
RUN cp /app/rpm/minmon.repo /etc/yum.repos.d/minmon.repo
RUN dnf install -y minmon

ENTRYPOINT ["/bin/minmon"]
CMD ["/etc/minmon.toml"]