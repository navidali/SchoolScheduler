RUSTC = rustc
RUST_FLAGS = --crate-type=dylib

SOURCE_FILES = scheduler.rs
OUTPUT_FILE = sa.so

libxorcipher.so: ${SOURCE_FILES}
	${RUSTC} ${RUST_FLAGS} -o ${OUTPUT_FILE} ${SOURCE_FILES}

clean:
	rm ${OUTPUT_FILE}