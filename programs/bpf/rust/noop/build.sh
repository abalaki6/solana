#!/usr/bin/env bash

cd "$(dirname "$0")"

cargo install xargo

set -e

# Ensure the sdk is installed
../../../../sdk/bpf/scripts/install.sh
rustup override set bpf

export RUSTFLAGS="$RUSTFLAGS \
    -C lto=no \
    -C opt-level=2 \
    -C link-arg=-Tbpf.ld \
    -C link-arg=-z -C link-arg=notext \
    -C link-arg=--Bdynamic \
    -C link-arg=-shared \
    -C link-arg=--entry=entrypoint \
    -C linker=../../../../sdk/bpf/llvm-native/bin/ld.lld"
export XARGO_HOME="$PWD/target/xargo"
export XARGO_RUST_SRC="../../../../sdk/bpf/rust-bpf-sysroot/src"
# export XARGO_RUST_SRC="../../../../../rust-bpf-sysroot/src"
xargo build --target bpfel-unknown-unknown --release -v

{ { set +x; } 2>/dev/null; echo Success; }
